import os


def setup_prealoder(testfile, response_class=None):
    """Loading examples from results folder."""
    def preload_example(name, response_class=response_class):
        fname = os.path.join(os.path.split(testfile)[0],
                             'examples', name)
        with open(fname, 'r') as f:
            return f.read()

    return preload_example
