import functools
import inspect

class bind(object):
    """
    Inspired by boost::bind (C++).
    Behaves like functools.partial, but discards any extra parameters it gets when called.
    Also, bind objects can be compared for equality.
    """
    def __init__(self, f, *args):
        self.f = f
        self.bound_args = args
        self.numUnboundArgs = len(inspect.getargspec(self.f).args) - len(self.bound_args)
        if hasattr(f, 'im_self'):
            self.numUnboundArgs -= 1
    def __call__(self, *args):
        self.f(*(self.bound_args + args[0:self.numUnboundArgs]))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        result = True
        result &= ( self.f == other.f )
        result &= ( self.bound_args == other.bound_args )
        result &= ( self.numUnboundArgs == other.numUnboundArgs )
        return result
    
    def __ne__(self, other):
        return not ( self == other )