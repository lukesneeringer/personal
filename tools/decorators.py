from django.contrib import admin

def cached_property(method):
    """Decorator that turns a method into a special kind of property;
    it retrieves the data requested by the method, and caches the result
    so that future calls to the property do not invoke the computation time.
    
    This decorator is intended for expensive property calls (e.g. how many threads in this forum?)
    which, while they may change often, are unlikely to change during the life cycle of a request."""
    
    def f(self):
        # do I have a metadata repository?
        if not hasattr(self, '_metadata_cache'):
            self._metadata_cache = {}

        # do I already have the result cached?
        if method.__name__ in self._metadata_cache:
            return self._metadata_cache[method.__name__]
            
        # okay, I don't so I need to run the method
        answer = method(self)
        
        # cache the response
        self._metadata_cache[method.__name__] = answer
        return self._metadata_cache[method.__name__]
    return property(f)
    
    
def admin_register(model):
    """Method that returns a decorator that registers the admin class,
    running it through admin.site.register."""
    
    def f(class_):
        admin.site.register(model, class_)
        return class_
    return f