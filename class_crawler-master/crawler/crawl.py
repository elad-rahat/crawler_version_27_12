import dataclasses
import collections
import re


@dataclasses.dataclass
class _Link:
    url: str
    depth: int

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url

class Crawl:
    def __init__(self, root_url, max_depth, ingore_regex,  *, find_urls):
        self._find_urls = find_urls
        self._seen = set()
        self._result = collections.defaultdict(list)
        self._max_depth = max_depth
        self.ingore_regex = str(ingore_regex)
        root_link = _Link(root_url, depth=0)
        self._go(root_link)

    def _go(self, root_link):
        self._result[0] = [root_link]
        self._to_explore = [root_link]
        while len(self._to_explore) > 0:
            link = self._to_explore.pop(0)
            self._add_links_from(link)

    def _should_skip(self, link):
        if link in self._seen:
            return True
        if not (link.depth < self._max_depth):
            return True
        if re.search(self.ingore_regex, link.url):
            return True

        return False

    def _add_links_from(self, link):
        links = self._find_links(link)
        self._seen.add(link)
        new_links = [link_ for link_ in links if not self._should_skip(link_)]
        if len(new_links) == 0:
            return

        self._result[link.depth + 1] += new_links
        self._to_explore += new_links



    def _find_links(self, link):
        urls = self._find_urls(link.url)
        return [_Link(url, link.depth + 1) for url in urls]


    def web_of_links(self):
        result = []
        for depth in range(len(self._result)):
            links = self._result[depth]
            urls = [link.url for link in links]
            result.append(urls)

        return result
