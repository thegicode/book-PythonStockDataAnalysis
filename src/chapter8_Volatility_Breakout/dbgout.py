

from datetime import datetime
import os
from dotenv import load_dotenv
import requests

# 환경 변수 로드
load_dotenv()

# Slack 인증 토큰
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
CHANNEL_ID =  os.getenv("SLACK_CHANNEL_ID")

def send_slack_message(message: str):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": CHANNEL_ID,
        "text": message
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


def dbgout(message):
    # 현재 시간 형식 문자열 생성
    now = datetime.now().strftime('[%m/%d %H:%M:%S]')

    # 시간 문자열과 메시지 결합
    strbuf = f"{now} {message}"
    print(strbuf)
    send_slack_message(strbuf)


if __name__ == "__main__":
    dbgout("메세지 테스트")

