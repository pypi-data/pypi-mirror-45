import os
import os.path

from .const import *

__all__ = ["Tail"]


class Tail:
    """Follow file contents change.

    This class is iterable, and yields data portions as `bytes` objects and
    Truncated events until depleted. After raising StopIteration, new events
    may appear later.

    :ivar closed: True if this Tail object has been closed. False initially.

    :Limitations:

    * Truncation detection is unreliable in general. It is primarily tracked by
      file size decrease, which sometimes can be unreliable. In cases when a file
      grows large and is truncated seldom, this is sufficient.
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
        if self.closed:
            raise ValueError("closed")
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
            self._file_pos += len(data)
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
                self._file_pos = 0  # only valid if self.file is not None
            except EnvironmentError:
                return True
        stat = os.fstat(self.file.fileno())
        if stat.st_size < self._file_pos:
            return True
        self._file_id = (stat.st_dev, stat.st_ino)

    def _check_truncated_post_data(self):
        """do truncation checks after reading data"""
        try:
            stat = os.stat(self.path)
        except EnvironmentError:
            # TODO when file is unlinked, maybe it's better to keep following
            # it, until a file with the same name is created again
            return Truncated
        if self._file_id != (stat.st_dev, stat.st_ino):
            return Truncated

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def close(self):
        """Finalize this Tail object and free underlying resources.

        It is allowed to close an already closed Tail object.
        """
        if self.closed:
            return
        if self.file is not None:
            self.file.close()
        self.file = None
        self.closed = True
