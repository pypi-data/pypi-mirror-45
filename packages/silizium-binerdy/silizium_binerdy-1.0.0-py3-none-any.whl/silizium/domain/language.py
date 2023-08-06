def get_wiki_url_base(lang):
    url_base = {
        'de': 'https://de.wikipedia.org/wiki/',
        'en': 'https://en.wikipedia.org/wiki/'
    }
    return url_base[lang]


def get_target_url(lang):
    target_url = {
        'de': 'https://de.wikipedia.org/wiki/Philosophie',
        'en': 'https://en.wikipedia.org/wiki/Philosophy'
    }
    return target_url[lang]
