from .SearchEngine import SearchEngine, Navigator
from bs4 import BeautifulSoup


class Bing(SearchEngine):
	def __init__(self, navigator=None):
		"""
		:type navigator: Navigator
		"""
		super().__init__(base_url='https://bing.com', navigator=navigator)

	def reset(self):
		super().reset()


	def get_search_url(self, query):
		return f'{self.url}/search?q={query}'

	def parse_search_results(self, html):
		"""
		:type html: BeautifulSoup
		:rtype: list[dict[str,str]]
		"""
		b_content = html.findAll(attrs={'id': 'b_content'})[0]
		b_algo = b_content.findAll(attrs={'class': 'b_algo'})
		results = [{'url': result.findAll('a')[0]['href'], 'text': result.get_text()} for result in b_algo]
		return results
