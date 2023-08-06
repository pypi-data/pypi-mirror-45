from collections import Counter, defaultdict
from lxml.html.clean import Cleaner
from pageplanner.parsers.text_normalizer import TextNormalizer
from pageplanner.models.document import Document
from pageplanner.config import PARSER_CONFIG
from bs4 import BeautifulSoup
from requests_html import HTML
import logging

logger = logging.getLogger(__name__)


class HTMLParser:

    def __init__(self, text_normalizer=None):

        # Use the TextNormalizer provided if possible, otherwise instantiate a new one.
        self.normalizer = text_normalizer if text_normalizer is not None else TextNormalizer()

        # The Element config contains instructions on what elements to extract and which text from each
        self.elem_config = PARSER_CONFIG

    def create_document_from_html(self, html, focus, variants=None, rank=None, selector=None):

        # Variants are option, we can use an empty list if not provided.
        if variants is None:
            variants = []

        # Create the document we're going to output.
        url = html.url
        document = Document(url)

        # Convert back to BeautifulSoup because it allows for elements to be decomposed.
        html = BeautifulSoup(html.raw_html, 'lxml')

        # Decompose noscript tags, they duplicate lazyloaded images.
        noscript_tags = html.select('noscript')
        for noscript_tag in noscript_tags:
            noscript_tag.decompose()

        body = self.create_body(html, selector)

        # Back to requests-html
        html = HTML(url=url, html=html.encode())
        body = HTML(url=url, html=body.encode())

        # Set up counters and initially available data.
        elements = {}
        focus_total = 0
        variant_total = 0
        word_count = self.get_word_count(body)

        # Iterate over each selector in the config.
        for selector in self.elem_config.keys():

            # If the elements in the head use the whole html, otherwise the narrowed body only.
            search_space = html if self.elem_config[selector].get('in_head', False) else body

            element_data = self.get_element_data(search_space, selector, focus, variants)

            # Add resulting data to collections.
            elements[selector] = element_data
            focus_total += element_data['focus_keywords']['count']
            variant_total += element_data['variant_keywords']['count']

        # Set all the attributes of the ParsedDocument.
        document \
            .set_word_count(word_count) \
            .set_elements(elements) \
            .set_focus_total(focus_total) \
            .set_variant_total(variant_total) \
            .set_focus_keyword(focus) \
            .set_variant_keywords(variants) \
            .set_rank(rank) \
            .set_selector(selector)

        logger.info('Succesfully parsed document for %s.' % html.url)

        return document

    @staticmethod
    def parent_only_text(elem):
        """
        Returns the text for the current element without the text of child elements.

        :param elem:
        :return string:
        """
        # . = current node, / = root node, ./ = works?!
        parent_only_text = elem.lxml.findtext('./')
        return parent_only_text

    @staticmethod
    def get_word_count(elem):
        """
        Returns the word count of the given element.

        :param elem:
        :return:
        """
        cleaner = Cleaner(style=True)
        cleaned = cleaner.clean_html(elem.lxml)
        return len(cleaned.text_content().split(' '))

    @staticmethod
    def get_elements(html, selector):
        """
        Returns all elements found matching the given selector.

        :param html:
        :param selector:
        :return:
        """
        return html.find(selector)

    def get_element_data(self, html, selector, focus, variants=None):
        """
        Takes a CSS selector and keywords, returns a dict containing the counts and occurrences for
        each keyword type.

        Element name and text extraction is done according to the element config.

        :param html:
        :param selector:
        :param focus:
        :param variants:
        :return:
        """
        element = {
            "element_name": self.elem_config[selector].get('name', selector),
            "element_count": 0,
            "focus_keywords": {
                "count": 0,
                "occurrences": Counter()
            },
            "variant_keywords": {
                "count": 0,
                "occurrences": Counter()
            }
        }

        # Grab elements matching this selector
        elements = self.get_elements(html, selector)
        element_count = len(elements)
        element["element_count"] = element_count

        # No elements? We're done, return the element as is.
        if element_count == 0:
            return element

        # Get the config that describes how we extract text from this type of elements.
        text_config = self.elem_config[selector].get('text_config', None)

        # False value for config means no text extraction, so we can return with empty counts.
        if text_config is False:
            return element

        # Loop over each of the matching elements.
        for el in elements:

            # Returns a list of normalized sentences.
            text = self.get_element_text_as_sentences(el, text_config)

            for sentence in text:

                # Each sentence becomes split into a [word, 0] format to allow for marking
                # when a word has previously been part of a match. This is to avoid double-matching keywords.
                tokenized_sentence = [[word, 0] for word in sentence.split(' ')]

                # Returns the count (int), occurrences (dict), and updated tokenized sentence with matched words
                # marked as [word, 1] rather than the original [word, 0]
                focus_count, focus_occurrences, tokenized_sentence = self.find_keyword_occurrences_in_text(focus,
                                                                                                           tokenized_sentence)
                element['focus_keywords']["count"] += focus_count
                element['focus_keywords']["occurrences"] += Counter(focus_occurrences)

                # Same again but for variants, this time passing in the tokenized sentence that has the focus keywords
                # marked so they can't be matched again.
                variant_count, variant_occurrences, tokenized_sentence = self.find_keyword_occurrences_in_text(variants,
                                                                                                               tokenized_sentence)

                element['variant_keywords']["count"] += variant_count
                element['variant_keywords']["occurrences"] += Counter(variant_occurrences)

        return element

    @staticmethod
    def find_keyword_occurrences_in_text(keywords, tokenized_sentence):
        """
        Searches a tokenized sentence to for each of the given keywords.
        When a keyword is found, the matching words of the tokenized sentence are marked as previously matched,
        meaning they won't be eligible for the next keyword search, removing duplicate matches in overlapping
        phrases.

        :param keywords:
        :param tokenized_sentence:
        :return:
        """
        # Set up some counters.
        count = 0
        occurrences = defaultdict(int)

        # If we were passed a single keyword, make it a list anyway.
        if type(keywords) == str:
            keywords = [keywords]

        # For each of the provided keywords.
        for keyword in keywords:

            # Split our keyword up, so each word is an array with a marker (initially 0).
            split_keyword = [[word, 0] for word in keyword.split(' ')]

            consecutive = 0

            # Loop over the words in the tokenized sentence.
            for i in range(len(tokenized_sentence)):

                # Does this word match the i-th consecutive word of the keyword and have a 0 for the found bit?
                if tokenized_sentence[i][0] == split_keyword[consecutive][0] and tokenized_sentence[i][1] == 0:
                    consecutive += 1
                else:
                    consecutive = 0

                # If the amount of consecutive matches is equal to the length of words in the keyword,
                # we've found the keyword!
                if consecutive == len(split_keyword):
                    count += 1
                    occurrences[keyword] += 1

                    # Reverse back over the items we've matched and set the found bit to 1.
                    for y in range(i, i - (len(split_keyword)), -1):
                        tokenized_sentence[y][1] = 1

                    # Reset to search for more in the string.
                    consecutive = 0

        return count, occurrences, tokenized_sentence

    def get_element_text_as_sentences(self, el, text_config):
        """
        Returns the normalized element text in sentences according to the
        text config provided.

        :param el:
        :param text_config:
        :return:
        """
        text = None

        # Default to get_text()
        if text_config is None:
            text = el.full_text
        else:

            # Manage the different types of text accessors that can be described in the config.
            accessor_type = text_config['accessor_type']

            if accessor_type == 'default':
                text = el.full_text

            elif accessor_type == 'attribute':
                attribute_name = text_config['accessor_attribute_name']
                text = el.attrs.get(attribute_name, '')

            elif accessor_type == 'parent_only':
                text = self.parent_only_text(el)

        return self.normalizer.create_normalized_sentences(str(text))

    @staticmethod
    def create_body(soup, selector):
        """
        Marrows down to any selector given in the constructor.

        :param selector:
        :param soup:
        :return BeautifulSoup:
        """

        # Narrow down the soup to the content found by the selector if provided.
        if selector is not None:
            selected_elem = soup.select_one(selector)
            if selected_elem is not None:
                soup = selected_elem
                logger.info('Narrowed page to selector: %s' % selector)

            else:
                logger.warning('Selector %s returned None while narrowing. Using whole page.' % selector)

        return soup