from __future__ import division
import json
import os
import socket
import logging
import threading
from datetime import datetime
from time import sleep
from functools import total_ordering, wraps, partial

from flask import Flask, Blueprint
from flask import render_template, redirect, request, url_for, jsonify
import waitress
import rpyc
from rpyc.utils.server import ThreadedServer

import kuyruk
from kuyruk.signals import worker_start, worker_init

logger = logging.getLogger(__name__)

CONFIG = {
    "MANAGER_HOST": "127.0.0.1",
    "MANAGER_PORT": 16501,
    "MANAGER_LISTEN_HOST": "127.0.0.1",
    "MANAGER_LISTEN_PORT": 16501,
    "MANAGER_LISTEN_HOST_HTTP": "127.0.0.1",
    "MANAGER_LISTEN_PORT_HTTP": 16500,
    "SENTRY_PROJECT_URL": None,
}

ACTION_WAIT_TIME = 1  # seconds


def start_daemon_thread(target, args=()):
    t = threading.Thread(target=target, args=args)
    t.daemon = True
    t.start()
    return t


def retry(sleep_seconds=1, stop_event=threading.Event(),
          on_exception=lambda e: logger.debug(e)):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            while not stop_event.is_set():
                try:
                    f(*args, **kwargs)
                except Exception as e:
                    if on_exception:
                        on_exception(e)
                    if sleep_seconds:
                        sleep(sleep_seconds)
        return inner
    return decorator


def _connect_rpc(worker):
    conn = rpyc.connect(worker.kuyruk.config.MANAGER_HOST,
                        worker.kuyruk.config.MANAGER_PORT,
                        service=_WorkerService(worker),
                        config={"allow_pickle": True})
    rpyc.BgServingThread(conn)._thread.join()


def start_rpc_thread(sender, worker=None):
    start_daemon_thread(retry()(_connect_rpc), args=(worker, ))


def add_exit_method(sender, worker=None):
    worker.manager_exit = partial(os._exit, 0)


class Manager(object):

    def __init__(self, kuyruk):
        self.kuyruk = kuyruk
        self.service = _ManagerService()
        self.requeue = kuyruk.extensions.get("requeue")

        self.has_sentry = "sentry" in kuyruk.extensions
        if self.has_sentry and not kuyruk.config.SENTRY_PROJECT_URL:
            raise Exception("SENTRY_PROJECT_URL is not set")

        worker_start.connect(start_rpc_thread, sender=kuyruk, weak=False)
        worker_init.connect(add_exit_method, sender=kuyruk, weak=False)

        kuyruk.extensions["manager"] = self

    def start_rpc_server(self):
        s = ThreadedServer(self.service,
                           hostname=self.kuyruk.config.MANAGER_LISTEN_HOST,
                           port=self.kuyruk.config.MANAGER_LISTEN_PORT)
        start_daemon_thread(s.start)

    def flask_blueprint(self):
        b = Blueprint("kuyruk_manager", __name__)
        b.add_url_rule('/', 'index', self._get_index)
        b.add_url_rule('/workers', 'workers', self._get_workers)
        b.add_url_rule('/failed-tasks', 'failed_tasks',
                       self._get_failed_tasks)
        b.add_url_rule('/api/failed-tasks', 'api_failed_tasks',
                       self._api_get_failed_tasks)
        b.add_url_rule('/action', 'action',
                       self._post_action, methods=['POST'])
        b.add_url_rule('/action-all', 'action_all',
                       self._post_action_all, methods=['POST'])
        b.add_url_rule('/requeue', 'requeue_task',
                       self._post_requeue, methods=['POST'])
        b.add_url_rule('/delete', 'delete_task',
                       self._post_delete, methods=['POST'])
        b.context_processor(self._context_processors)
        return b

    def flask_application(self):
        app = Flask(__name__)
        app.debug = True
        app.register_blueprint(self.flask_blueprint())
        return app

    def _get_index(self):
        return redirect(url_for('kuyruk_manager.workers'))

    def _get_workers(self):
        hostname = request.args.get('hostname')
        queue = request.args.get('queue')
        consuming = request.args.get('consuming')
        working = request.args.get('working')

        workers = {}
        for addr, worker in self.service.workers.items():
            if hostname and hostname != worker.stats.get('hostname', ''):
                continue
            if queue and queue not in worker.stats.get('queues', []):
                continue
            if consuming and not worker.stats.get('consuming', False):
                continue
            if working and not worker.stats.get('current_task', None):
                continue
            workers[addr] = worker

        return render_template('workers.html', sockets=workers)

    def _failed_tasks(self):
        tasks = self.requeue.redis.hvals('failed_tasks')
        tasks = [t.decode('utf-8') for t in tasks]
        decoder = json.JSONDecoder()
        tasks = map(decoder.decode, tasks)
        return tasks

    def _get_failed_tasks(self):
        tasks = list(self._failed_tasks())
        return render_template('failed_tasks.html', tasks=tasks)

    def _api_get_failed_tasks(self):
        return jsonify(tasks=self._failed_tasks())

    def _post_action(self):
        addr = (request.args['host'], int(request.args['port']))
        worker = self.service.workers[addr]
        f = getattr(worker.conn.root, request.form['action'])
        rpyc.async_(f)()
        sleep(ACTION_WAIT_TIME)
        return redirect_back()

    def _post_action_all(self):
        for addr, worker in self.service.workers.items():
            f = getattr(worker.conn.root, request.form['action'])
            rpyc.async_(f)()
        sleep(ACTION_WAIT_TIME)
        return redirect_back()

    def _post_requeue(self):
        task_id = request.form['task_id']
        redis = self.requeue.redis

        if task_id == 'ALL':
            self.requeue.requeue_failed_tasks()
        else:
            failed = redis.hget('failed_tasks', task_id)
            failed = json.loads(failed)
            self.requeue.requeue_task(failed)

        return redirect_back()

    def _post_delete(self):
        task_id = request.form['task_id']
        self.requeue.redis.hdel('failed_tasks', task_id)
        return redirect_back()

    def _context_processors(self):
        return {
            'manager': self,
            'now': str(datetime.utcnow())[:19],
            'hostname': socket.gethostname(),
            'has_requeue': self.requeue is not None,
            'has_sentry': self.has_sentry,
            'sentry_url': self._sentry_url,
            'human_time': self._human_time,
        }

    def _sentry_url(self, sentry_id):
        if not sentry_id:
            return

        url = self.kuyruk.config.SENTRY_PROJECT_URL
        if not url.endswith('/'):
            url += '/'

        url += '?query=%s' % sentry_id
        return url

    def _human_time(self, seconds, suffixes=['y', 'w', 'd', 'h', 'm', 's'],
                    add_s=False, separator=' '):
        """
        Takes an amount of seconds and
        turns it into a human-readable amount of time.

        """
        # the formatted time string to be returned
        time = []

        # the pieces of time to iterate over (days, hours, minutes, etc)
        # the first piece in each tuple is the suffix (d, h, w)
        # the second piece is the length in seconds (a day is 60s * 60m * 24h)
        parts = [
            (suffixes[0], 60 * 60 * 24 * 7 * 52),
            (suffixes[1], 60 * 60 * 24 * 7),
            (suffixes[2], 60 * 60 * 24),
            (suffixes[3], 60 * 60),
            (suffixes[4], 60),
            (suffixes[5], 1)]

        # for each time piece, grab the value and remaining seconds,
        # and add it to the time string
        for suffix, length in parts:
            value = seconds // length
            if value > 0:
                seconds %= length
                time.append('%s%s' % (str(value), (
                    suffix, (suffix, suffix + 's')[value > 1])[add_s]))
            if seconds < 1:
                break

        return separator.join(time)


def redirect_back():
    referrer = request.headers.get('Referer')
    if referrer:
        return redirect(referrer)
    return 'Go back'


class _ManagerService(rpyc.Service):
    def __init__(self):
        self.workers = {}
        super().__init__()

    def on_connect(self, conn):
        addr = conn._config['endpoints'][1]
        logger.info("Client connected: %s", addr)
        worker = _Worker(conn)
        start_daemon_thread(target=worker._read_stats)
        self.workers[addr] = worker

    def on_disconnect(self, conn):
        addr = conn._config['endpoints'][1]
        logger.info("Client disconnected: %s", addr)
        del self.workers[addr]


class _WorkerService(rpyc.Service):
    def __init__(self, worker):
        self.worker = worker
        super().__init__()

    def exposed_warm_shutdown(self):
        return self.worker.shutdown()

    def exposed_cold_shutdown(self):
        return self.worker.manager_exit()

    def exposed_quit_task(self):
        return self.worker.drop_task()

    def exposed_get_stats(self):
        return {
            'hostname': socket.gethostname(),
            'uptime': int(self.worker.uptime),
            'pid': os.getpid(),
            'version': kuyruk.__version__,
            'current_task': getattr(self.worker.current_task, "name", None),
            'current_args': self.worker.current_args,
            'current_kwargs': self.worker.current_kwargs,
            'consuming': self.worker.consuming,
            'queues': self.worker.queues,
        }


@total_ordering
class _Worker:
    def __init__(self, conn):
        self.conn = conn
        self.stats = {}

    def __lt__(self, other):
        if not self.sort_key:
            return False

        if not other.sort_key:
            return True

        # TODO there is a bug with this comparison statement.
        # Eat the error until the fix.
        #   TypeError: unorderable types: NoneType() < str()
        try:
            return self.sort_key < other.sort_key
        except Exception:
            return True

    def _read_stats(self):
        while True:
            try:
                proxy_obj = self.conn.root.get_stats()
                self.stats = rpyc.classic.obtain(proxy_obj)
            except Exception as e:
                logger.error("%s", e)
                try:
                    self.conn.close()
                except Exception:
                    pass
                return
            sleep(1)

    @property
    def sort_key(self):
        order = ('hostname', 'queues', 'uptime', 'pid')
        # TODO replace get_stat with operator.itemgetter
        return tuple(self.get_stat(attr) for attr in order)

    def get_stat(self, name):
        return self.stats.get(name, None)


def run_manager(kuyruk, args):
    manager = kuyruk.extensions["manager"]
    manager.start_rpc_server()

    app = manager.flask_application()
    waitress.serve(
            app,
            host=kuyruk.config.MANAGER_LISTEN_HOST_HTTP,
            port=kuyruk.config.MANAGER_LISTEN_PORT_HTTP)


help_text = "see and manage kuyruk workers"

command = (run_manager, help_text, None)
