#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string


def normalize_whitespace(text):
    return string.join(string.split(text), ' ')


class CounterHandler(ContentHandler):

    def __init__(self):
        self.inContent = 0
        self.theContent = ""
        self.news = 1
        self.out = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.link = normalize_whitespace(attrs.get('rdf:about'))
            self.inContent = 1

    def endElement(self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'title' and self.inContent:
            self.out += ("<li><a href=" + self.link + ">" +
                    "Title " + str(self.news) + ": " +
                    self.theContent + "</a></li>\n")
            self.inContent = 0
            self.theContent = ""
            self.news = self.news + 1

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def getBarrapunto():
    BarraParser = make_parser()
    BarraHandler = CounterHandler()
    BarraParser.setContentHandler(BarraHandler)
    BarraParser.parse("http://barrapunto.com/index.rss")
    return BarraHandler.out
