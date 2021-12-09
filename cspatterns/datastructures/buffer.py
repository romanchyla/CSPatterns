from collections.abc import Iterable


class CircularBuffer(object):
    """
    Hold predefined number of items arranged in a circular fashion
    so that it can simulate infinite sequence going in one direction.
    """

    def __init__(self, size, attrs):
        self.prev = [None] * size
        self.next = [None] * size

        if attrs and isinstance(attrs, Iterable):
            for a in attrs:
                setattr(self, a, None)
        self.size = size
        self.attrs = attrs

    @staticmethod
    def create(size, attrs=None):

        elements = [CircularBuffer(size, attrs) for _ in range(size)]
        for i, b in enumerate(elements):
            for j in range(1, size):
                b.prev[-j] = elements[i - j]
                b.next[j] = elements[(i + j) % size]
            b.prev[0] = b
            b.next[0] = b
        return elements[0]
