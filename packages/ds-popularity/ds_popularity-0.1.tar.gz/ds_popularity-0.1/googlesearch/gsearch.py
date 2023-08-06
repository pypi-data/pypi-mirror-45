#pip install --upgrade google-api-python-client
from googleapiclient.discovery import build
#pip install pandas
my_api_key = "AIzaSyDC4MZhBR3QcQrZbM-juMYgVWraVs02FAk"
my_cse_id = "006012280939763386453:hlayczalnw8"


def _search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def search(search_term, **kwargs):
    return _search(search_term,api_key=my_api_key, cse_id=my_cse_id, **kwargs)


def result_count(result):
    return result['queries']['request'][0]['totalResults']


def search_term(result):
    return result['queries']['request'][0]['searchTerms']

