#!/usr/bin/env python
import requests
import os
from bs4 import BeautifulSoup, SoupStrainer
from utils import tabula
import urllib

REPORT_PAGE = 'https://registrar.wisc.edu/current-reports/'

def fetch_dir_links():
  """Retrieve links to DIR PDFs from the registrar website.
  
  [description]
  
  Returns:
    dict -- All DIR files with term code as key, URL as value
  """


  page = requests.get(REPORT_PAGE)
  links = BeautifulSoup(page.text, 'html.parser', parse_only=SoupStrainer('a'))

  dir_hrefs = {}

  for link in links:
    if not link.has_attr('href'):
      continue

    href = link['href']
    href_upper = href.upper()

    # only parse DIR pdfs
    if 'DIR' not in href_upper:
      continue

    # ignore "memos" and "calls", they do not contain data
    if 'MEMO' in href_upper or 'CALL' in href_upper:
      continue

    # get the file name, it contains the term code
    file = href.split("/")[-1]

    # extract the term code, the only digits in the file name
    sis_term_code = int(filter(str.isdigit, str(file)))

    # check if we already encountered this DIR, in case something weird is going on
    if sis_term_code in dir_hrefs:
      existing_href = dir_hrefs[sis_term_code]
      print('Already parsed %s DIR. Did registrar website update?' % sis_term_code)
      print('Ignoring: %s, using existing DIR: %s' % (href, existing_href))
      continue

    # term code -> link
    dir_hrefs[sis_term_code] = href

  return dir_hrefs

# data_path = '../data'

# if not os.path.isdir(data_path):
#   os.makedirs(data_path)

# links = fetch_dir_links()
# for term_code in links:
#   link = links[term_code]

#   urllib.urlretrieve(link, '%s/dir_%s.pdf' % (data_path, term_code))