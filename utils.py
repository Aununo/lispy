def builtin_add(*args):
    result = 0
    for n in args:
        result += n
    return result

def builtin_subtract(*args):
    [result, *nums] = args
    for n in nums:
        result -= n
    return result

def builtin_multiply(*args):
    [result, *nums] = args
    for n in nums:
        result *= n
    return result

def builtin_divide(a, b):
    return int(a / b)

def builtin_eq(a, b):
    if a == b:
        return ":true"
    return ":false"

def builtin_print_value(*args):
    result = ""
    for arg in args:
        if isinstance(arg, str) and arg.startswith('"') and arg.endswith('"'):
            result += bytes(arg[1:-1], "utf-8").decode("unicode_escape") + " "
        else:
            result += str(arg) + " "
    print(result.strip())


def builtin_read_value():
    return input("user> ")


def builtin_less_than(a, b):
    return ":true" if a < b else ":false"


def builtin_list(*args):
    return list(args)

def builtin_len(lst):
    return len(lst)

def builtin_get(lst, index):
    return lst[index]