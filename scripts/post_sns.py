#!/usr/bin/env python3
"""
SNS自動投稿スクリプト
X/Twitter APIで新着記事を自動シェアする

必要な環境変数:
- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_SECRET
"""

import os
import json
import hmac
import hashlib
import base64
import time
import urllib.request
import urllib.parse
import urllib.error
import uuid


def post_to_twitter(text: str) -> bool:
    """X/Twitter API v2 でツイートする"""
    api_key = os.environ.get("TWITTER_API_KEY", "")
    api_secret = os.environ.get("TWITTER_API_SECRET", "")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN", "")
    access_secret = os.environ.get("TWITTER_ACCESS_SECRET", "")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("⚠️ Twitter APIキーが設定されていません。SNS投稿をスキップします。")
        print(f"📱 手動投稿用テキスト:\n{text}")
        return False

    url = "https://api.twitter.com/2/tweets"
    method = "POST"

    # OAuth 1.0a 署名生成
    oauth_params = {
        "oauth_consumer_key": api_key,
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token,
        "oauth_version": "1.0",
    }

    # 署名ベース文字列
    param_string = "&".join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
        for k, v in sorted(oauth_params.items())
    )
    base_string = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_string, safe='')}"
    signing_key = f"{urllib.parse.quote(api_secret, safe='')}&{urllib.parse.quote(access_secret, safe='')}"

    signature = base64.b64encode(
        hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
    ).decode()

    oauth_params["oauth_signature"] = signature

    auth_header = "OAuth " + ", ".join(
        f'{urllib.parse.quote(k, safe="")}="{urllib.parse.quote(v, safe="")}"'
        for k, v in sorted(oauth_params.items())
    )

    payload = json.dumps({"text": text}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tweet_id = data.get("data", {}).get("id", "unknown")
            print(f"✅ ツイート投稿成功！ ID: {tweet_id}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"❌ Twitter API エラー {e.code}: {body}")
        return False


def main():
    sns_text_path = os.path.join(os.path.dirname(__file__), "..", "latest_sns.txt")

    if not os.path.exists(sns_text_path):
        print("⚠️ latest_sns.txt が見つかりません。先に記事を生成してください。")
        return

    with open(sns_text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("⚠️ SNSテキストが空です")
        return

    print(f"📱 投稿テキスト:\n{text}\n")
    post_to_twitter(text)


if __name__ == "__main__":
    main()
