from normalizeurl import normalize

def check(url1, url2):
    url1 = normalize(url1)
    url2 = normalize(url2)

    if url1 == url2:
        return True
    else:
        return False
