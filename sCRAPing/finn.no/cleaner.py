shorts = {'administrasjon': 'adm'}
remove = {' -': ',', 'European Organization for Nuclear Research': ''}


def shortenword(word):
    wolo = word.lower()
    return shorts[wolo] if wolo in shorts else word


def uniquewords(line, shorten=False):
    trim = ''
    for word in line.split():
        if word not in trim:
            trim += ' ' + shortenword(word) if shorten else word
    for key,val in remove.items():
        trim = trim.replace(key, val)
    return trim[1::]




