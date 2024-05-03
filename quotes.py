import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

QUOTES_URL = "https://quotes.toscrape.com/"


def get_all_quotes() -> dict[str, int]:
    index = {}
    curr_page = 1
    while True:
        quotes = _parse_quotes_from_page(curr_page)
        if len(quotes) > 0:
            index = _quote_to_index(index, quotes, curr_page)
        else:
            break
        curr_page += 1

    return index


def _parse_quotes_from_page(page: int) -> str:
    res = ""
    curr = _get_quotes_html(page)
    quotes_els = curr.find_all("div", class_="quote")
    for q_el in quotes_els:
        q_text = q_el.find("span", class_="text")
        q_author = q_el.find("small", class_="author")
        q_tags = q_el.find_all("a", class_="tag")

        full_quote = _to_full_quote(q_text, q_author, q_tags)
        res += full_quote

    return res


def _quote_to_index(
    index: dict[str, int],
    text: str,
    page: int
) -> dict[str, int]:
    for word in text.split():
        word = word.lower()
        if word not in index:
            index[word] = []
        if page not in index[word]:
            index[word].append(page)

    return index


def _to_full_quote(q_text: Tag, q_author: Tag, q_tags: ResultSet) -> str:
    text = _clean_tag(q_text)
    author = _clean_tag(q_author)
    tags = _clean_result_set(q_tags)

    return f"{text} {author} {tags}\n"


def _get_quotes_html(page: int = 1) -> BeautifulSoup:
    uri = f"{QUOTES_URL}page/{page}"
    print(f"Scraping {uri}...")
    page = requests.get(uri)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def _clean_tag(tag: Tag) -> str:
    return tag.text.strip()


def _clean_result_set(result_set: ResultSet) -> list[str]:
    for i in range(len(result_set)):
        result_set[i] = result_set[i].text.strip()
    return "".join(result_set)
