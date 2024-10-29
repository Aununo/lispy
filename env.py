from utils import *
from dataclasses import dataclass

global_env = {
    "+": builtin_add,
    "-": builtin_subtract,
    "*": builtin_multiply,
    "/": builtin_divide,
    "=": builtin_eq,

    "print": builtin_print_value,
    "read": builtin_read_value,

    "<": builtin_less_than,

    "list": builtin_list,
    "len": builtin_len,
    "get": builtin_get
}


def new_env(parent_env, params, args):
    env = dict(zip(params, args))
    env[":parent"] = parent_env
    return env


def get_var(key, env):
    if key in env:
        return env[key]
    elif ":parent" in env:
        return get_var(key, env[":parent"])
    else:
        raise KeyError(f"{key} not found in env: {env}")


@dataclass
class Function:
    params: list
    body: list
    env: dict

