import asyncio
from .basic import Tail as BaseTail


class Tail(BaseTail):
    async def wait_event(self):
        """

        :return: next event or None
        """
        while True:
            try:
                return next(self)
            except StopIteration:
                await asyncio.sleep(0.01)
