def make_path(*args):
    import os
    loc = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(loc, *args)
