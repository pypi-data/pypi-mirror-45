def repeat(*args, **kwargs):
    def wrapper(function):
        i = 1;
        while i <= kwargs['i']:
            function()
            i = i + 1
    return wrapper


