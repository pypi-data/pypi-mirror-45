# https://stackoverflow.com/a/279586
def static_variable(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate
