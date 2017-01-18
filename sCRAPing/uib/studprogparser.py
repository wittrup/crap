from html.parser import HTMLParser


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
                self.result[self.key].append((data, self.attrs['href']))
            else:
                self.key = 'P' if 'Profesjonsstudier' in data else data[0]
                self.result[self.key] = []