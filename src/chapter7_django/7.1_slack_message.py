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


# 메시지 보내기 예제
if __name__ == "__main__":
    send_slack_message("안녕하세요! 슬랙 봇을 통해 보내는 메시지입니다.")


