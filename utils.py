from six.moves import cPickle


def load(path):
    f = open(path, "rb")
    dicts = cPickle.load(f)
    f.close()
    return dicts


def dump(dicts, path):
    f = open(path, "wb")
    cPickle.dump(dicts, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()
