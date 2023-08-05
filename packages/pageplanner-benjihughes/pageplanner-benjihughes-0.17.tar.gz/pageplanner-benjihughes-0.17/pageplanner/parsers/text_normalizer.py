from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import sys
import re
import unicodedata


class TextNormalizer:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.punctuation = dict.fromkeys(
            i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P')
        )
        self.merge_acronyms_pattern = re.compile(r'(?:(?<=\.|\s)[A-Z]\.)+')

    @staticmethod
    def convert_pos_to_wordnet(pos):
        pos = pos[0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(pos, wordnet.NOUN)

    def remove_punctuation(self, item):
        return item.translate(self.punctuation)

    def lemmatize_pos_sentence(self, sentence):
        """ Lemmatize every pos tagged word in a sentence """
        return [self.lemmatizer.lemmatize(word[0], TextNormalizer.convert_pos_to_wordnet(word[1]))
                for word in sentence]

    def lowercase(self, item):
        """ Recursively lowercase the first item of any tuple in a nested list """
        if type(item) is str:
            return item.lower()
        if type(item) is tuple:
            return self.lowercase(item[0]), item[1]

        return [self.lowercase(sub) for sub in item]

    def merge_acronyms(self, text):
        acronyms = self.merge_acronyms_pattern.findall(text)
        for a in acronyms:
            text = text.replace(a, a.replace('.', ''))
        return text

    def create_normalized_sentences(self, text):

        text = self.merge_acronyms(text)
        text = self.lowercase(text)

        # De-hyphenate
        text = text.replace('-', ' ')
        text = text.replace('_', ' ')

        sentences = [self.remove_punctuation(sent) for sent in nltk.sent_tokenize(text)]
        words = [nltk.word_tokenize(w) for w in [s for s in sentences]]
        pos_words = [nltk.pos_tag(s) for s in words]
        lemmatized = [self.lemmatize_pos_sentence(sent) for sent in pos_words]

        # Reconstruct sentences from lists of lemmatized words within sentences
        text = [' '.join(words) for words in [sentence for sentence in lemmatized]]

        return text

    def normalize_phrase(self, phrase):
        return ' '.join(self.create_normalized_sentences(phrase))

    def normalize_phrases(self, phrases):
        return [self.normalize_phrase(x) for x in phrases]

    def unique_normalized_list_by_word_count_descending(self, phrase_list):
        normalized = self.normalize_phrases(phrase_list)
        unique = list(set(normalized))
        unique.sort(key=lambda x: len(x.split()), reverse=True)
        return unique
