import crawler.links

def test_no_links():
    HTML1 = """
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Directory listing for /</title>
    </head>
    <body>
    <h1>Directory listing for /</h1>
    <hr>
    <ul>
    </ul>
    <hr>
    </body>
    </html>
    """
    tested = crawler.links.Links(HTML1)
    assert set() == tested.all()

def test_get_all_links_from_page():
    HTML1 = """
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Directory listing for /</title>
    </head>
    <body>
    <h1>Directory listing for /</h1>
    <hr>
    <ul>
    <li><a href="a.txt">a.txt</a></li>
    <li><a href="b.txt">b.txt</a></li>
    <li><a href="one/">one/</a></li>
    <li><a href="three/">three/</a></li>
    <li><a href="two/">two/</a></li>
    </ul>
    <hr>
    </body>
    </html>
    """
    tested = crawler.links.Links(HTML1)
    assert_same_elements(tested.all(), [
                    "a.txt",
                    "b.txt",
                    "one/",
                    "three/",
                    "two/",
            ])

def test_links_from_wikipedia_article():
    HTML = """
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Directory listing for /</title>
    </head>
    <body>
        <a href="#cite_note-IreneTCR-1">
        <a href="//en.wikipedia.org/wiki/Wikipedia:Contact_us">
        <a href="//en.wikipedia.org/wiki/Wikipedia:Contact_us">
        <a rel="nofollow" class="external text" href="http://abclocal.go.com/wpvi/story?section=local&amp;id=3353400">
        <a href="/w/index.php?title=Hurricane_Irene_(2005)&amp;action=edit&amp;section=5" title="Edit section: External links">
        <a href="/wiki/1852_Atlantic_hurricane_season#Hurricane_Five" title="1852 Atlantic hurricane season">
    </body>
    </html>
    """
    tested = crawler.links.Links(HTML)
    EXPECTED = [
        "#cite_note-IreneTCR-1",
        "//en.wikipedia.org/wiki/Wikipedia:Contact_us",
        "http://abclocal.go.com/wpvi/story?section=local&id=3353400",
        "/w/index.php?title=Hurricane_Irene_(2005)&action=edit&section=5",
        "/wiki/1852_Atlantic_hurricane_season#Hurricane_Five",
        ]

    actual = tested.all()
    assert_same_elements(EXPECTED, actual)

def assert_same_elements(a, b):
    assert set(a) == set(b)
