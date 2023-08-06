import math

def typ(val):
    try:
        if int(float(val)) == float(val):
            return "int"
        else:
            return "float"
    except ValueError:
        return "str"

def c2t(val): # convert to type
    if typ(val) == 'str':
        return str(val)
    elif typ(val) == 'float':
        return float(val)
    elif typ(val) == 'int':
        return int(val)


def s20(val): # string to 0
    if typ(val) == "str":
        return 0
    else:
        return c2t(val)

# def typ(value):
#     return(type(value).__name__)

def iof(val): # int or float
    if float(int(val)) == float(val): # then num is int
        return int(val)
    else:
        return float(val)

def compare_char_values(val1, val2):
    longest_code = 0 
    val1_list = []
    for index in range(len(val1)):
        char = val1[index]
        char_code = ord(char)
        longest_code = max(longest_code, len(str(char_code)))
        val1_list.append(char_code)
    val2_list = []
    for index in range(len(val2)):
        char = val2[index]
        char_code = ord(char)
        longest_code = max(longest_code, len(str(char_code)))
        val2_list.append(char_code)
    val1 = ""
    for item in range(len(val1_list)):
        number_of_0s = longest_code-len(str(v1_list[item]))
        v1 += "{0}{1}".format("0"*number_of_0s, v1_list[item])
    val2 = ""
    for item in range(len(val2_list)):
        number_of_0s = longest_code-len(str(v2_list[item]))
        v2 += "{0}{1}".format("0"*number_of_0s, v2_list[item])
    return int(v1), int(v2)

# ACTUAL FUNCTIONS START HERE

def str(val):
    if typ(val) == "bool":
        return str(val).lower()
    else:
        return str(val)

def add(val1, val2):
    val1 = s20(val1)
    val2 = s20(val2)
    return val1 + val2

def sub(val1, val2):
    val1 = s20(val1)
    val2 = s20(val2)
    return val1 - val2

def mul(val1, val2):
    val1 = s20(val1)
    val2 = s20(val2)
    return val1 * val2

def div(val1, val2):
    val1 = s20(val1)
    val2 = s20(val2)
    return val1 / val2

def mod(val1, val2):
    val1 = s20(val1)
    val2 = s20(val2)
    return val1 % val2

def gt(val1, val2):
    type1 = typ(val1)
    type2 = typ(val2)
    if type1 == "str" and type2 == "str":
        val1, val2 = compare_char_values(val1, val2)
    elif type1 == "str":
        return True
    elif type2 == "str":
        return False
    result = v1 > v2
    return result

def gt(val1, val2):
    type1 = typ(val1)
    type2 = typ(val2)
    if type1 == "str" and type2 == "str":
        val1, val2 = compare_char_values(val1, val2)
    elif type1 == "str":
        return False
    elif type2 == "str":
        return True
    result = v1 > v2
    return result

def eq(val1, val2):
    result = c2t(val1) == c2t(val2)
    return result

def join(val1, val2):
    result = "{0}{1}".format(val1, val2)
    return result

def letter(val, index):
    result = str(val)[index]
    return result

def contains(val1, val2):
    result = str(val1) in str(val2)
    return result

def len(val):
    result = len(str(val))
    return result

def round(val):
    result = round(s20(val))
    return result

def abs(val):
    result = abs(s20(val))
    return result

def floor(val):
    result = int(s20(val))
    return result

def ceil(val):
    result = math.ceil(s20(val))
    return result

def sqrt(val):
    result = (s20(val))**0.5
    return result

def sin(val):
    result = math.sin(math.radians(s20(val)))
    return result

def cos(val):
    result = math.cos(math.radians(s20(val)))
    return result

def tan(val):
    result = math.tan(math.radians(s20(val)))
    return result

def asin(val):
    result = math.asin(math.radians(s20(val)))
    return result

def acos(val):
    result = math.acos(math.radians(s20(val)))
    return result

def atan(val):
    result = math.atan(math.radians(s20(val)))
    return result

def nl(val):
    result = math.log(s20(val))
    return result

def log(val):
    result = math.log10(s20(val))
    return result

def e2x(val):
    result = math.exp(s20(val))
    return result

def ten2x(val):
    result = 10**(s20(val))
    return result