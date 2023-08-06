import math

class fv:
    def __init__(self, value, data_type="str"):
        self.value = str(value)
        self.data_type = data_type
        # this is a fluid variable, which mimics the variables scratch uses
        # it needs a .type attribute, as certain blocks behave differently
        # it is either: string or number
        # everything but these make it a string:
        # +
        # -
        # /
        # *
        # random
        # mod
        # round
        # abs etc...
        # change by 1

    def __repr__(self):
        return "<fv value:{0} type:{1}>".format(self.value, self.data_type)


    def value_type(self, value):
        try:
            if int(float(value.value)) == float(value.value):
                return "int"
            else:
                return "float"
        except ValueError:
            return "str"

    def convert_to_type(self, value):
        data_type = self.value_type(value)
        if data_type == "int":
            return int(float(value.value))
        elif data_type == "float":
            return float(value.value)
        elif data_type == "str":
            return value.value

    def string_to_0(self, value):
        data_type = self.value_type(value)
        if data_type == "str":
            return 0
        elif data_type in ["int", "float"]:
            return self.convert_to_type(value)

    def compare_char_values(self, other):
        longest_code = 0 
        v1_list = []
        for item in range(len(self.value)):
            char = self.value[item]
            char_code = ord(char)
            longest_code = max(longest_code, len(str(char_code)))
            v1_list.append(char_code)
        v2_list = []
        for item in range(len(other.value)):
            char = other.value[item]
            char_code = ord(char)
            longest_code = max(longest_code, len(str(char_code)))
            v2_list.append(char_code)
        v1 = ""
        for item in range(len(v1_list)):
            number_of_0s = longest_code-len(str(v1_list[item]))
            v1 += "{0}{1}".format("0"*number_of_0s, v1_list[item])
        v2 = ""
        for item in range(len(v2_list)):
            number_of_0s = longest_code-len(str(v2_list[item]))
            v2 += "{0}{1}".format("0"*number_of_0s, v2_list[item])
        return v1, v2

    # ACTUAL FUNCTIONS START HERE

    def __add__(self, other):
        v1 = self.string_to_0(self)
        v2 = self.string_to_0(other)
        return fv(v1 + v2, data_type="num")

    def __sub__(self, other):
        v1 = self.string_to_0(self)
        v2 = self.string_to_0(other)
        return fv(v1 - v2, data_type="num")

    def __mul__(self, other):
        v1 = self.string_to_0(self)
        v2 = self.string_to_0(other)
        return fv(v1 * v2, data_type="num")

    def __truediv__(self, other):
        v1 = self.string_to_0(self)
        v2 = self.string_to_0(other)
        return fv(v1 / v2, data_type="num")

    def __mod__(self, other):
        v1 = self.string_to_0(self)
        v2 = self.string_to_0(other)
        return fv(v1 % v2, data_type="num")

    def __gt__(self, other):
        t1 = self.value_type(self)
        t2 = self.value_type(other)
        if t1 == "str" and t2 == "str":
            v1, v2 = self.compare_char_values(other)
        elif t1 == "str":
            return True
        elif t2 == "str":
            return False
        elif t1 in ["int", "float"] and t2 in ["int", "float"]:
            v1 = self.value
            v2 = other.value
        result = v1 > v2
        str_result = str(result).lower()
        return [result, fv(str_result, data_type="str")]

    def __lt__(self, other):
        t1 = self.value_type(self)
        t2 = self.value_type(other)
        if t1 == "str" and t2 == "str":
            v1, v2 = self.compare_char_values(other)
        elif t1 == "str":
            return False
        elif t2 == "str":
            return True
        elif t1 in ["int", "float"] and t2 in ["int", "float"]:
            v1 = self.value
            v2 = other.value
        result = v1 < v2
        str_result = str(result).lower()
        return [result, fv(str_result, data_type="str")]

    def __eq__(self, other):
        v1 = self.convert_to_type(self)
        v2 = self.convert_to_type(other)
        result = v1 == v2
        str_result = str(result).lower()
        return [result, fv(str_result, data_type="str")]

    def join(self, other):
        v1 = self.value
        v2 = other.value
        return fv(v1 + v2, data_type="str")

    def letter(self, index):
        try:
            return self.value[index]
        except IndexError:
            return fv("", data_type="str")

    def contains(self, other):
        result = str(other.value in self.value).lower()
        return fv(result, data_type="str")

    def len(self):
        result = len(self.value)
        return fv(result, data_type="num")

    def round(self):
        result = round(self.string_to_0(self))
        return fv(result, data_type="num")

    def abs(self):
        result = abs(self.string_to_0(self))
        return fv(result, data_type="num")

    def floor(self):
        result = math.floor(self.string_to_0(self))
        return fv(result, data_type="num")

    def ceil(self):
        result = math.ceil(self.string_to_0(self))
        return fv(result, data_type="num")

    def sqrt(self):
        result = (self.string_to_0(self))**0.5
        return fv(result, data_type="num")

    def sin(self):
        result = math.sin(math.radians(self.string_to_0(self)))
        return fv(result, data_type="num")

    def cos(self):
        result = math.cos(math.radians(self.string_to_0(self)))
        return fv(result, data_type="num")

    def tan(self):
        result = math.tan(math.radians(self.string_to_0(self)))
        return fv(result, data_type="num")

    def asin(self):
        result = math.asin(math.radians(self.string_to_0(self)))
        return fv(result, data_type="num")

    def acos(self):
        result = math.acos(math.radians(self.string_to_0(self)))
        return fv(result, data_type="num")

    def atan(self):
        result = math.atan(math.radians(self.string_to_0(self)))
        return fv(result, data_type="num")

    def nl(self):
        result = math.log(self.string_to_0(self))
        return fv(result, data_type="num")

    def log(self):
        result = math.log10(self.string_to_0(self))
        return fv(result, data_type="num")

    def e2x(self):
        result = math.exp(self.string_to_0(self))
        return fv(result, data_type="num")

    def ten2x(self):
        result = 10**(self.string_to_0(self))
        return fv(result, data_type="num")

    # not built in

    def neg(self):
        return fv(-(self.string_to_0(self)))

