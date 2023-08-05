import os
import time
import logging
import threading
import multiprocessing
from six.moves.queue import Queue

from alephclient.errors import AlephException
from alephclient.util import Path

log = logging.getLogger(__name__)

THREADS = int(os.getenv("ALEPHCLIENT_THREADS", 5 * multiprocessing.cpu_count()))  # noqa
TIMEOUT = int(os.getenv("ALEPHCLIENT_TIMEOUT", 5))
MAX_TRIES = int(os.getenv("ALEPHCLIENT_MAX_TRIES", 3))


def _get_foreign_id(root_path, path):
    if path == root_path:
        if path.is_dir():
            return
        return path.name
    if root_path in path.parents:
        return str(path.relative_to(root_path))


def _upload_path(api, collection_id, languages, root_path, path):
    foreign_id = _get_foreign_id(root_path, path)
    if foreign_id is None:
        return
    metadata = {
        'foreign_id': foreign_id,
        'languages': languages,
        'file_name': path.name,
    }
    log.info('Upload [%s]: %s', collection_id, foreign_id)
    parent_id = _get_foreign_id(root_path, path.parent)
    if parent_id is not None:
        metadata['parent'] = {'foreign_id': parent_id}
    file_path = None if path.is_dir() else path
    api.ingest_upload(collection_id, file_path, metadata=metadata)


def _crawl_path(q, api, collection_id, languages, root_path, path):
    _upload_path(api, collection_id, languages, root_path, path)
    if not path.is_dir():
        return
    for child in path.iterdir():
        q.put((child, 1))


def _upload(q, api, collection_id, languages, root_path):
    while not q.empty():
        path, try_number = q.get()
        try:
            _crawl_path(q, api, collection_id, languages, root_path, path)
        except AlephException as exc:
            if exc.status >= 500 and try_number < MAX_TRIES:
                time.sleep(TIMEOUT * try_number)
                q.put((path, try_number + 1))
            else:
                log.error(exc.message)
        except Exception:
            log.exception('Failed [%s]: %s', collection_id, path)
        q.task_done()


def crawl_dir(api, path, foreign_id, config):
    """Crawl a directory and upload its content to a collection

    params
    ------
    path: path of the directory
    foreign_id: foreign_id of the collection to use.
    language: language hint for the documents
    """
    path = Path(path).resolve()
    collection = api.load_collection_by_foreign_id(foreign_id, config)
    collection_id = collection.get('id')
    languages = config.get('languages', [])
    q = Queue()
    q.put((path, 1))
    threads = []
    for i in range(THREADS):
        args = (q, api, collection_id, languages, path)
        t = threading.Thread(target=_upload, args=args)
        t.daemon = True
        t.start()
        threads.append(t)

    # block until all tasks are done
    q.join()
    for t in threads:
        t.join()
