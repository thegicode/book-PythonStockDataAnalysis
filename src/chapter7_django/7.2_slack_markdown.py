import os
from dotenv import load_dotenv
import requests

# 환경 변수 로드
load_dotenv()

# Slack 인증 토큰 및 채널 ID 설정
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

def send_slack_message_with_md(markdown_text: str, attachments: list):
    """
    슬랙으로 마크다운 텍스트와 첨부 파일을 포함한 메시지를 전송합니다.
    """
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": CHANNEL_ID,
        "text": markdown_text,  # 기본 텍스트
        "attachments": attachments  # 첨부 파일
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            print("메시지 전송 성공")
        else:
            print(f"슬랙 API 에러: {data.get('error')}")
    else:
        print(f"HTTP 요청 실패: {response.status_code}")

if __name__ == "__main__":
    # 마크다운 텍스트
    markdown_text = '''
    This message is plain.
    *This message is bold.*
    `This message is code.`
    _This message is italic._
    ~This message is strike.~
    '''

    # 첨부 파일
    attach_dict = {
        "color": "#ff0000",
        "author_name": "INVESTAR",
        "author_link": "https://github.com/investar",
        "title": "오늘의 증시 KOSPI",
        "title_link": "http://finance.naver.com/sise/sise_index.nhn?code=KOSPI",
        "text": "2,488.97 △11.89 (+0.51%)",
        "image_url": "https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png"
    }
    attach_list = [attach_dict]

    # 메시지 전송
    send_slack_message_with_md(markdown_text, attach_list)
