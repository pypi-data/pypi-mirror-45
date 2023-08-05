import hashlib
import os
import tempfile
from functools import wraps

import requests
from django.core.files import File
from django.utils.functional import SimpleLazyObject, empty


def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()


def retry(max_retries):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            for i in range(max_retries - 1):
                try:
                    return f(*args, **kwargs)
                except Exception:
                    pass

            return f(*args, **kwargs)

        return inner

    return wrapper


def file_get_url(url):
    f = tempfile.NamedTemporaryFile('w+b')
    response = requests.get(url, stream=True)
    if not response.ok:
        raise FileNotFoundError()

    for content_chunk in response.iter_content(chunk_size=1024 * 1024):
        f.write(content_chunk)

    f.seek(0)

    return f


def lazy_remote_file(url, name=None):
    if not name:
        name = os.path.basename(url)

    def _load():
        return File(file_get_url(url), name=name)

    return SimpleLazyObject(_load)


def resolve_lazy_remote_file(file):
    if isinstance(file, SimpleLazyObject):
        if file._wrapped is empty:
            try:
                file._setup()
            except FileNotFoundError:
                return None

        return file._wrapped

    return file
