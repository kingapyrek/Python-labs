import copy
import types


class Matrix:
    def __init__(self, *args):
        if not args:
            self.elements = []
            self.N = 0
        else:
            if not type(args[0]) is list:
                self.from_numbers(self, args)
            else:
                self.elements = list(args)
                self.N = len(args[0])

    @staticmethod
    def from_numbers(self, args):
        self.elements = []
        i = 1
        self.N = 0
        elem = []
        while True:
            if i * i == len(args):
                self.N = i
                break
            i += 1

        for i in range(self.N * self.N):
            if i % self.N == self.N - 1:
                elem.append(args[i])
                self.elements.append(copy.deepcopy(elem))
                elem.clear()
            else:
                elem.append(args[i])

    def operation(self, other, operator):
        new_matrix = copy.deepcopy(self)
        if type(other) in (int, float):
            for i in range(self.N):
                for j in range(self.N):
                    if operator == "+":
                        new_matrix.elements[i][j] += other
                    elif operator == "/":
                        new_matrix.elements[i][j] /= other
                    elif operator == "*":
                        new_matrix.elements[i][j] *= other

        elif type(other) is Matrix:
            for i in range(self.N):
                for j in range(self.N):
                    if operator == "+":
                        new_matrix.elements[i][j] += other.elements[i][j]
                    elif operator == "*":
                        new_matrix.elements[i][j] *= other.elements[i][j]
                    elif operator == "/":
                        new_matrix.elements[i][j] /= other.elements[i][j]

        return new_matrix

    def __add__(self, other):
        return self.operation(other, "+")

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        new_matrix = copy.deepcopy(self)
        for i in range(self.N):
            for j in range(self.N):
                new_matrix.elements[i][j] = -1*self.elements[i][j]
        return new_matrix

    def __sub__(self, other):
        return self + (- other)

    def __rsub__(self, other):
        if type(other) in (int, float):
            new_matrix = copy.deepcopy(self)
            for i in range(new_matrix.N):
                for j in range(new_matrix.N):
                    new_matrix.elements[i][j] = other
            return  (new_matrix) - (self)
        else:
            return (self) - (other)

    def __mul__(self, other):
        return self.operation(other, "*")

    def __rmul__(self, other):
        return self.operation(other, "*")

    def __truediv__(self, other):
        return self.operation(other, "/")

    def __rtruediv__(self, other):
        new_matrix = copy.deepcopy(self)
        if type(other) in (int, float):
            for i in range(new_matrix.N):
                for j in range(new_matrix.N):
                    new_matrix.elements[i][j] = other
            return new_matrix / self
        else:
            return self.operation(other, "/")

    def __matmul__(self, other):
        new_matrix = copy.deepcopy(self)
        for i in range(self.N):
            for j in range(self.N):
                new_matrix.elements[i][j] = 0

        for i in range(len(self.elements)):
            for j in range(len(other.elements[0])):
                for k in range(len(other.elements)):
                    new_matrix.elements[i][j] += self.elements[i][k] * other.elements[k][j]

        return new_matrix

    def __iter__(self):
        self.row = -1
        return self

    def __next__(self):
        if self.row < self.N-1:
            self.row += 1
            return self.elements[self.row]
        else:
            raise StopIteration

    def __str__(self):
        result = '\n'
        for i in range(self.N):
            result += "["
            for j in range(self.N):
                if j != self.N-1:
                    result += str(round(self.elements[i][j], 2)) + ", "
                else:
                    result += str(round(self.elements[i][j], 2))
            result += ']\n'
        return result


if __name__ == "__main__":
    m1 = Matrix([1, 8, 5], [7, 5, 6], [7, 2, 4])
    m2 = Matrix(7, 8, 9, 2, 5, 6, 7, 8, 10)
    m3 = m1 + m2
    m4 = m1 - m2
    m5 = m1 + 5
    m6 = 5 + m1
    m7 = m1 - 7
    m8 = 7 - m1
    m9 = m1 * m2
    m10 = m1 * 3
    m11 = 3 * m1
    m12 = m1 / 4
    m13 = 4 / m1
    m14 = m1 / m2
    m15 = m1@m2

    print("m1: ", m1)
    print("m2: ", m2)
    print("m1 + m2 = {}".format(m3))
    print("m1 - m2 = {}".format(m4))
    print("m1 + 5 = {}".format(m5))
    print("5 + m1 = {}".format(m6))
    print("m1 - 7 = {}".format(m7))
    print("7 - m1 = {}".format(m8))
    print("m1 * m2 = {}".format(m9))
    print("m1 * 3 = {}".format(m10))
    print("3 * m1 = {}".format(m11))
    print("m1 / 4 = {}".format(m12))
    print("4 / m1 = {}".format(m13))
    print("m1 / m2 = {}".format(m14))
    print("m1 @ m2 = {}".format(m15))

    print('Iterator')
    for row in m1:
        print(row)