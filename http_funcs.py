from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def get_page(url):
    """
    Get an HTML page
    """
    try:
        with closing(get(url, stream=True)) as res:
            if is_good_response(res):
                return res.content
    except RequestException as e:
        log_error(e)

def is_good_response(res):
    """
    Return True if the response is HTML, else False
    """
    content_type = res.headers['Content-Type'].lower()
    return (res.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)