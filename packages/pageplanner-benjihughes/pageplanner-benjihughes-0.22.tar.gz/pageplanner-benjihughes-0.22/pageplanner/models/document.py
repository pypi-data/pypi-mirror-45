import json


class Document:

    def __init__(self, url, rank=None, selector=None, elements=None, word_count=None,
                 focus_total=0, variant_total=0, variant_keywords=None, focus_keyword=None):

        if elements is None:
            elements = {}

        self.url = url
        self.rank = rank
        self.selector = selector
        self.elements = elements
        self.word_count = word_count
        self.focus_total = focus_total
        self.variant_total = variant_total
        self.focus_keyword = focus_keyword
        self.variant_keywords = variant_keywords

    def set_focus_total(self, value):
        self.focus_total = value
        return self

    def set_variant_total(self, value):
        self.variant_total = value
        return self

    def set_word_count(self, value):
        self.word_count = value
        return self

    def set_elements(self, value):
        self.elements = value
        return self

    def set_variant_keywords(self, value):
        self.variant_keywords = value
        return self

    def set_focus_keyword(self, value):
        self.focus_keyword = value
        return self

    def set_rank(self, value):
        self.rank = value
        return self

    def set_selector(self, value):
        self.selector = value
        return self

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_dict(self):
        return {
            'url': self.url,
            'rank': self.rank,
            'selector': self.selector,
            'focus_keyword': self.focus_keyword,
            'variant_keywords': self.variant_keywords,
            'word_count': self.word_count,
            'focus_total': self.focus_total,
            'variant_total': self.variant_total,
            'elements': self.elements
        }

    def get_focus_count_for_elem(self, selector):
        return self.elements[selector]['focus_keywords']['count']

    def get_variant_count_for_elem(self, selector):
        return self.elements[selector]['variant_keywords']['count']

    def get_element_count_for_elem(self, selector):
        return self.elements[selector]['element_count']

    def get_word_count(self):
        return self.word_count
