class lazy_property(object):
    def __init__(self, func=None):
        self._func = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__
        self._sfunc = None

    def __get__(self, instance, owner=None):
        myname = self.__name__
        privname = '_'+instance.__class__.__name__+'__'+myname

        if instance is None: return self

        if self._func is None:
            raise AttributeError, "unknown attribute %s" % myname
        # Check if we've already loaded from API
        if 'loaded' in instance.__dict__:
            if myname in dir(instance):
                return self._func(instance)
            else:
                raise AttributeError, "unknown attribute %s" % myname
        elif myname in instance.__dict__:
            return self._func(instance)
        else:
            if getattr(instance, instance.primary_key) is not None:
                try:
                    instance.load()
                except AttributeError:
                    if instance.last_error is not None:
                        return instance.last_error
                    else:
                        raise AttributeError, "unknown attribute %s" % myname

        return self._func(instance)

    def __set__(self, instance, value):
        if self._sfunc is None:
            raise TypeError, "immutable attribute: %s" % self.__name__
        else:
            self._sfunc(instance, value)

    def setter(self, sfunc):
        self._sfunc = sfunc
        return self
