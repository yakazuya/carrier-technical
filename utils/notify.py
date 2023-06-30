import slackweb

def send2app(text: str, slack_id: str) -> None:
    if text == '':
        text = '条件を満たす銘柄がありません'
    slack = slackweb.Slack(url = slack_id)
    slack.notify(text = text)

def make_text(ticker: str, notify_dict: dict) -> str:
    indicator_list = list(notify_dict[ticker].keys())
    _text = []
    text = f'<{ticker}>\n'
    for indicator in indicator_list:
        label = notify_dict[ticker][indicator]
        _text.append(f'{indicator}:{label}')
    for item in _text:
        text += f'  {item}\n'
    return text

def notify(notify_dict:dict, slack_id:str) -> None:
    text = str()

    for ticker in notify_dict:
        text += make_text(ticker, notify_dict)
    
    send2app(text, slack_id)
