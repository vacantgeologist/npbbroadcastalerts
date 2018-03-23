import copy
import datetime

from pushover import init, Client
from bs4 import BeautifulSoup

from http_funcs import get_page
from config import Config
from teams.hanshin import HanshinTigers


init(Config.APP_TOKEN)

all_teams = [
    HanshinTigers(),
]

def concat_broadcasts(broadcasts):
    """
    Concatenate broadcast dict into a single string
    """
    all_broadcasts = []
    for b in broadcasts:
        s = '{channel} {time}'.format(channel=b['channel'], time=b['time'])
        all_broadcasts.append(s)
    return ' AND '.join(all_broadcasts)

def notify_todays_games(notify_games, team_name):
    """
    Send a push notification for today's games
    """
    for single_game in notify_games:
        today = datetime.datetime.now()
        if today >= single_game['date']:
            message_body = '{team_name} 対 {opponent} {channel_and_time}'.format(
                team_name=team_name,
                opponent=single_game['opponent'],
                channel_and_time=concat_broadcasts(single_game['broadcasts']),
            )
            message_title = '{teamname} {month}月{day}日の試合放送'.format(
                teamname=team.team_name,
                month=today.month, 
                day=today.day,
            )
            # Send a notification to Pushover
            Client(user_key=Config.USER_KEY).send_message(message_body, title=message_title)

for team in all_teams:
    if team.team_name not in Config.NOTIFY_TEAMS:
        continue
    notify_games = []
    team_upcoming_games = team.get_upcoming_games()
    for game in team_upcoming_games:
        if len(game['broadcasts']) > 0:  
            # Only add games with broadcasts
            notify_games.append(game)
    notify_todays_games(notify_games, team.team_name_short)    
    
    # upcoming_games = [
    #     {
    #         'date': <datetime>,
    #         'opponent': 'オリックス',
    #         'broadcasts': [
    #             {
    #                 'broadcast_medium': '地上波',
    #                 'channel': 'サンテレビ',
    #                 'time': '13:45-試合終了まで',
    #             }
    #         ]
    #     }
    # ]
