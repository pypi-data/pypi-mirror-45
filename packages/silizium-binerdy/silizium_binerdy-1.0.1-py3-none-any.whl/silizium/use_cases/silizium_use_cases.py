from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from silizium.domain.language import get_wiki_url_base, get_target_url
from silizium.domain.wiki_parser import *


def load_browser(headless):
    options = Options()
    options.headless = True if headless else False
    return webdriver.Firefox(options=options)

def get_full_link(link, lang):
    return get_wiki_url_base(lang) + get_href(link).replace('/wiki/', '')

def get_page_content(browser):
    return browser.find_elements_by_css_selector('.mw-parser-output > p, .mw-parser-output > ul')

def get_links_html(content):
    return [link.get_attribute('outerHTML') for link in content.find_elements_by_css_selector('a')]

def extract_valid_link(link_dict, normalized_html, actual_url):
    for link_name in link_dict:
        link = link_dict[link_name]
        link_target = get_href(link)
        if is_wiki_page(link_target, 'wiki/') and not is_same_page(link_target, actual_url):
            if not is_in_brackets(link_name, normalized_html) and not is_italic(link_name, normalized_html):
                if is_not_ogg_file(link_target) and is_not_help(link_target):
                    return link
    return None

def get_first_valid_link(contents, current_url):
    for content in contents:
        html = content.get_attribute('innerHTML')
        links = get_links_html(content)
        link_dict, normalized_html = normalize(links, html)
        valid_link = extract_valid_link(link_dict, normalized_html, current_url)
        if valid_link is not None:
            return valid_link

def philosophy_game(word, limit, headless, lang='de'):
    browser = load_browser(headless)
    link = get_wiki_url_base(lang) + word
    browser.get(link)
    for i in range(limit):
        try:
            if link == get_target_url('de'):
                yield link, i+1
                browser.quit()
                break
            else:
                yield link, i+1
            contents = get_page_content(browser)
            link = get_first_valid_link(contents, browser.current_url)
            link = get_full_link(link, lang)
            browser.get(link)
        except Exception as e:
            browser.quit()
            break
    browser.quit()
