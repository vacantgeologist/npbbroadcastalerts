# NPBチーム別放送通知

毎日好きなチームのホームページで放送情報を調べるのが面倒だったので、これを作った。 

cron等で登録して、当日の0時以降に実行すると、当日の放送情報をプッシュ通知で受け取ることが可能になる。

## 概要

チームの放送日程が掲載されているページをスクレーピングして、当日の試合放送があった場合はプッシュ通知で知らせてくれる。
見れない放送種別(例えば、CS・BSなど)がある場合は、それらを設定で除外できるようになっている。

利用するにはPushoverのアカウントとアプリのインストールが必要。 https://pushover.net/

Pushover の User Key, App Token をそれぞれ取得して config.py に記載する。

## 対応チーム

現在は阪神タイガースのみだが、他のチームの追加を意識した設計にはなっている。

## 設定について

config.py に設定が記載されている。必要に応じて自分に合った設定に更新してください。

```python
class Config:
    """Manage settings"""
    RESTRICT_TO_VIEWABLE = True  # 見れる放送のみ通知するかどうか
    MY_VIEWABLE_MEDIA = ['地上波']  # 自分の見れる放送の種別
    APP_TOKEN = ''  # Pushover App Token
    USER_KEY = ''  # Pushover User Key
    NOTIFY_TEAMS = ['阪神タイガース']  # 見たいチームをこちらに追加
```

## 他のチームを追加するには？

`teams/<teamname>.py` のファイルに以下のメソッドを持つクラスを作ると追加できる。 `teams/hanshin.py`を参考に。

- `get_upcoming_games`: チームのページをBeautifulSoupでスクレーピングして、以下の形式のdictで必要な情報を返す

なお、クラスが持つ以下の変数の定義も必要：

- `self.url`: スクレーピングするurl
- `team_name`: チーム名 (config.pyのNOTIFY_TEAMSで利用)
- `team_name_short`: チーム名(省略)、例えば 「中日ドラゴンズ」⇒ 「中日」。 

```python
upcoming_games = [
    {
        'date': <datetime>,  # datetime object 試合の日付、 timeは当日の0時に設定
        'opponent': 'オリックス',  # str 相手チーム
        'broadcasts': [  # list その試合の書く放送
            {
                'broadcast_medium': '地上波',  # str
                'channel': 'サンテレビ',  # str
                'time': '13:45-試合終了まで',  # str
            }
        ]
    }
]
```

notify.py にクラスをインポートし、all_teamsのリストにインスタンスを追加すると利用できるようになる(はず)。

```python
from teams import HanshinTigers

all_teams = [
    HanshinTigers(),
]
```
