import json
from pageplanner.config import PARSER_CONFIG
from pageplanner.scraper.scraper import Scraper
from pageplanner.parsers.html_parser import HTMLParser
from pageplanner.parsers.text_normalizer import TextNormalizer


def get_document(url, focus, variants=None, selector=None, rank=None, parser=None, normalizer=None, kws_normalized=False, as_dict=False):
    """
    Scrape and parse a single url into a document.

    :param selector:
    :param url:
    :param focus:
    :param variants:
    :param rank:
    :param parser:
    :param normalizer:
    :param kws_normalized:
    :param as_dict:
    :return:
    """
    # Prepare the response.
    response = {"success": False}

    # If there's no URL we can't scrape anything, so return a failure.
    if url is None:
        response['reason'] = 'No URL supplied.'
        return response if as_dict else json.dumps(response)

    # Set the url in the response for further errors.
    response['url'] = url

    # Set the configured elements.
    response['configured_elements'] = list(PARSER_CONFIG.keys())

    s = Scraper()

    # We might be provided these already instantiated.
    n = normalizer if normalizer is not None else TextNormalizer()
    p = parser if parser is not None else HTMLParser(text_normalizer=n)

    # Scrape the page.
    try:
        html = s.scrape(url)
    except Exception as e:

        # If we fail, set the reason and return in the appropriate format.
        response['reason'] = str(e)
        return response if as_dict else json.dumps(response)

    # Normalize the keywords provided if they haven't been already
    if kws_normalized:
        normalized_focus_keyword = focus
        normalized_variant_keywords = variants
    else:
        normalized_focus_keyword = n.normalize_phrase(focus)

        if variants is not None:
            normalized_variant_keywords = n.unique_normalized_list_by_word_count_descending(variants)
        else:
            normalized_variant_keywords = None

    # Create the document
    try:
        document = p.create_document_from_html(html, normalized_focus_keyword,
                                               normalized_variant_keywords,
                                               rank=rank,
                                               selector=selector)
    except Exception as e:

        # If we fail, set the reason and return in the appropriate format.
        response['reason'] = str(e)
        return response if as_dict else json.dumps(response)

    response["success"] = True
    response["result"] = document.get_dict()

    return response if as_dict else json.dumps(response)


def get_documents(pages, focus, variants):
    """
    Runs get_document multiple times without re-instantiating classes.

    Returns a json object where 'results' contains an array of get_document response objects.

    :param pages:
    :param focus:
    :param variants:
    :return:
    """
    # Instantiate the classes required to retrieve documents.
    n = TextNormalizer()
    p = HTMLParser(n)

    # Normalize the keywords provided
    normalized_focus_keyword = n.normalize_phrase(focus)
    normalized_variant_keywords = n.unique_normalized_list_by_word_count_descending(variants)

    documents = []

    for page in pages:

        url = page.get('url', None)
        rank = page.get('rank', None)
        selector = page.get('selector', None)

        # Create a document for this url, receiving the return as a dict.
        document = get_document(url,
                                normalized_focus_keyword,
                                normalized_variant_keywords,
                                parser=p, normalizer=n, kws_normalized=True, as_dict=True, rank=rank, selector=selector
                                )
        documents.append(document)

    # Create and return our response
    response = {'success': True, 'result': documents}
    return json.dumps(response)
