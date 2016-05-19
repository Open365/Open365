import urllib.parse as urlparse


def https2git(url):
    u = urlparse.urlsplit(url)
    parts = ['git@', u.hostname, ':', u.path.strip('/')]
    return ''.join(parts)
