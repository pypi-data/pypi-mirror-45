import types


class Context(dict):
    """ Immutable context based on `dict`
    """

    ContextIsImmutable = type('ContextIsImmutable', (Exception,), {})

    def __not_impl(self, *args, **kwargs):
        raise Context.ContextIsImmutable('Context is immutable')

    def __repr__(self):
        return f'<Context: {super().__repr__()}>'

    __setitem__ = __not_impl
    pop = __not_impl
    popitem = __not_impl
    update = __not_impl
    setdefault = __not_impl


class Context2(types.SimpleNamespace):
    """ Immutable context based on `types.SimpleNamespace`
    """

    ContextIsImmutable = type('ContextIsImmutable', (Exception,), {})

    def __setattr__(self, key, value):
        raise Context.ContextIsImmutable('Context is immutable')

    def __repr__(self):
        return f'<Context: {super().__repr__()}>'
