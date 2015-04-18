"""

File downloader with progress bar and download speed

"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from ..console import Console
from ..progress import Progress

import hashlib
import requests
from time import time


class DownloaderError(Exception):
    pass


def _filesize(size):
    try:
        size = int(size)
    except:
        raise ValueError("filesize requires a numeric value, not {!r}".format(size))
    suffixes = ('kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    base = 1024
    if size == 1:
        return '1 byte'
    elif size < base:
        return '{:,} bytes'.format(size)

    for i, suffix in enumerate(suffixes):
        unit = base ** (i + 2)
        if size < unit:
            return "{:,.01f} {}".format((base * size / unit), suffix)
    return "{:,.01f} {}".format((base * size / unit), suffix)


def download(url, store_file, filename=None, console=None, chunk_size=1024 * 16, auth=None, verify_ssl=True):
    """Download a url and render a progress bar"""
    if console is None:
        console = Console()

    if filename is None:
        filename = url.rsplit('/')[-1]

    progress_width = 20
    progress = Progress(console, 'downloading {}'.format(filename), width=progress_width)
    progress.update(0, msg="contacting server")
    try:

        response = requests.get(url, stream=True, auth=auth, verify=verify_ssl)
        start = time()
        length = response.headers.get('content-length')
        if response.status_code != 200:
            raise DownloaderError('downloader received bad status code ({})'.format(response.status_code))

        m = hashlib.md5()
        bytes_read = 0
        if length is None:
            console('downloading {}'.format(filename))
            console.flush()
            for data in response.iter_content(chunk_size):
                store_file.write(data)
                m.update(data)

            console.nl()
        else:
            length = int(length)
            progress.set_num_steps(length)
            #with console.progress('downloading {}'.format(filename), length, width=progress_width) as progress:
            for data in response.iter_content(chunk_size):
                store_file.write(data)
                m.update(data)
                bytes_read += len(data)

                bytes_per_second = int(float(bytes_read) / (time() - start))
                speed = "downloading {} {}/s".format(filename, _filesize(bytes_per_second))

                progress.step(len(data), msg=speed)
    finally:
        progress.done()

    return m.hexdigest()
