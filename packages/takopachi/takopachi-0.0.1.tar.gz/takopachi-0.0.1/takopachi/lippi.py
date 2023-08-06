#!/usr/bin/env python -*- coding: utf-8 -*-

""" Parses http://lippli.jp """

import json
import os
from itertools import chain
from collections import defaultdict

from lazyme import deduplicate
from lazyme import find_files

from tqdm import tqdm
from bs4 import BeautifulSoup


def get_page(url):
    return requests.get(url).content.decode('utf8')


def parse_title(article_bsoup, lang):
    # Parse h1
    h1 = article_bsoup.find_all('h1')
    h1_span = h1[0].find('span').text.strip()
    h1_small = h1[0].find('small').text.strip()
    # Parse h2
    h2 = article_bsoup.find_all('h2')
    if lang == 'zh':
        h2_span = h2[0].attrs['id'].strip()
    else:
        h2_span = h2[0].text.strip()
    return h1, h1_span, h1_small, h2, h2_span

def slurp_text(bsoup):
    return deduplicate(bsoup.get_text("\n").strip(), '\n').replace('\n', ' <br> '  )

def parse_description(article_bsoup):
    div = article_bsoup.find('div', attrs={'itemprop':'description'}).find_all('p')
    peas = []
    for p in div:
        #if p.text.strip():
        peas.append(slurp_text(p))
    return peas

def parse_hframes(article_bsoup):
    hframes = article_bsoup.find_all('div', attrs={'class':'padding-horizontal'})
    return [slurp_text(div) for div in hframes if div]

def read_static_crawl(filename, lang, dirname='lippli.jp/'):
    if lang == 'ja':
        lang = ''
    filename = dirname+f'{lang}/lineup/'+filename
    with open(filename) as fin:
        bsoup = BeautifulSoup(fin.read())
        article = bsoup.find('article')
    return bsoup, article

def get_parallel_titles(article_bsoups, lang):
    titles = {}
    try:
        for article_bsoup, l in zip(article_bsoups, lang):
            _, h1_span, h1_small, _, h2_span = parse_title(article_bsoup, l)
            section[l] = {'h1_span_0':h1_span, 'h1_small_0': h1_small, 'h2_span_0': h2_span}
    except AttributeError:
        pass
    return titles
