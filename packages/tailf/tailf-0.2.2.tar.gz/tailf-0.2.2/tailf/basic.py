import os
import os.path

from .const import *

__all__ = ["Tail"]


class Tail:
    """Follow file contents change.

    This class is iterable, and yields data portions as `bytes` objects and
    Truncated events until depleted. After raising StopIteration, new events
    may appear later.

    :Limitations:

    * Truncations are tracked primarily by file size change. That doesn't
    guarantee 100% reliability. If the file grows quite large before
    truncation, that would not be an issue. `tail -f` in linux might expose the
    same limitation.
    """

    def __init__(self, path):
        self.path = path
        head, tail = os.path.split(path)
        if not tail:
            raise ValueError("directory path")
        if not head:
            head = "."
        self.dir, self.filename = head, tail
        self.file = None
        self.last_truncated = True
        self.closed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._check_truncated_pre_data():
            if self.file is not None and not self.file.closed:
                self.file.close()
                self.file = None
            if not self.last_truncated:
                # report Truncated if we haven't just reported it already
                self.last_truncated = True
                return Truncated
            raise StopIteration
        data = self.file.read()
        if len(data):
            self.last_truncated = False
            self.file_pos += len(data)
            return data
        if self._check_truncated_post_data():
            if self.file is not None and not self.file.closed:
                self.file.close()
                self.file = None
            if not self.last_truncated:
                # report Truncated if we haven't just reported it already
                self.last_truncated = True
                return Truncated
            raise StopIteration
        raise StopIteration

    def _check_truncated_pre_data(self):
        """do truncation checks before reading data"""
        if self.file is None:
            try:
                self.file = open(self.path, "rb")
                self.file_pos = 0  # only valid if self.file is not None
            except EnvironmentError:
                return True
        stat = os.fstat(self.file.fileno())
        if stat.st_size < self.file_pos:
            return True
        # TODO check creation date on Windows. (pre/post - ?)

    def _check_truncated_post_data(self):
        """do truncation checks after reading data"""
        # TODO check path existance (and maybe inode number consistency). If
        # the file was deleted/recreated, return True
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def close(self):
        if self.closed:
            return
        if self.file is not None:
            self.file.close()
        self.file = None
        self.closed = True
