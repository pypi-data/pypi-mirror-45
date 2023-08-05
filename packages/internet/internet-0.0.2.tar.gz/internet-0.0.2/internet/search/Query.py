from datetime import datetime
from chronology import get_elapsed_seconds

class Query:
	def __init__(self, **kwargs):
		self._objects = dict()
		self._timestamps = dict()
		self._durations =dict()
		self._last_timestamp = datetime.now()
		for key, value in kwargs.items():
			self[key] = value

	def __getstate__(self):
		return {
			'objects': self._objects,
			'timestamps': self._timestamps,
			'durations': self._durations
		}

	def __setstate__(self, state):
		self._objects = state['objects']
		self._timestamps = state['timestamps']
		self._durations = state['durations']
		self._last_timestamp = datetime.now()

	def __setitem__(self, key, value):
		self._objects[key] = value
		self._timestamps[key] = datetime.now()
		self._durations[key] = get_elapsed_seconds(start=self._last_timestamp, end=self._timestamps[key])

	def __getitem__(self, item):
		self._last_timestamp = datetime.now()
		return self._objects[item]

	def get_timestamp(self, item):
		return self._timestamps[item]

	def get_duration(self, item):
		return self._durations[item]
