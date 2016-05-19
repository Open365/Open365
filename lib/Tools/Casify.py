import re


def to_pascal_case(name):
    titles = _get_words(name)
    return "".join([title.title() for title in titles])


def to_dash_case(name):
    titles = _get_words(name)
    return "-".join(titles)


def _get_words(name):
    titles = []
    for match in re.finditer('([A-Z_-]?)([a-z0-9]*)', name):
        # we should skip those matches where both capture groups are empty
        if match.group() == "":
            continue

        word = ""
        if match.group(1).isupper():
            word += match.group(1).lower()
        word += match.group(2)
        titles.append(word)
    return titles
