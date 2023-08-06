from __future__ import unicode_literals

import re
import unicodedata
from urllib.parse import quote, unquote, urlsplit, urlunsplit

def scrub(string, charset = 'utf-8'):
    string = unquote(string)
    return unicodedata.normalize('NFC', string).encode(charset)

DEFAULTPORT = {
    'ftp': 21,
    'telnet': 23,
    'http': 80,
    'ws': 80,
    'gopher': 70,
    'news': 119,
    'nntp': 119,
    'prospero': 191,
    'https': 443,
    'wss': 443,
    'snews': 563,
    'snntp': 563,
}

def normalize(url, charset = 'utf-8'):
    if url[0] not in ['/', '-'] and ':' not in url[:7]:
        url = 'http://' + url

    url = url.replace('#!', '?_escaped_fragment_=')
    url = re.sub(r'\?utm_source=feedburner.+$', '', url)
    scheme, auth, path, query, fragment = urlsplit(url.strip())
    (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

    scheme = scheme.lower()

    host = host.lower()
    if host and host[-1] == '.':
        host = host[:-1]

    host = host.encode("idna").decode(charset)

    path = quote(scrub(path), "~:/?#[]@!$&'()*+,;=")
    fragment = quote(scrub(fragment), "~")

    query = "&".join(
        sorted(["=".join(
            [quote(scrub(t), "~:/?#[]@!$'()*+,;=")
             for t in q.split("=", 1)]) for q in query.split("&")]))

    if scheme in ["", "http", "https", "ftp", "file"]:
        output, part = [], None
        for part in path.split('/'):
            if part == "":
                if not output:
                    output.append(part)
            elif part == ".":
                pass
            elif part == "..":
                if len(output) > 1:
                    output.pop()
            else:
                output.append(part)
        if part in ["", ".", ".."]:
            output.append("")
        path = '/'.join(output)

    if userinfo in ["@", ":@"]:
        userinfo = ""

    if path == "" and scheme in ["http", "https", "ftp", "file"]:
        path = "/"

    if port and scheme in DEFAULTPORT.keys():
        if port.isdigit():
            port = str(int(port))
            if int(port) == DEFAULTPORT[scheme]:
                port = ''

    auth = (userinfo or "") + host
    if port:
        auth += ":" + port
    if url.endswith("#") and query == "" and fragment == "":
        path += "#"

    return urlunsplit((scheme, auth, path, query, fragment))
