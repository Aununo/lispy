import re
from env import *

def lex(s):
    s = re.sub(r'//.*', '', s)  
    s = re.sub(r'/\*[\s\S]*?\*/', '', s) 
    return re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^() \n]+', s)
# s = (+ 1 2), lex(s) = ['+', '1', '2']


def parse(tokens):
    token = tokens.pop(0)
    if token == "(":
        result = []
        while len(tokens):
            if tokens[0] == ")":
                tokens.pop(0)
                return result
            else:
                result.append(parse(tokens))
    elif token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
        return int(token)
    elif re.match(r"^-?\d+\.\d+$", token):
        return float(token)
    else:
        return token


def Eval(node, env=global_env):
    if type(node) is list:
        [fn, *args] = node
        match fn:
            case "def":
                [key, value] = args
                value = Eval(value, env)
                env[key] = value
                return value
            case "if":
                [cond, conseq, alter] = args
                cond = Eval(cond, env)
                if cond == ":true":
                    return Eval(conseq, env)
                else:
                    return Eval(alter, env)
            case "while":
                cond, body = args
                result = ":nil"
                while Eval(cond, env) == ":true":
                    result = Eval(body, env)
                return result
            case "for":
                init, cond, step, body = args
                Eval(init, env)
                result = ":nil"
                while Eval(cond, env) == ":true":
                    result = Eval(body, env)
                    Eval(step, env)
                return result
            case "do":
                result = ":nil"
                for a in args:
                    result = Eval(a, env)
                return result
            case "fn":
                [params, body] = args
                return Function(params, body, env)
            case _:
                args = [Eval(a, env) for a in args]
                fn = Eval(node[0], env)
                if type(fn) is Function:
                    fn_env = new_env(fn.env, fn.params, args)
                    return Eval(fn.body, fn_env)
                else:
                    return fn(*args)
    elif type(node) in (int, float):
        return node
    elif type(node) is str and node[0] == ":":
        return node
    elif node.startswith('"') and node.endswith('"'):
        return node
    else:
        return get_var(node, env)


def run(s):
    tokens = lex(s)
    tree = parse(tokens)
    return Eval(tree)


def test(s, expected):
    actual = run(s)
    if actual == expected:
        print(f"[PASS] {s}")
    else:
        print(f"[FAIL] {s} -> expected={expected}, got={actual}")


if __name__ == "__main__":
    with open("./test/main.lsy", "r") as reader:
        run(reader.read())