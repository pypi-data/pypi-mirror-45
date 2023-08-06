"""analyze_syntax.py

Attempts to find the most likely cause of a SyntaxError.
"""

# Note: we do not attempt to translate strings here,
# so that we could more easily write targeted unit tests.
# However, note that we have not created
# separate unit tests yet.

import keyword
import tokenize

from .utils import collect_tokens

possible_causes = []


def add_cause(func):
    """A simple decorator that adds a given cause to the list
       of probable causes."""
    possible_causes.append(func)

    def wrapper(*args):
        return func(*args)

    return wrapper


def find_likely_cause(source, linenumber, message, offset):
    """Given some source code as a list of lines, a linenumber
       (starting at 1) indicating where a SyntaxError was detected,
       a message (which follows SyntaxError:) and an offset,
       this attempts to find a probable cause for the Syntax Error.
    """

    offending_line = source[linenumber - 1]
    line = offending_line.rstrip()

    # If Python includes a descriptive enough message, we rely
    # on the information that it provides.
    if message == "can't assign to literal":
        return assign_to_literal(message, line)

    # If not, we guess based on the content of the last line of code
    # Note: we will need to do more than this to catch other types
    # of errors, such as mismatched brackets, etc.
    return analyze_last_line(line)


def assign_to_literal(message, line):
    variable = line.split("=")[0].strip()
    return message + " %s" % variable


def analyze_last_line(line):
    """Analyzes the last line of code as identified by Python as that
       on which the error occurred."""
    tokens = collect_tokens(line)

    if not tokens:
        return "No cause found"

    for possible in possible_causes:
        cause = possible(tokens)
        if cause:
            return cause
    return "No cause found"


# ==================
# IMPORTANT: causes are looked at in the same order as they appear below.
# Changing the order can yield incorrect results
# ==================


@add_cause
def assign_to_a_keyword(tokens):
    """Checks to see if it is of the formm

       keyword = ...
    """
    if len(tokens) < 2:
        return False
    if tokens[0].string not in keyword.kwlist:
        return False

    if tokens[1].string == "=":
        return "Assigning to Python keyword"
    return False


@add_cause
def confused_elif(tokens):
    if tokens[0].string == "elseif":
        return "elif not elseif"

    if tokens[0].string == "else" and len(tokens) > 1 and tokens[1].string == "if":
        return "elif not else if"
    return False


@add_cause
def import_from(tokens):
    """Looks for
            import X from Y
       instead of
            from Y import X
    """
    if len(tokens) < 4:
        return
    first = tokens[0].string
    if first != "import":
        return
    third = tokens[2].string
    if third == "from":
        return "import X from Y"
    return False


@add_cause
def missing_colon(tokens):
    # needs unit tests:
    if len(tokens) < 2:
        return False

    name = tokens[0].string
    if name in [
        "class",
        "def",
        "elif",
        "else",
        "except",
        "finally",
        "if",
        "for",
        "while",
        "try",
    ]:
        last = tokens[-1]
        if last.string != ":":
            return "%s missing colon" % name
    return False


@add_cause
def malformed_def(tokens):
    # need at least five tokens: def name ( ) :
    if tokens[0].string != "def":
        return False

    if (
        len(tokens) < 5
        or tokens[1].type != tokenize.NAME
        or tokens[2].string != "("
        or tokens[-2].string != ")"
        or tokens[-1].string != ":"
    ):
        return "malformed def"

    return False
