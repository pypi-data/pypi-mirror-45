import json

class JSONStoreTable(object):
    def __init__(self, filename):
        self._file = open(filename, 'r+')
        self.data = json.loads(self._read())

    def insert(self, key, value):
        self.data[key] = value
        self.sync()
    
    def select(self, key):
        return self.data.get(key)
    
    def selectBy(self, predicate, limit=1):
        results = []
        for key, value in self.data.items():
            if predicate(value):
                results.append((key, value))
                if limit and len(results) == limit:
                    break
        return results

    def sync(self):
        self._file.seek(0)
        self._file.write(json.dumps(self.data))

    def _read(self):
        self._file.seek(0)
        return self._file.read()
