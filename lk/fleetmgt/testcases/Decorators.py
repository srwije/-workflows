import functools


def before(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        instance.before_test()
        return func(*args, **kwargs)

    return wrapper


def after(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        instance = args[0]
        instance.after_test()
        return result

    return wrapper


def test(func):
    setattr(func, '__test__', True)
    return func
