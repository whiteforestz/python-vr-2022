def gen_cat(name):
    with open(name) as f:
        while True:
            line = f.readline()
            if not line:
                break

            yield line


def gen_head(n, src):
    counter = 0
    for line in src:
        if counter > n:
            break

        yield line
        counter += 1


def gen_grep(kw, src):
    for line in src:
        if kw in line:
            yield line


out_cat = gen_cat('/Users/wfzx/dev/python/lesson/iterator/main.py')
out_head = gen_head(10, out_cat)
out_grep = gen_grep('val', out_head)
