import shelve

class AnalysisCache:
    def __init__(self, filename, rebuild=False):
        self.cache = {}
        with shelve.open(filename) as shelf:
            if rebuild or not shelf:
                self.generate_cache()
                shelf['cache'] = self.cache
            else:
                self.cache = shelf['cache']

    def generate_cache(self):
        raise NotImplementedError
