import re


def is_wiki_page(link_html, url_base):
    return url_base in link_html

def is_same_page(link_html, actual_url):
    return (actual_url + "#") in link_html

def is_in_brackets(link_html, all_html):
    in_brackets = re.findall(r'\((.*?)\)', all_html)
    if any(link_html in i for i in in_brackets):
        return True
    return False

def is_italic(link_html, all_html):
    italic = re.findall(r'<i>(.*?)</i>', all_html)
    if any(link_html in i for i in italic):
        return True
    return False

def is_not_ogg_file(link):
    return '.ogg' not in link

def is_not_help(link):
    return 'Hilfe' not in link

def get_href(link):
    return re.search(r'href="([^"].*?)"', link).group(0).split('"')[1]

def normalize(link_list, all_html):
    link_name_base = 'silizium_link_'
    link_dict = {}

    for index, link_html in enumerate(link_list):
        link_name = link_name_base + str(index)
        link_dict[link_name] = link_html
        all_html = all_html.replace(link_html, link_name, 1)
    return link_dict, all_html
