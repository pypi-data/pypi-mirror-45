__all__ = ["Truncated"]


class TailEvent:
    __slots__ = "_name"

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return "TailEvent(%r)" % (self.__class__.name, self._name)

    def __str__(self):
        return repr(self)


Truncated = TailEvent("Truncated")
