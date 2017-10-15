from gevent import monkey

monkey.patch_all()

import gevent
import gevent.pool

import urllib2
import os
import threading
import optparse

from bs4 import BeautifulSoup
from urlparse import urlparse, urlunparse, urljoin

OUTPUT_DIR = 'output'

visited_links = set()
pending_links = set()
crawlin_links = set()


def download_and_save(url):
    """
    Download one page from the web and save it to OUTPUT_DIR preserving relative path
    :param url: url to download
    :return: string with raw web page content
    """
    request = urllib2.Request(url)

    response = urllib2.urlopen(request)

    page = response.read()

    rel_path = request.get_selector()

    parts = rel_path.split('/')
    output_dir_path = parts[:-1]

    output_dir = os.path.join(OUTPUT_DIR, *output_dir_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(OUTPUT_DIR, *parts), 'w') as output_file:
        output_file.write(page)

    # print('%s - written to disk: %s' % (threading.currentThread(), request.get_full_url()))

    return page


def is_new_link(current, link):
    """
    Is this a link we didn't visit before?
    :param current: current link we're crawling
    :param link: subject link
    :return: true/false
    """
    return \
        link not in visited_links and \
        link not in pending_links and \
        link not in crawlin_links and \
        current != link


def drop_params(url):
    """
    Drop query params and fragment from URL
    """
    return urlunparse(urlparse(url)[:3] + ('', '', ''))


def same_host(url1, url2):
    """
    Are this two URLs point to the same host?
    """
    return urlparse(url1)[1] == urlparse(url2)[1]


def crawl_one(url):
    """
    Crawl one page, i.e. download and collect outgoing links from one web page
    :param url: url to crawl
    :return: None
    """
    page = download_and_save(url)
    soup = BeautifulSoup(page, 'html.parser')

    tags = soup.find_all('a')
    links = [urljoin(url, tag.get('href')) for tag in tags]

    # print('%s - links crawled: %s' % (threading.currentThread(), links))

    new_links = set(
        filter(
            lambda l: same_host(url, l),
            (drop_params(link) for link in links if is_new_link(url, drop_params(link)))
        )
    )

    # print('%s - new links: %s' % (threading.currentThread(), new_links))

    pending_links.update(new_links)

    visited_links.add(url)
    crawlin_links.remove(url)


def crawl(start_url, concurrency_level, visited_link_limit):
    """
    Main crawling function. Uses a pool of greenlets to get the job done
    :param start_url: URL to start crawling from
    :param concurrency_level: number of concurrent downloads
    :param visited_link_limit: maximum number of links to crawl
    :return: None
    """

    print('start crawling from %s' % start_url)
    print('concurrency level: %s, visited link limit: %s' % (concurrency_level, visited_link_limit))

    # init our pending links with start_url
    pending_links.update([start_url])

    pool = gevent.pool.Pool(concurrency_level)

    # limit number of visited links, just for testing purposes
    while len(visited_links) < visited_link_limit and (len(pending_links) > 0 or len(crawlin_links) > 0):
        # if there is nothing more to schedule, then wait for current jobs to complete and try again
        if not pending_links:
            pool.join()
            continue

        link = pending_links.pop()
        crawlin_links.add(link)
        pool.add(gevent.spawn(crawl_one, link))

        # print('%s - current visited: %s' % (threading.currentThread(), visited_links))

    pool.join()

    # print('%s - visited links: %s' % (threading.currentThread(), visited_links))
    # print('%s - pending links: %s' % (threading.currentThread(), pending_links))


if __name__ == '__main__':
    usage = 'usage: %prog [options] <start URL>'

    parser = optparse.OptionParser(usage)
    parser.add_option(
        '-c', '--concurrency',
        action='store', type='int', dest='concurrency', default=6
    )
    parser.add_option(
        '-l', '--limit',
        action='store', type='int', dest='limit', default=100
    )
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error('start URL for crawl was not specified')

    main = gevent.spawn(
        crawl,
        args[0],
        options.concurrency,
        options.limit
    )
    main.start()

    gevent.wait([main])
