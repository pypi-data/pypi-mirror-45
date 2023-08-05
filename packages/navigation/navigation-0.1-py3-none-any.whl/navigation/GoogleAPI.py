import socket
import time
import gzip
from io import StringIO
import re
import random
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import URLError

base_url = 'https://www.google.com'
results_per_page = 10
user_agents = list()


class SearchResult:
	def __init__(self):
		self.url = ''
		self.title = ''
		self.content = ''

	def get_url(self):
		return self.url

	def set_url(self, url):
		self.url = url

	def get_title(self):
		return self.title

	def set_title(self, title):
		self.title = title

	def get_content(self):
		return self.content

	def set_content(self, content):
		self.content = content

	def print_it(self):
		print('url\t->', self.url)
		print('title\t->', self.title)
		print('content\t->', self.content)
		print()

	def write_file(self, filename):
		file = open(filename, 'a')
		try:
			file.write('url:' + self.url + '\n')
			file.write('title:' + self.title + '\n')
			file.write('content:' + self.content + '\n\n')
		except IOError as e:
			print('file error:', e)
		finally:
			file.close()


class GoogleAPI:
	def __init__(self):
		timeout = 40
		socket.setdefaulttimeout(timeout)

	@staticmethod
	def random_sleep():
		sleep_time = random.randint(60, 120)
		time.sleep(sleep_time)

	@staticmethod
	def extract_domain(url):
		"""Return string
		extract the domain of a url
		"""
		domain = ''
		pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
		url_match = pattern.search(url)
		if url_match and url_match.lastindex > 0:
			domain = url_match.group(1)

		return domain

	@staticmethod
	def extract_url(href):
		""" Return a string
		extract a url from a link
		"""
		url = ''
		pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
		url_match = pattern.search(href)
		if url_match and url_match.lastindex > 0:
			url = url_match.group(1)

		return url

	def extract_search_results(self, html):
		"""Return a list
		extract serach results list from downloaded html file
		"""
		results = list()
		soup = BeautifulSoup(html, 'html.parser')
		div = soup.find('div', id='search')
		if div is not None:
			lis = div.findAll('div', {'class': 'g'})
			if len(lis) > 0:
				for li in lis:
					result = SearchResult()
					h3 = li.find('h3', {'class': 'r'})
					if h3 is None:
						continue
					# extract domain and title from h3 object
					link = h3.find('a')
					if link is None:
						continue
					url = link['href']
					url = self.extract_url(url)
					if (url > '') - (url < '') == 0:
						continue
					title = link.renderContents()
					title = re.sub(r'<.+?>', '', title)
					result.set_url(url)
					result.set_title(title)
					span = li.find('span', {'class': 'st'})
					if span is not None:
						content = span.renderContents()
						content = re.sub(r'<.+?>', '', content)
						result.set_content(content)
					results.append(result)
		return results

	def search(self, query, lang='en', num=results_per_page):
		"""Return a list of lists
		search web
		@param query -> query key words
		@param lang -> language of search results
		@param num -> number of search results to return
		"""
		search_results = list()
		query = quote(query)
		if num % results_per_page == 0:
			pages = int(round(num / results_per_page))
		else:
			pages = int(round(num / results_per_page + 1))

		for p in range(0, pages):
			start = p * results_per_page
			url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (
				base_url, lang, results_per_page, start, query)
			retry = 3
			while retry > 0:
				try:
					request = Request(url)
					length = len(user_agents)
					index = random.randint(0, length-1)
					user_agent = user_agents[index]
					request.add_header('User-agent', user_agent)
					request.add_header('connection', 'keep-alive')
					request.add_header('Accept-Encoding', 'gzip')
					request.add_header('referer', base_url)
					response = urlopen(request)
					html = response.read()
					if response.headers.get('content-encoding', None) == 'gzip':
						html = gzip.GzipFile(
							fileobj=StringIO(html)).read()

					results = self.extract_search_results(html)
					search_results.extend(results)
					break
				except URLError as e:
					print('url error:', e)
					self.random_sleep()
					retry = retry - 1
					continue

				except Exception as e:
					print('error:', e)
					retry = retry - 1
					self.random_sleep()
					continue
		return search_results
