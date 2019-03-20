import shelve

class AnalysisCache:
    def __init__(self, filename, rebuild=False):
        self.cache = {}
        with shelve.open(filename) as shelf:
            if rebuild or not shelf:
                print("Creating stuff")
                self.generate_cache()
                shelf['cache'] = self.cache
            else:
                print("Loading stuff")
                self.cache = shelf['cache']

    def generate_cache(self):
        raise NotImplementedError
