from .. import Navigator
from .Query import Query
from datetime import datetime
from chronology import get_elapsed_seconds


class SearchEngine:
	def __init__(self, base_url, navigator=None):
		"""
		:type base_url: str
		:type navigator: Navigator or NoneType
		"""
		self._base_url = base_url
		self._navigator = navigator or Navigator()
		self._elapsed_time = 0
		self._num_queries = 0


	def reset(self):
		self._elapsed_time = 0
		self._num_queries = 0

	@property
	def query_speed(self):
		return self._elapsed_time / self._num_queries

	@property
	def navigator(self):
		"""
		:rtype: Navigator
		"""
		return self._navigator

	@property
	def url(self):
		"""
		:rtype: str
		"""
		return self._base_url

	def get_search_url(self, query):
		"""
		:type query: str
		:rtype: str
		"""
		return f'{self.url}/search?q={query}'

	@staticmethod
	def parse_search_results(html):
		raise RuntimeError('this is just a place holder')

	def search(self, query, **kwargs):
		"""
		:type query: str
		:param callable or NoneType search_function: a function that can be called on html and returns results
		:rtype: list
		"""
		start_time = datetime.now()
		q = Query(query = query)
		q['url'] = self.get_search_url(query=query)
		q['html'] = self.navigator.get(url=q['url'], **kwargs)
		q['result'] = self.parse_search_results(q['html'])
		end_time = datetime.now()
		self._elapsed_time += get_elapsed_seconds(start=start_time, end=end_time)
		self._num_queries += 1
		return q
