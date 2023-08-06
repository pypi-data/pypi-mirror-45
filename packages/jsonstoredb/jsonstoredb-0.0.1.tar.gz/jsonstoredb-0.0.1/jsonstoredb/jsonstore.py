import os
from .table import JSONStoreTable

class JSONStore(object):
    def __init__(self, *, folder="data"):
        if os.path.isfile(folder):
            raise ValueError(f"{folder} already exists and is a file.")
        if not os.path.isdir(folder):
            os.makedirs(folder)
        self._folder = folder
        self.tables = self.load_tables()
    
    def load_tables(self):
        return {
            os.path.splitext(filename)[0]: JSONStoreTable(os.path.join(self._folder, filename))
            for filename in os.listdir(self._folder)
        }

    def table(self, name):
        filename = self._filename(name)
        if not os.path.isfile(filename):
            with open(filename, "w") as table:
                table.write("{}")
            self.tables[name] = JSONStoreTable(filename)
        return self.tables[name]

    def _filename(self, name):
        return os.path.join(self._folder, f"{name}.json")
