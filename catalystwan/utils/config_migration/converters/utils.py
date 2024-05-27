import re

NEGATIVE_VARIABLE_REGEX = re.compile(r"[^.\/\[\]a-zA-Z0-9_-]")


def convert_varname(orig: str) -> str:
    return NEGATIVE_VARIABLE_REGEX.sub("_", orig)
