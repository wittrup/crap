from html.parser import HTMLParser


class Parser(HTMLParser):
    nais=False
    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.nais = True
    def handle_data(self, data):
        if self.nais:
            self.data = data
    def handle_endtag(self, tag):
        self.nais = False

if __name__ == '__main__':
    fname = "ignore/7.html"
    parse = Parser()
    for chunk in open(fname):
        parse.feed(chunk)
    print(parse.data)
