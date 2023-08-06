from youtube.baseparser import BaseSearchParser
from youtube.signatures import ChannelSignature


class ChannelSearchParser(BaseSearchParser):
    _tile_class_name = 'yt-lockup-channel'

    def _parse_single_result(self, search_result):
        self._initialize_parser(repr(search_result))
        return ChannelSignature(self._extract_id(),
                                self._extract_name(),
                                int(self._extract_videos_amount()),
                                int(self._extract_subscriptions()),
                                self._extract_thumbnail_url())

    def _extract_id(self):
        return self._find_by_class('a', 'yt-uix-tile-link')['data-ytid']

    def _extract_name(self):
        return str(self._find_by_class('a', 'yt-uix-tile-link').string)

    def _extract_videos_amount(self):
        try:
            return self._html_parser.select('.yt-lockup-meta-info li')[1].string.split(' ')[0]
        except IndexError:
            return '0'  # no information means user has no uploaded videos

    def _extract_thumbnail_url(self):
        return self._find_by_class('span', 'yt-thumb-simple').img['src']

    def _extract_subscriptions(self):
        count = self._find_by_class('span', 'yt-subscriber-count')
        rmnbs = self._remove_non_breaking_spaces
        return '0' if count is None else rmnbs(count['title']).replace(' ', '').replace(',', '')
