class IntLike:
    def __init__(self, value):
        self.value = value

    # 算术运算符
    def __add__(self, other):
        if isinstance(other, IntLike):
            return IntLike(self.value + other.value)
        return IntLike(self.value + other)

    def __sub__(self, other):
        if isinstance(other, IntLike):
            return IntLike(self.value - other.value)
        return IntLike(self.value - other)

    def __mul__(self, other):
        if isinstance(other, IntLike):
            return IntLike(self.value * other.value)
        return IntLike(self.value * other)

    def __truediv__(self, other):
        if isinstance(other, IntLike):
            return IntLike(self.value / other.value)
        return IntLike(self.value / other)

    def __floordiv__(self, other):
        if isinstance(other, IntLike):
            return IntLike(self.value // other.value)
        return IntLike(self.value // other)

    # 比较运算符
    def __eq__(self, other):
        if isinstance(other, IntLike):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, IntLike):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, IntLike):
            return self.value <= other.value
        return self.value <= other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    # 一元运算符和其他必要方法
    def __int__(self):
        return int(self.value)

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return str(self.value)


if __name__ == '__main__':
    x = IntLike(5)
    y = IntLike(3)
    print(x + y)  # 输出 8
    print(x > 2)  # 输出 True
    print(x * 3)  # 输出 15
    print(int(x))  # 输出 5
