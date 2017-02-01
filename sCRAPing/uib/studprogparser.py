from html.parser import HTMLParser
import re


PATTERN_uib_study_data = r'([A-Za-z]+\d+)|(\w+-\w+)'


class StudProgParser(HTMLParser):
    liststarted = False
    divseen = False
    h3aseen = False
    result = {}
    def handle_starttag(self, tag, attrs):
        self.divseen = tag == 'div' or self.divseen
        self.h3aseen = tag == 'h3' or tag == 'a' or self.h3aseen
        self.attrs = dict(attrs)
    def handle_endtag(self, tag):
        self.divseen = self.divseen and tag != 'div'
        self.h3aseen = self.h3aseen and tag != 'h3' and tag != 'a'
    def handle_data(self, data):
        data = data.strip()
        self.liststarted = r'Funnet 212 studieprogram' in data or (self.liststarted and not 'Studietilbud' in data)
        if self.liststarted and self.divseen and self.h3aseen:
            if 'href' in self.attrs:
                self.result[self.key].append((data, r'http://www.uib.no' + self.attrs['href']))
            else:
                self.key = 'P' if 'Profesjonsstudier' in data else data[0]
                self.result[self.key] = []

class StudPageParser(HTMLParser):
    headings = {'studieplassar': '', 'poenggrense': ''}
    key = False
    result = {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'class' in attrs:
            c = attrs['class']
            if tag == 'span' and c in ['study-facts__label', 'study-facts__value']:
                self.key = 'heading'
            elif tag == 'td':
                if c == 'uib-cell-indent-2':
                    self.key = 'subject'
                elif c == 'uib-study-data':
                    self.key = 'uib-study-data'

    def handle_data(self, data):
        data = data.strip().lower()
        if self.key:
            if not self.key in self.result:
                self.result[self.key] = []
            if self.key == 'uib-study-data':
                match = re.match(PATTERN_uib_study_data, data)
                if match:
                    data = (len(self.result['subject'])-1, data)
                else:
                    self.key = None
            if self.key:
                self.key = self.result[self.key].append(data)
    def heading(self):
        i = iter(self.result['heading'])
        self.headings.update(dict(zip(i, i)))
        return self.headings
    def data(self,key):
        if key in self.result:
            return self.result[key]
