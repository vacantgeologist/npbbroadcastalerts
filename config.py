class Config:
    """Manage settings"""
    RESTRICT_TO_VIEWABLE = True  # 見れる放送のみ通知するかどうか
    MY_VIEWABLE_MEDIA = ['地上波']  # 自分の見れる放送の種別
    APP_TOKEN = ''  # Pushover App Token
    USER_KEY = ''  # Pushover User Key
    NOTIFY_TEAMS = ['阪神タイガース']  # 見たいチームをこちらに追加
