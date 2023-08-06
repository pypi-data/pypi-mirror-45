from collections import namedtuple

Suggestion = namedtuple("Suggestion", "type")


def suggest_type(command, cursor_pos):
    word_before_cursor = command[:cursor_pos]
    return Suggestion("keyword")
