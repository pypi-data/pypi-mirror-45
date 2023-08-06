from youtube.baseparser import BaseSearchParser
from youtube.signatures import VideoSignature


class VideoSearchParser(BaseSearchParser):
	_tile_class_name = 'yt-lockup-video'

	def _parse_single_result(self, search_result):
		self._initialize_parser(repr(search_result))
		return VideoSignature(self._extract_id(), self._extract_title(),
							  self._extract_author(), self._extract_views(),
							  self._extract_length())

	def _extract_length(self):
		try:
			buf = str(self._find_by_class('span', 'video-time').string)
		except Exception as e:
			buf = "live"
		return buf

	def _extract_author(self):
		return str(self._find_by_class('div', 'yt-lockup-byline').a.string)

	def _extract_title(self):
		return str(self._find_by_class('h3', 'yt-lockup-title').a.string)

	def _extract_id(self):
		return self._html_parser.div['data-context-item-id']

	def _extract_views(self):
		views_ul = self._find_by_class('ul', 'yt-lockup-meta-info')
		li_lst = views_ul.find_all('li')
		rmnbs = self._remove_non_breaking_spaces
		views = rmnbs(li_lst[1].string.split(' ')[0]).replace(',', '') if len(li_lst) > 1 else '0'
		try:
			return int(views)
		except ValueError:
			return 0
