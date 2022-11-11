import functools


def coroutine(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        cr = f(*args, **kwargs)
        next(cr)
        return cr

    return wrapped


@coroutine
def cr_cat(name, dst):
    with open(name) as f:
        while True:
            line = f.readline()
            if not line:
                break

            try:
                dst.send(line)
            except StopIteration:
                break

            yield


@coroutine
def cr_head(n, dst):
    counter = 0
    while True:
        if counter > n:
            break

        line = yield
        counter += 1

        dst.send(line)


@coroutine
def cr_grep(kw, dst):
    while True:
        line = yield
        if kw in line:
            dst.send(line)


@coroutine
def cr_reader():
    while True:
        line = yield
        print(line, end='')


out_reader = cr_reader()
out_grep = cr_grep('val', out_reader)
out_head = cr_head(10, out_grep)
out_cat = cr_cat('/Users/wfzx/dev/python/lesson/iterator/main.py', out_head)
