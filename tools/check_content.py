"""Validate crawlable content, index coverage and local links in the built site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from xml.etree import ElementTree

SITE = Path(__file__).resolve().parents[1] / 'dist'
ORIGIN = 'https://howtofishgames.com'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.canonical = []
        self.h1 = 0
        self.noindex = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.noindex = 'noindex' in attrs.get('content', '')
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('script', 'img') and 'src' in attrs:
            self.links.append(attrs['src'])
        if tag == 'img':
            assert attrs.get('alt'), 'Image requires alternative text'
            assert attrs.get('width') and attrs.get('height'), 'Image requires dimensions'

pages = {('/' if p == SITE/'index.html' else '/' + p.parent.relative_to(SITE).as_posix() + '/'): p for p in SITE.rglob('index.html')}
game = set(pages) - {'/about/', '/contact/', '/privacy/'}
assert len(game) == 25, f'Expected 25 game pages, got {len(game)}'
xml = ElementTree.parse(SITE/'sitemap.xml')
urls = {x.text for x in xml.findall('.//{*}loc')}
assert urls == {ORIGIN + path for path in pages}, 'Sitemap and indexable pages differ'
for path, file in pages.items():
    parsed = Page(file.read_text())
    assert parsed.h1 == 1, (path, 'exactly one H1 required')
    assert parsed.canonical == [ORIGIN + path], (path, 'canonical mismatch')
    assert not parsed.noindex, (path, 'unexpected noindex')
    for href in parsed.links:
        url = urlparse(urljoin(ORIGIN + path, href))
        if url.netloc != 'howtofishgames.com':
            continue
        local = SITE / unquote(url.path).lstrip('/')
        if url.path.endswith('/'):
            local /= 'index.html'
        assert local.is_file(), (path, 'broken local link', href)
index = Page(pages['/fish-list/'].read_text())
covered = {urlparse(urljoin(ORIGIN+'/fish-list/', h)).path for h in index.links}
assert game - {'/fish-list/'} <= covered, 'Game pages missing from searchable index or navigation'
print(f'PASS: {len(game)} game pages; {len(urls)} sitemap URLs; canonicals, H1s, links and index coverage')
