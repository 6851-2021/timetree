class LinkedNode:
    """ Base class for circular linked list nodes

    Provides self.prev and self.next, as well as functions for insert/remove
    We assume lists are circular and thus don't bother validating that prev
    and next are not None.
    """
    __slots__ = ('prev', 'next',)

    is_head = False
    is_node = True

    def __init__(self):
        self.prev = None
        self.next = None

    def insert(self, prev):
        """ Insert yourself into prev's linked list right after prev """
        # Insert self between prev..next
        assert self.prev is None and self.next is None, 'prev and next should be None'
        assert prev is not None

        self.next = prev.next
        self.next.prev = self

        self.prev = prev
        self.prev.next = self

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev

        self.next = None
        self.prev = None


class LinkedList:
    """ Base class for heads of circular linked lists """
    __slots__ = ('prev', 'next',)

    is_head = True
    is_node = False

    def __init__(self):
        self.prev = self
        self.next = self

    def append(self, new_node):
        new_node.insert(self.prev)

    def prepend(self, new_node):
        new_node.insert(self)

    def __iter__(self):
        return LinkedListIterator(self)

    def __reversed__(self):
        return LinkedListReverseIterator(self)


class LinkedListIterator:
    __slots__ = ('node',)

    def __init__(self, list):
        self.node = list

    def __iter__(self):
        return self

    def __next__(self):
        result = self.node.next
        if result.is_head:
            raise StopIteration
        self.node = result
        return result


class LinkedListReverseIterator:
    __slots__ = ('node',)

    def __init__(self, list):
        self.node = list

    def __iter__(self):
        return self

    def __next__(self):
        result = self.node.prev
        if result.is_head:
            raise StopIteration
        self.node = result
        return result


class HeadTrackingNodeMixin(LinkedNode):
    __slots__ = ('head',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head = None

    def insert(self, prev):
        self.head = prev.head
        super().insert(prev)

    def remove(self):
        super().remove()
        self.head = None


class HeadTrackingListMixin(LinkedList):
    __slots__ = ('head',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.head = self


class SizeTrackingNodeMixin(HeadTrackingNodeMixin):
    __slots__ = ()

    def insert(self, prev):
        super().insert(prev)
        self.head.size += 1

    def remove(self):
        self.head.size -= 1
        super().remove()

    @property
    def size(self):
        return self.head.size


class SizeTrackingListMixin(HeadTrackingListMixin):
    __slots__ = ('size',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 0

    def __len__(self):
        return self.size
