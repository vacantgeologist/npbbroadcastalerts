import datetime

from bs4 import BeautifulSoup

from http_funcs import get_page
from config import Config


class HanshinTigers:
    """Hanshin Tigers"""

    def __init__(self):
        self.team_name = '阪神タイガース'
        self.team_name_short = '阪神'
        self.url = 'http://hanshintigers.jp/news/media/live.html'

    @staticmethod
    def summarize_game_info(basic_info, headers, content):
        """
        Summarize the scraped game info into dict form. If broadcasts should be restricted to only those that
        are viewable, unviewable broadcasts will be eliminated.
        """
        convert = {
            '種別': 'broadcast_medium',
            '放送局': 'channel',
            '時間': 'time',
        }
        for i, h in enumerate(headers):
            headers[i] = convert[h]
        game = basic_info.copy()
        game['broadcasts'] = []
        for c in content:
            headers_and_content = zip(headers, c)
            broadcast = {}
            for k, v in headers_and_content:
                broadcast[k] = v
            if Config.RESTRICT_TO_VIEWABLE and broadcast['broadcast_medium'] in Config.MY_VIEWABLE_MEDIA:
                game['broadcasts'].append(broadcast)
        return game

    @staticmethod
    def convert_date(datestr):
        """
        Convert the date on the Tigers' page, which is in M/DD format, to a datetime object for easy handling
        """
        datestr_with_year = '{year}/{date}'.format(year=datetime.datetime.now().year, date=datestr)
        game_day = datetime.datetime.strptime(datestr_with_year, '%Y/%m/%d')
        return game_day

    def get_upcoming_games(self):
        """Scrape the Tigers' media page and return info on all upcoming games.
        
        :return dict: All upcoming games scraped from the page
        """
        upcoming_games = []
        raw_html = get_page(self.url)
        html = BeautifulSoup(raw_html, 'html.parser')
        for i, game in enumerate(html.select('div.media-list')):
            game_info_headers = []
            game_info_content = []
            basic_info = {}
            game_date = game.select('.day1')[0]
            opponent = game.select('.day3')[0]
            basic_info['date'] = self.convert_date(game_date.text) # '3/21' -> datetime object
            basic_info['opponent'] = opponent.text.replace('戦', '')  # '巨人戦' -> '巨人'
            game_info_categories = game.select('thead th')
            for i, info_type in enumerate(game_info_categories):
                if i < 3:  # [3]は詳細なので要らない 
                    game_info_headers.append(info_type.text)
            broadcast_infos = game.select('tbody tr')
            for i, info_piece in enumerate(broadcast_infos):
                broadcast = []
                single_broadcast = info_piece.select('td')
                for info in single_broadcast:
                    broadcast.append(info.text)
                game_info_content.append(broadcast[:3])  # 詳細は除く
            formatted_info = self.summarize_game_info(basic_info, game_info_headers, game_info_content)
            upcoming_games.append(formatted_info)
        return upcoming_games



