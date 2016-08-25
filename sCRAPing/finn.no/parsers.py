from html.parser import HTMLParser
import glob


class ListParser(HTMLParser):
    nais = False # next data is title
    kode = 0
    finn = {}
    def handle_starttag(self, tag, attrs):
        dattr = dict(attrs)
        if tag == 'div' and 'data-favorite-ad' in dattr:
            self.kode = int(dattr['data-favorite-ad'])
            self.finn[self.kode] = {}
        if tag == 'h2' and 'class' in dattr and dattr['class'] == 't3 truncate pvt man':
            self.nais = True
    def handle_data(self, data):
        dast = data.strip()
        if self.nais:# and dast not in ['Velkommen til m.finn.no', '']:
            self.finn[self.kode]['title'] = dast
            self.nais = False
    def handle_endtag(self, tag):
        self.nais = False
    def __iter__(self):
        return iter(self.finn.items())


NXT_IS_KEY = 1
NXT_IS_VAL = 2
class AdParser(HTMLParser):
    lstkey = ''
    values = {}
    nxt_is = 0 # next is ?
    def handle_starttag(self, tag, attrs):
        dattr = dict(attrs)
        if tag == 'dt' and 'data-automation-id' in dattr and dattr['data-automation-id'] == 'key':
            self.nxt_is = NXT_IS_KEY
        if tag == 'dd' and 'data-automation-id' in dattr and dattr['data-automation-id'] == 'value':
            self.nxt_is = NXT_IS_VAL

    def handle_data(self, data):
        if self.nxt_is == NXT_IS_KEY:
            self.values[data] = ''
            self.lstkey = data.strip().lower()
        elif self.nxt_is == NXT_IS_VAL:
            self.values[self.lstkey] = data.strip()

    def handle_endtag(self, tag):
        self.nxt_is = 0
    def clean(self):
        self.values = dict((k, v) for k, v in self.values.items() if v)
    def __repr__(self):
        return str(self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, item):
        return self.values[item]


if __name__ == '__main__':
    parser = ListParser()
    for fname in glob.glob('favorites/*.html'):
        for chunk in open(fname):
            parser.feed(chunk)

    print('\n'.join(map(str, parser)))

    f = open('parsed.txt', 'w')
    parser = AdParser()
    for chunk in open('ads/71231332.html'):
        parser.feed(chunk)
    parser.clean()

    print(parser)