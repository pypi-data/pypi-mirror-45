class DF:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def columns(self):
        return set(self.a.columns).intersection(set(self.b.columns))

    def compare(self, *columns):
        a = self.a[list(columns)].rename(columns={col: f'old_{col}' for col in columns})
        b = self.b[list(columns)].rename(columns={col: f'new_{col}' for col in columns})

        return a.join(b)
