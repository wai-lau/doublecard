import shelve

class AnalysisCache:
    def __init__(self, filename, rebuild=False):
        self.cache = {}
        with shelve.open(filename) as shelf:
            if rebuild or not shelf:
                print("Creating", type(self).__name__ + "...")
                self.generate_cache()
                shelf['cache'] = self.cache
            else:
                print("Loading", type(self).__name__)
                self.cache = shelf['cache']

    def generate_cache(self):
        raise NotImplementedError
