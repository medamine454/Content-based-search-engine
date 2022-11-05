# srcs/streamlit_app/utils.py
from tkinter.tix import AUTO


def index_search(es, index: str, keywords: str, filters: str,
                 from_i: int, size: int) -> dict:
    """
    Args:
        es: Elasticsearch client instance.
        index: Name of the index we are going to use.
        keywords: Search keywords.
        filters: Tag name to filter medium stories.
        from_i: Start index of the results for pagination.
        size: Number of results returned in each search.
    """
    # search query
    body = {

        'query': {

            'fuzzy': {
                'title': {
                    'value': keywords,
                    'fuzziness': 1

                },
            },

        },

    }

    res = es.search(index=index, body=body)
    # sort popular tags

    return res