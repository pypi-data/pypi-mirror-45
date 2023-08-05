from .SearchEngine import SearchEngine, Navigator
from bs4 import BeautifulSoup


class DuckDuckGo(SearchEngine):
	def __init__(self, navigator=None):
		"""
		:type navigator: Navigator
		"""
		super().__init__(base_url='https://duckduckgo.com', navigator=navigator)
		self._links = None
		self._raw_results = None
		self._results = None

	def reset(self):
		super().reset()
		self._links = None
		self._raw_results = None
		self._results = None

	def get_search_url(self, query):
		return f'{self.url}/?q={query}&ia=web'

	def parse_search_results(self, html):
		"""
		:type html: BeautifulSoup
		:rtype: list[dict[str,str]]
		"""
		self._links = html.findAll(attrs={'id': 'links'})[0]
		self._raw_results = self._links.findAll(attrs={'class': 'result__a'})
		self._results = [
			{'url': result.attrs['href'], 'text': result.get_text()}
			for result in self._raw_results if not result.attrs['href'].startswith('https://duckduckgo.com')
		]
		return self._results
