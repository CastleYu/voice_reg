class InvalidOpError(Exception):
    def __init__(self, left, right, key=None):
        if key is not None:
            key = f"{key}: "
        else:
            key = getattr(left, "key", None)
        msg = f"尝试将实例({key}{left.__class__})与类({right.__class__})的实例相运算"
        super().__init__(msg)


class KVNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    @property
    def type(self) -> str:
        return type(self.value).__name__

    def _check_op_cal(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return True
        if isinstance(self.value, (int, float)) and isinstance(other, (int, float)):
            return True
        raise InvalidOpError(self, other)

    def _check_op(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return True
        raise InvalidOpError(self, other)

    def __add__(self, other):
        self._check_op_cal(other)
        value = self.value + other.value if isinstance(other, self.__class__) else self.value + other
        return self.__class__(self.key, value)

    def __iadd__(self, other):
        self.value = self.__add__(other).value
        return self

    def __sub__(self, other):
        self._check_op_cal(other)
        value = self.value - other.value if isinstance(other, self.__class__) else self.value - other
        return self.__class__(self.key, value)

    def __isub__(self, other):
        self.value = self.__sub__(other).value
        return self

    def __mul__(self, other):
        self._check_op_cal(other)
        value = self.value * other.value if isinstance(other, self.__class__) else self.value * other
        return self.__class__(self.key, value)

    def __imul__(self, other):
        self.value = self.__mul__(other).value
        return self

    def __pow__(self, power, modulo=None):
        self._check_op_cal(power)
        value = self.value ** power % modulo if modulo is not None else self.value ** power
        return self.__class__(self.key, value)

    def __ipow__(self, power, modulo=None):
        self.value = self.__pow__(power, modulo).value
        return self

    def __truediv__(self, other):
        self._check_op_cal(other)
        value = self.value / other.value if isinstance(other, self.__class__) else self.value / other
        return self.__class__(self.key, value)

    def __itruediv__(self, other):
        self.value = self.__truediv__(other).value
        return self

    def __floordiv__(self, other):
        self._check_op_cal(other)
        value = self.value // other.value if isinstance(other, self.__class__) else self.value // other
        return self.__class__(self.key, value)

    def __ifloordiv__(self, other):
        self.value = self.__floordiv__(other).value
        return self

    def __mod__(self, other):
        self._check_op_cal(other)
        value = self.value % other.value if isinstance(other, self.__class__) else self.value % other
        return self.__class__(self.key, value)

    def __imod__(self, other):
        self.value = self.__mod__(other).value
        return self

    def __and__(self, other):
        self._check_op(other)
        value = self.value & other.value if isinstance(other, self.__class__) else self.value & other
        return self.__class__(self.key, value)

    def __iand__(self, other):
        self.value = self.__and__(other).value
        return self

    def __or__(self, other):
        self._check_op(other)
        value = self.value | other.value if isinstance(other, self.__class__) else self.value | other
        return self.__class__(self.key, value)

    def __ior__(self, other):
        self.value = self.__or__(other).value
        return self

    def __xor__(self, other):
        self._check_op(other)
        value = self.value ^ other.value if isinstance(other, self.__class__) else self.value ^ other
        return self.__class__(self.key, value)

    def __ixor__(self, other):
        self.value = self.__xor__(other).value
        return self

    def __lshift__(self, other):
        return self

    def __ilshift__(self, other):
        self.value = self.__lshift__(other).value
        return self

    def __rshift__(self, other):
        return self

    def __irshift__(self, other):
        self.value = self.__rshift__(other).value
        return self

    def __invert__(self):
        return self.__class__(self.key, ~self.value)

    def __eq__(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return self.value == other.value if isinstance(other, self.__class__) else self.value == other
        return False

    def __ne__(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return self.value != other.value if isinstance(other, self.__class__) else self.value != other
        return True

    def __lt__(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return self.value < other.value if isinstance(other, self.__class__) else self.value < other
        raise InvalidOpError(self, other)

    def __le__(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return self.value <= other.value if isinstance(other, self.__class__) else self.value <= other
        raise InvalidOpError(self, other)

    def __gt__(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return self.value > other.value if isinstance(other, self.__class__) else self.value > other
        raise InvalidOpError(self, other)

    def __ge__(self, other):
        if isinstance(other, self.value.__class__) or isinstance(other, self.__class__):
            return self.value >= other.value if isinstance(other, self.__class__) else self.value >= other
        raise InvalidOpError(self, other)

    def __int__(self):
        return self.__class__(self.key, int(self.value))

    def __float__(self):
        return self.__class__(self.key, float(self.value))

    def __bool__(self):
        return bool(self.value)

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        return iter(self.value)

    def __repr__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        # return hash((self.key, self.value))
        return hash(self.value)

    def __call__(self, *args, **kwargs):
        return self

    @property
    def print(self):
        print(self)
        return self
