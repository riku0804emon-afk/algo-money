#!/usr/bin/env python3
"""
トップページの記事一覧セクションを自動更新する
articles/index.json を読み込んで index.html の記事セクションを書き換える
"""

import os
import json
import re


def update_index_page():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    index_html_path = os.path.join(base_dir, "index.html")
    articles_index_path = os.path.join(base_dir, "articles", "index.json")

    if not os.path.exists(articles_index_path):
        print("⚠️ articles/index.json が見つかりません")
        return

    with open(articles_index_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # 最新6件を取得
    latest = articles[:6]

    # 記事カードHTMLを生成
    emojis = {
        "レビュー": "⭐",
        "ノウハウ": "💡",
        "ガイド": "📘",
        "税金・法律": "📊",
        "比較": "⚖️",
        "体験談": "💬",
        "ランキング": "🏆",
        "コラム": "📝",
    }
    colors = {
        "レビュー": "#DBEAFE,#F3E8FF",
        "ノウハウ": "#D1FAE5,#DBEAFE",
        "ガイド": "#DBEAFE,#CFFAFE",
        "税金・法律": "#FEF3C7,#DBEAFE",
        "比較": "#F3E8FF,#FCE7F3",
        "体験談": "#D1FAE5,#FEF3C7",
        "ランキング": "#FEF3C7,#FCE7F3",
        "コラム": "#F1F5F9,#DBEAFE",
    }

    cards_html = ""
    for i, art in enumerate(latest):
        emoji = emojis.get(art.get("category", ""), "📝")
        color = colors.get(art.get("category", ""), "#DBEAFE,#F3E8FF")
        delay = f" reveal-delay-{(i % 3) + 1}"
        cards_html += f"""    <a href="{art['url']}" class="article-card reveal{delay}">
      <div class="article-thumb">
        <div class="article-thumb-inner" style="background:linear-gradient(135deg,{color})">{emoji}</div>
        <div class="article-cat">{art.get('category', '')}</div>
      </div>
      <div class="article-body">
        <div class="article-title">{art['title']}</div>
        <div class="article-meta">
          <span>{art.get('date', '')}</span>
          <span class="article-read">続きを読む <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
        </div>
      </div>
    </a>
"""

    # index.html を読み込んで記事セクションを差し替え
    if not os.path.exists(index_html_path):
        print("⚠️ index.html が見つかりません")
        return

    with open(index_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # <!-- ARTICLES_START --> と <!-- ARTICLES_END --> の間を差し替え
    pattern = r"(<!-- ARTICLES_START -->).*?(<!-- ARTICLES_END -->)"
    replacement = f"\\1\n{cards_html}  \\2"
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    if new_html == html:
        print("⚠️ ARTICLES_START/END マーカーが見つかりません。index.htmlにマーカーを追加してください。")
        return

    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"✅ index.html 更新完了: {len(latest)}件の記事を表示")


if __name__ == "__main__":
    update_index_page()
