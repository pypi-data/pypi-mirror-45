# -*- coding: utf-8 -*-
import logging
import urbandictionary
import wikipedia

from wikipedia.wikipedia import WikipediaPage
from .pydictionary import core


class LowerCaseDict(dict):
    def __setitem__(self, key, value):
        return super(LowerCaseDict, self).__setitem__(key, value)

    def update(self, kw):
        new = [(k.lower(), v) for k, v in kw.items()]
        return super(LowerCaseDict, self).update(new)


class DefinitionFinder(object):
    def __init__(self):
        self.dictionary = core.PyDictionary()

    def get_definition_types(self, data=None):
        data = data or self.get_data()
        keys = data.keys()
        types = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'slang']
        matching_types = filter(lambda name: name in types, keys)

        return tuple(matching_types)

    def get_wikipedia_summary(self, term, recursive=True):
        try:
            wikipedia_summary = wikipedia.summary(term)
            yield wikipedia_summary
        except wikipedia.DisambiguationError as e:
            if not recursive:
                for option in e.options:
                    pages = list(self.get_wikipedia_page(term, recursive=False))
                    yield pages[0]
        except Exception:
            logging.error('failed to retrieve wikipedia summary for: %s', term)

    def get_wikipedia_page(self, term, recursive=True):
        try:
            wikipedia_page = wikipedia.page(term)
            yield wikipedia_page
        except wikipedia.DisambiguationError as e:
            if not recursive:
                for option in e.options:
                    pages = list(self.get_wikipedia_page(term, recursive=False))
                    yield pages[0]
        except Exception:
            logging.error('failed to retrieve wikipedia page for: %s', term)

    def get_slangs(self, term):
        # TODO: replace urbandictionary package with custom client to *new* urbandictionary API
        # the urbandictionary package no longer works with urban dictionary API responses
        urban_results = urbandictionary.define(term)
        slangs = list(map(self.extract_dict, urban_results))
        return slangs

    def get_wikipedia_definition(self, term):
        wikipedia_summaries = self.get_wikipedia_summary(term, recursive=True)
        wikipedia_pages = self.get_wikipedia_page(term, recursive=True)

        summaries = list(map(self.extract_wikipedia_dict,
                             wikipedia_summaries))

        pages = list(map(self.extract_wikipedia_dict,
                         wikipedia_pages))

        if not pages and not summaries:
            return {}

        return {
            'summaries': summaries,
            'pages': pages,
        }

    def get_meaning(self, term):
        term = term.lower()
        data = LowerCaseDict()
        data.update(self.dictionary.meaning(term) or {})
        google = self.dictionary.googlemeaning(term)

        data['term'] = term

        if google:
            data['google'] = google

        wikipedia = self.get_wikipedia_definition(term)
        if wikipedia:
            data['wikipedia'] = wikipedia

        data['synonyms'] = self.dictionary.synonym(term)
        # data['slangs'] = self.get_slangs(term)
        data['antonyms'] = self.dictionary.antonym(term)

        data['definition_types'] = self.get_definition_types(data)

        return data

    def extract_dict(self, item):
        data = {}
        data['definition'] = item.definition
        data['word'] = item.word
        data['example'] = item.example
        # data['upvotes'] = item.upvotes
        # data['downvotes'] = item.downvotes
        return data

    def extract_wikipedia_dict(self, item):
        data = {}
        page_attributes = ('title', 'content', 'links', 'images', 'summary', 'sections', 'references', 'url', 'categories')

        if isinstance(item, WikipediaPage):
            for attr in page_attributes:
                try:
                    value = getattr(item, attr, None)
                except (AttributeError, KeyError):
                    value = None
                    logging.error('failed to retrieve "{}" from wikipedia page {}'.format(attr, item))

                if value is not None:
                    data[attr] = value

        return data
