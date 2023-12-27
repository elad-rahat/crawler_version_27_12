import crawler.crawl
from testix import *
import re

def test_no_links__return_only_root_url():
    with Scenario() as s:
        s.find_links('root') >> []

        tested = crawler.crawl.Crawl('root', 1, ingore_regex=Fake('ingore_regex'),  find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
           ]

def test_depth_2_link_tree():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> []
        s.find_links('link2') >> []

        tested = crawler.crawl.Crawl('root', 2, ingore_regex=Fake('ingore_regex'), find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
           ]

def test_edge_case__depth_2_loop():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> []
        s.find_links('link2') >> ['root']

        tested = crawler.crawl.Crawl('root', 2, ingore_regex=Fake('ingore_regex'), find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
           ]

def test_depth_4_link_tree():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> ['link1.1', 'link1.2']
        s.find_links('link2') >> ['link2.1']
        s.find_links('link1.1') >> []
        s.find_links('link1.2') >> ['link1.2.1']
        s.find_links('link2.1') >> []
        s.find_links('link1.2.1') >> []

        tested = crawler.crawl.Crawl('root', 4, ingore_regex=Fake('ingore_regex'), find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
                ['link1.1', 'link1.2', 'link2.1'],
                ['link1.2.1',]
           ]

def test_edge_case__depth_3_but_max_depth_is_2():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> []
        s.find_links('link2') >> ['link2.1']

        tested = crawler.crawl.Crawl('root', max_depth=2, ingore_regex=Fake('ingore_regex'), find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
           ]

def test_depth_4_link_tree_but_depth_is_3():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> ['link1.1', 'link1.2']
        s.find_links('link2') >> ['link2.1']
        s.find_links('link1.1') >> []
        s.find_links('link1.2') >> ['link1.2.1']
        s.find_links('link2.1') >> []

        tested = crawler.crawl.Crawl('root', max_depth=3, ingore_regex=Fake('ingore_regex'), find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
                ['link1.1', 'link1.2', 'link2.1'],
           ]


def test_depth_2_link_tree_with_ingore_regex():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']


        tested = crawler.crawl.Crawl('root', max_depth=2, ingore_regex="^l", find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
           ]

def test_ignore_regex_never_matches_any_link__all_links_visited():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> []
        s.find_links('link2') >> []

        tested = crawler.crawl.Crawl('root', max_depth=100, ingore_regex="^n", find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
           ]



def test_depth_4_link_tree_with_ingore_regex():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link2') >> ['link2.1']
        s.find_links('link2.1') >> []

        tested = crawler.crawl.Crawl('root', 4, "^link1", find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link2'],
                ['link2.1'],
           ]

def test_depth_4_link_tree_with_ingore_regex_start_link11():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> ['link1.1', 'link1.2']
        s.find_links('link2') >> ['link2.1']
        s.find_links('link1.2') >> ['link1.2.1']
        s.find_links('link2.1') >> []
        s.find_links('link1.2.1') >> []

        tested = crawler.crawl.Crawl('root', 4, "^link1\.1", find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
                ['link1.2', 'link2.1'],
                ['link1.2.1',]
           ]

def test_depth_4_link_tree_with_ingore_regex_mean_nothing():
    with Scenario() as s:
        s.find_links('root') >> ['link1', 'link2']
        s.find_links('link1') >> ['link1.1', 'link1.2']
        s.find_links('link2') >> ['link2.1']
        s.find_links('link1.1') >> []
        s.find_links('link1.2') >> ['link1.2.1']
        s.find_links('link2.1') >> []
        s.find_links('link1.2.1') >> []

        tested = crawler.crawl.Crawl('root', 4, "^s", find_urls=Fake('find_links'))
        assert tested.web_of_links() == [
                ['root'],
                ['link1', 'link2'],
                ['link1.1', 'link1.2', 'link2.1'],
                ['link1.2.1',]
           ]
