from fuzzyfinder import fuzzyfinder
from prompt_toolkit.completion import Completer, Completion
from .packages.completion_engine import suggest_type


class RedisCompleter(Completer):
    keywords = ["keys", "set", "get"]

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        suggestion = suggest_type(document.text, len(document.text_before_cursor))
        if suggestion.type == "keyword":
            corpus = self.keywords
        results = fuzzyfinder(word, corpus)
        return [Completion(x, -len(x)) for x in results]
