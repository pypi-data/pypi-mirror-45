

class Vector:

    def __init__(self, values):
        self._values = list(values)
    
    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return f'Vector({self._values   })'

    def __str__(self):
        return ''.join([f'{v:>10.2f}' for v in self])

    def __ne__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError
            return Vector([a != b for a, b in zip(self, other)])
        if isinstance(other, (int, float)):
            return Vector([a != other for a in self])
        raise ValueError()

    def equals(self, other):
        return self._values == other._values

    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError
            return Vector([a * b for a, b in zip(self, other)])
        if isinstance(other, (int, float)):
            return Vector([a * other for a in self])
        raise ValueError()

    def __matmul__(self, other):
        if not isinstance(other, Vector):
            raise ValueError
        return sum(self * other)
    
    def __getitem__(self, i):
        return self._values[i]

    def __setitem__(self, index, value):
        if isinstance(index, int):
            if not isinstance(value, (int, float)):
                raise ValueError(f'Expected int or float. Got {value}.')
            self._values[index] = value
        elif isinstance(index, Vector):
            if not isinstance(value, Vector):
                raise ValueError(f'Expected Vector. Got {value}.')
            if len(self) != len(index):
                raise ValueError
            for i in range(len(self)):
                if index[i]:
                    self._values[i] = value[i]
            
    @staticmethod
    def ones(size):
        return Vector([1.0] * size)

    
class Matrix:
    def __init__(self, rows):
        rows = [Vector(row) for row in rows]
        assert len(set(len(v) for v in rows)) == 1
        self.shape = len(rows), len(rows[0])
        self.rows = rows

    def __getitem__(self, i):
        return self.rows[i]

    def __repr__(self):
        return f'Matrix({self.rows})'

    def __iter__(self):
        return iter(self.rows)

    def __str__(self):
        return '\n'.join(
            str(row)
            for row in self
        )
        
    def __matmul__(self, vec):
        if not isinstance(vec, Vector):
            raise ValueError
        if self.shape[1] != len(vec):
            raise ValueError

        return Vector([self[i] @ vec for i in range(self.shape[0])])