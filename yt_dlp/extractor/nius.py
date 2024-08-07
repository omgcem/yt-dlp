from .common import InfoExtractor
from ..utils import (
    float_or_none,
    traverse_obj,
    parse_duration
)


class NiusIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?nius\.de/episodes/.*/(?P<id>[a-z0-9\-]+)'
    _TESTS = [{
        'url': 'https://www.nius.de/episodes/sarah-bosetti-grimme-preis-fuer-s-faktenverdrehen/1f3bd94c-aea8-43ff-aeda-52443cceef08',
        'md5': '79ff50e8f974365449d14adf255d82ce',
        'info_dict': {
            'url': 'https://d3bmxwd83nift9.cloudfront.net/df384f3c-9ede-4677-b396-676806676a8d/AppleHLS1/aa8655a7-4a97-4c58-95d8-61406503de6f_Gio%2007.05%20NIUSSS_Ott_Hls_Ts_Avc_Aac_16x9_1920x1080p_5.5Mbps_qvbr.m3u8',
            'id': '1f3bd94c-aea8-43ff-aeda-52443cceef08',
            'title': 'Sarah Bosetti - Grimme-Preis für´s Faktenverdrehen!',
            'description': 'md5:032ac9530bb3261040e5d560e9b64ca9',
            'ext': 'mp4',
            'duration': 840.00,
            'thumbnail': 'https://api.nius.de/api/assets/office-hr/06fae313-797a-4d17-85aa-5e5c06e6c837',
        },
    }
    ]

    def _real_extract(self, url):
        unique_id = self._match_id(url)
        webpage = self._download_webpage(url, unique_id)
        data = self._search_nextjs_data(webpage, unique_id)
        returnData =  {
            **traverse_obj(data, {
                'url': ('props','pageProps','_episode','video','encodedUri'),
                'id': ('props','pageProps','episodeId'),
                'title': ('props','pageProps','_episode','title'),
                'description': ('props','pageProps','_episode','description'),
                'duration':  ('props','pageProps','_episode','video','duration', {parse_duration}, {float_or_none}),
                'thumbnail': ('props','pageProps','_episode','image','original'),
                'ext':  ('props','pageProps','_episode','video','videotype'),
            }),
        }
        formats, subs = self._extract_m3u8_formats_and_subtitles(returnData['url'], returnData['id'], 'mp4')
        returnData['formats'] = formats
        return returnData
