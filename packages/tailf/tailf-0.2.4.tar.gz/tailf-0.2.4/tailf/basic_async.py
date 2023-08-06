import asyncio
from .basic import Tail as BaseTail


class Tail(BaseTail):
    """Follow file contents change.

    This class is iterable, and yields data portions as `bytes` objects and
    Truncated events until depleted. After raising StopIteration, new events
    may appear later.

    This class is iterable, and yields data portions as `bytes` objects and
    Truncated events until depleted. After raising StopIteration, new events
    may appear later.

    Asynchronous iteration awaits for more events to come.

    :ivar closed: True if this Tail object has been closed. False initially.

    :Limitations:

    * Truncation detection is unreliable in general. It is primarily tracked by
      file size decrease, which sometimes can be unreliable. In cases when a file
      grows large and is truncated seldom, this is sufficient.

    * Asynchronous tracking is done at timer events (0.01 seconds currently).
      Inotify support could solve this issue on linux. Feel free to suggest other
      solutions.
    """

    async def wait_event(self):
        """Wait for the next event and return it.

        :return: next event
        """
        while True:
            try:
                return next(self)
            except StopIteration:
                await asyncio.sleep(0.01)

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.wait_event()
