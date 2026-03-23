#!/usr/bin/env python3
"""
alogo-money.dev ブログ記事自動生成スクリプト
OpenRouter API を使って副業・在宅ワーク系の記事を自動生成する
"""

import os
import json
import random
import datetime
import re
import urllib.request
import urllib.error

# ========== 設定 ==========
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = os.environ.get("MODEL", "anthropic/claude-sonnet-4")
SITE_NAME = "alogo-money.dev"
SITE_URL = "https://algo-money.dev"
AUTHOR = "alogo-money編集部"

# ========== アフィリエイトリンク設定 ==========
# TODO: 実際のアフィリリンクに差し替えてね
AFFILIATE_LINKS = {
    "クラウドワークス": {
        "url": os.environ.get("AFF_CROWDWORKS", "https://crowdworks.jp/?ref=alogo"),
        "description": "国内最大級のクラウドソーシング",
        "category": "クラウドソーシング"
    },
    "ランサーズ": {
        "url": os.environ.get("AFF_LANCERS", "https://lancers.jp/?ref=alogo"),
        "description": "プロジェクト形式が充実",
        "category": "クラウドソーシング"
    },
    "ココナラ": {
        "url": os.environ.get("AFF_COCONALA", "https://px.a8.net/svt/ejp?a8mat=4AZMKL+D1R12Q+2PEO+1HMAQQ"),
        "description": "スキルを出品できるマーケット",
        "category": "スキルマーケット"
    },
    "レバテックフリーランス": {
        "url": os.environ.get("AFF_LEVTECH", "https://freelance.levtech.jp/?ref=alogo"),
        "description": "エンジニア特化の高単価案件",
        "category": "フリーランス"
    },
    "SHElikes": {
        "url": os.environ.get("AFF_SHELIKES", "https://shelikes.jp/?ref=alogo"),
        "description": "女性向けキャリアスクール",
        "category": "スクール"
    },
    "マクロミル": {
        "url": os.environ.get("AFF_MACROMILL", "https://monitor.macromill.com/?ref=alogo"),
        "description": "国内最大級のアンケートモニター",
        "category": "アンケート"
    },
    "A8.net": {
        "url": os.environ.get("AFF_A8", "https://a8.net/?ref=alogo"),
        "description": "日本最大級のASP",
        "category": "ASP"
    },
    "もしもアフィリエイト": {
        "url": os.environ.get("AFF_MOSHIMO", "https://af.moshimo.com/?ref=alogo"),
        "description": "W報酬制度が魅力のASP",
        "category": "ASP"
    },
    "SBI FXトレード": {
        "url": os.environ.get("AFF_SBIFX", "https://sbifxt.co.jp/?ref=alogo"),
        "description": "1通貨から取引可能なFX",
        "category": "投資"
    },
    "Coincheck": {
        "url": os.environ.get("AFF_COINCHECK", "https://coincheck.com/ja/?ref=alogo"),
        "description": "初心者向け仮想通貨取引所",
        "category": "投資"
    }
}

# ========== 記事テーマ ==========
ARTICLE_TOPICS = [
    {
        "title_template": "【{year}年最新】{service}の評判・口コミ｜実際に使ってわかったメリット・デメリット",
        "category": "レビュー",
        "services": ["クラウドワークス", "ランサーズ", "ココナラ", "レバテックフリーランス", "SHElikes", "マクロミル"],
        "tags": ["副業", "口コミ", "評判"]
    },
    {
        "title_template": "副業初心者が最初の月に{amount}万円稼ぐためのロードマップ",
        "category": "ノウハウ",
        "amounts": ["1", "3", "5", "10"],
        "tags": ["副業", "初心者", "稼ぎ方"]
    },
    {
        "title_template": "【{year}年版】{job_type}で稼ぐ方法｜未経験からの始め方完全ガイド",
        "category": "ガイド",
        "job_types": ["Webライティング", "プログラミング副業", "動画編集", "Webデザイン", "データ入力", "SNS運用代行", "ブログアフィリエイト", "せどり・転売"],
        "tags": ["副業", "始め方", "未経験"]
    },
    {
        "title_template": "副業の確定申告｜{topic}を徹底解説",
        "category": "税金・法律",
        "topics": ["20万円ルールの落とし穴", "経費にできるもの一覧", "会社にバレない方法", "青色申告と白色申告の違い", "住民税の申告方法"],
        "tags": ["確定申告", "税金", "副業"]
    },
    {
        "title_template": "{service1}と{service2}を徹底比較｜どっちがおすすめ？",
        "category": "比較",
        "pairs": [
            ("クラウドワークス", "ランサーズ"),
            ("ココナラ", "クラウドワークス"),
            ("A8.net", "もしもアフィリエイト"),
        ],
        "tags": ["比較", "副業", "おすすめ"]
    },
    {
        "title_template": "【体験談】{persona}が{service}で{period}やってみた結果",
        "category": "体験談",
        "personas": ["大学生", "主婦", "会社員", "フリーター"],
        "services": ["クラウドワークス", "ランサーズ", "ココナラ", "マクロミル"],
        "periods": ["1ヶ月", "3ヶ月", "半年"],
        "tags": ["体験談", "副業", "収入公開"]
    },
    {
        "title_template": "【{year}年】おすすめ副業ランキングTOP10｜{target}向け",
        "category": "ランキング",
        "targets": ["初心者", "学生", "主婦", "会社員", "スキマ時間で稼ぎたい人"],
        "tags": ["ランキング", "副業", "おすすめ"]
    },
    {
        "title_template": "{topic}｜副業で成功するための{keyword}",
        "category": "コラム",
        "combos": [
            ("時間管理術", "3つのルール"),
            ("モチベーション維持", "5つの習慣"),
            ("本業との両立", "タイムブロッキング術"),
            ("副業仲間の作り方", "コミュニティ活用法"),
        ],
        "tags": ["コラム", "副業", "マインドセット"]
    }
]


def call_openrouter(prompt: str, system_prompt: str = "") -> str:
    """OpenRouter APIを呼び出す"""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY が設定されていません")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "max_tokens": 4000,
        "temperature": 0.7,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": SITE_URL,
            "X-Title": SITE_NAME,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter API error {e.code}: {body}")


def pick_topic() -> dict:
    """ランダムに記事テーマを選んで具体的なタイトルを生成"""
    now = datetime.datetime.now()
    year = now.year
    topic_template = random.choice(ARTICLE_TOPICS)
    category = topic_template["category"]
    tags = list(topic_template["tags"])

    title_tpl = topic_template["title_template"]

    if category == "レビュー":
        service = random.choice(topic_template["services"])
        title = title_tpl.format(year=year, service=service)
        tags.append(service)
        context = {"service": service}
    elif category == "ノウハウ":
        amount = random.choice(topic_template["amounts"])
        title = title_tpl.format(amount=amount)
        context = {"amount": amount}
    elif category == "ガイド":
        job_type = random.choice(topic_template["job_types"])
        title = title_tpl.format(year=year, job_type=job_type)
        tags.append(job_type)
        context = {"job_type": job_type}
    elif category == "税金・法律":
        topic = random.choice(topic_template["topics"])
        title = title_tpl.format(topic=topic)
        context = {"topic": topic}
    elif category == "比較":
        pair = random.choice(topic_template["pairs"])
        title = title_tpl.format(service1=pair[0], service2=pair[1])
        tags.extend(list(pair))
        context = {"service1": pair[0], "service2": pair[1]}
    elif category == "体験談":
        persona = random.choice(topic_template["personas"])
        service = random.choice(topic_template["services"])
        period = random.choice(topic_template["periods"])
        title = title_tpl.format(persona=persona, service=service, period=period)
        tags.extend([service, persona])
        context = {"persona": persona, "service": service, "period": period}
    elif category == "ランキング":
        target = random.choice(topic_template["targets"])
        title = title_tpl.format(year=year, target=target)
        tags.append(target)
        context = {"target": target}
    elif category == "コラム":
        combo = random.choice(topic_template["combos"])
        title = title_tpl.format(topic=combo[0], keyword=combo[1])
        context = {"topic": combo[0], "keyword": combo[1]}
    else:
        title = title_tpl
        context = {}

    return {
        "title": title,
        "category": category,
        "tags": tags,
        "context": context,
    }


def generate_article(topic_info: dict) -> dict:
    """OpenRouter APIで記事本文を生成する"""
    title = topic_info["title"]
    category = topic_info["category"]
    tags = topic_info["tags"]

    # 利用可能なサービスリストを渡す
    services_info = "\n".join(
        f"- {name}: {info['description']}（{info['category']}）"
        for name, info in AFFILIATE_LINKS.items()
    )

    system_prompt = f"""あなたは副業・在宅ワーク専門の日本語ブログライターです。
SEOに強く、読者に価値を提供する記事を書いてください。

ルール:
1. 日本語で書く
2. 見出し（h2, h3）を適切に使う
3. HTMLタグで出力する（<h2>, <h3>, <p>, <ul>, <li>, <strong>, <blockquote> など）
4. 以下のサービス名が記事内容に関連する場合、自然な文脈で言及する：
{services_info}
5. サービス名を言及する際は、必ず {{{{AFFILIATE:サービス名}}}} の形式で記述する
   例: {{{{AFFILIATE:クラウドワークス}}}} に登録して始めましょう
6. 記事の冒頭にリード文（導入）を入れる
7. 記事の最後に「まとめ」セクションを入れる
8. 2500〜4000文字程度
9. 具体的な数字やデータを含める
10. 読者目線で実用的な内容にする
11. <article>タグで囲む
12. 体験談カテゴリの場合、リアルな体験談風に書く"""

    prompt = f"""以下のテーマで副業ブログ記事を書いてください。

タイトル: {title}
カテゴリ: {category}
タグ: {', '.join(tags)}

SEOを意識し、読者にとって価値のある具体的な内容を書いてください。
HTMLタグで出力してください。サービスへの言及は {{{{AFFILIATE:サービス名}}}} 形式を使ってください。"""

    content = call_openrouter(prompt, system_prompt)
    return {
        "title": title,
        "category": category,
        "tags": tags,
        "content": content,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }


def insert_affiliate_links(content: str) -> str:
    """{{AFFILIATE:サービス名}} をアフィリリンクに置換"""
    for name, info in AFFILIATE_LINKS.items():
        pattern = r"\{\{AFFILIATE:" + re.escape(name) + r"\}\}"
        link_html = (
            f'<a href="{info["url"]}" target="_blank" rel="noopener sponsored" '
            f'class="aff-link">{name}</a>'
        )
        content = re.sub(pattern, link_html, content)
    return content


def generate_meta_description(title: str, content: str) -> str:
    """記事のmeta descriptionを生成"""
    # コンテンツからタグを除去して先頭120文字
    text = re.sub(r"<[^>]+>", "", content)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 120:
        text = text[:117] + "..."
    return text


def generate_slug(title: str) -> str:
    """タイトルからURLスラッグを生成"""
    slug = datetime.datetime.now().strftime("%Y%m%d")
    keywords = {
        "クラウドワークス": "crowdworks",
        "ランサーズ": "lancers",
        "ココナラ": "coconala",
        "レバテック": "levtech",
        "SHElikes": "shelikes",
        "マクロミル": "macromill",
        "確定申告": "tax",
        "比較": "compare",
        "ランキング": "ranking",
        "体験談": "experience",
        "初心者": "beginner",
        "ライティング": "writing",
        "プログラミング": "programming",
        "動画編集": "video-editing",
        "Webデザイン": "web-design",
        "データ入力": "data-entry",
        "ブログ": "blog",
        "せどり": "resale",
        "SNS": "sns",
        "レビュー": "review",
        "口コミ": "review",
        "ガイド": "guide",
        "コラム": "column",
        "ノウハウ": "howto",
        "主婦": "housewife",
        "学生": "student",
        "会社員": "salaryman",
        "フリーター": "freeter",
        "時間管理": "time-management",
        "モチベーション": "motivation",
        "A8.net": "a8net",
        "もしも": "moshimo",
        "FX": "fx",
        "仮想通貨": "crypto",
    }
    found = []
    for jp, en in keywords.items():
        if jp in title:
            found.append(en)
    # 重複除去しつつ順序保持
    seen = set()
    unique = []
    for k in found:
        if k not in seen:
            seen.add(k)
            unique.append(k)
    if unique:
        slug += "-" + "-".join(unique[:3])
    else:
        slug += "-article"
    # ランダム suffix で重複回避
    slug += "-" + str(random.randint(100, 999))
    return slug


def generate_structured_data(article: dict, slug: str) -> str:
    """JSON-LD 構造化データを生成"""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article["title"],
        "datePublished": article["date"],
        "dateModified": article["date"],
        "author": {
            "@type": "Organization",
            "name": AUTHOR,
            "url": SITE_URL,
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL,
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{SITE_URL}/articles/{slug}.html",
        },
        "keywords": ", ".join(article["tags"]),
    }, ensure_ascii=False, indent=2)


def save_article(article: dict) -> str:
    """記事をHTMLファイルとして保存"""
    slug = generate_slug(article["title"])
    content_with_links = insert_affiliate_links(article["content"])
    meta_desc = generate_meta_description(article["title"], article["content"])
    structured_data = generate_structured_data(article, slug)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{', '.join(article['tags'])}">
<meta property="og:title" content="{article['title']}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE_URL}/articles/{slug}.html">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{article['title']}">
<meta name="twitter:description" content="{meta_desc}">
<link rel="canonical" href="{SITE_URL}/articles/{slug}.html">
<title>{article['title']}｜{SITE_NAME}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">
{structured_data}
</script>
<link rel="stylesheet" href="../static/article.css">
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-logo"><span class="dot"></span>alogo<span>-money</span>.dev</a>
    <div class="nav-links">
      <a href="../index.html#ranking">ランキング</a>
      <a href="../index.html#articles">記事一覧</a>
      <a href="../index.html#ranking" class="nav-cta">今すぐ始める →</a>
    </div>
  </div>
</nav>

<main class="article-main">
  <div class="article-header">
    <div class="article-meta-top">
      <span class="article-cat-badge">{article['category']}</span>
      <time datetime="{article['date']}">{article['date']}</time>
    </div>
    <h1>{article['title']}</h1>
    <div class="article-tags">
      {''.join(f'<span class="article-tag">#{tag}</span>' for tag in article['tags'])}
    </div>
  </div>

  <div class="article-toc" id="toc"></div>

  <div class="article-content">
    {content_with_links}
  </div>

  <div class="article-cta-box">
    <h3>副業を始めるならまずはここから</h3>
    <p>初心者におすすめのサービスを厳選しました。すべて無料で登録できます。</p>
    <div class="cta-links">
      <a href="{AFFILIATE_LINKS['クラウドワークス']['url']}" target="_blank" rel="noopener sponsored" class="cta-link-btn">クラウドワークス（無料登録）</a>
      <a href="{AFFILIATE_LINKS['ランサーズ']['url']}" target="_blank" rel="noopener sponsored" class="cta-link-btn">ランサーズ（無料登録）</a>
      <a href="{AFFILIATE_LINKS['ココナラ']['url']}" target="_blank" rel="noopener sponsored" class="cta-link-btn">ココナラ（無料登録）</a>
    </div>
  </div>

  <div class="article-share">
    <p>この記事をシェアする</p>
    <div class="share-buttons">
      <a href="https://twitter.com/intent/tweet?url={SITE_URL}/articles/{slug}.html&text={article['title']}" target="_blank" rel="noopener" class="share-btn share-x">X でシェア</a>
      <a href="https://www.facebook.com/sharer/sharer.php?u={SITE_URL}/articles/{slug}.html" target="_blank" rel="noopener" class="share-btn share-fb">Facebook</a>
      <a href="https://b.hatena.ne.jp/entry/{SITE_URL}/articles/{slug}.html" target="_blank" rel="noopener" class="share-btn share-hatena">はてブ</a>
    </div>
  </div>
</main>

<footer class="footer">
  <div class="footer-inner-simple">
    <div class="footer-logo">alogo<span>-money</span>.dev</div>
    <p>© {datetime.datetime.now().year} {SITE_NAME} All rights reserved.</p>
    <p class="disclaimer">当サイトはアフィリエイトプログラムに参加しています。</p>
  </div>
</footer>

<script>
// 目次自動生成
document.addEventListener('DOMContentLoaded', () => {{
  const content = document.querySelector('.article-content');
  const toc = document.getElementById('toc');
  const headings = content.querySelectorAll('h2, h3');
  if (headings.length > 2) {{
    let html = '<p class="toc-title">目次</p><ol class="toc-list">';
    headings.forEach((h, i) => {{
      h.id = 'section-' + i;
      const indent = h.tagName === 'H3' ? ' class="toc-sub"' : '';
      html += '<li' + indent + '><a href="#section-' + i + '">' + h.textContent + '</a></li>';
    }});
    html += '</ol>';
    toc.innerHTML = html;
  }}
}});
</script>
</body>
</html>"""

    # 保存
    articles_dir = os.path.join(os.path.dirname(__file__), "..", "articles")
    os.makedirs(articles_dir, exist_ok=True)
    filepath = os.path.join(articles_dir, f"{slug}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 記事生成完了: {filepath}")
    return slug


def update_articles_index():
    """記事一覧のJSONインデックスを更新"""
    articles_dir = os.path.join(os.path.dirname(__file__), "..", "articles")
    index_path = os.path.join(articles_dir, "index.json")

    # 既存インデックスを読み込み
    index = []
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)

    # 新しい記事を検出して追加
    existing_slugs = {a["slug"] for a in index}
    for fname in os.listdir(articles_dir):
        if fname.endswith(".html"):
            slug = fname.replace(".html", "")
            if slug not in existing_slugs:
                # HTMLからタイトルとメタ情報を抽出
                fpath = os.path.join(articles_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                title_match = re.search(r"<h1>(.*?)</h1>", content)
                date_match = re.search(r'datetime="(\d{4}-\d{2}-\d{2})"', content)
                cat_match = re.search(r'class="article-cat-badge">(.*?)</span>', content)
                title = title_match.group(1) if title_match else slug
                date = date_match.group(1) if date_match else ""
                category = cat_match.group(1) if cat_match else ""
                index.append({
                    "slug": slug,
                    "title": title,
                    "date": date,
                    "category": category,
                    "url": f"articles/{slug}.html",
                })

    # 日付でソート（新しい順）
    index.sort(key=lambda a: a.get("date", ""), reverse=True)

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"✅ インデックス更新: {len(index)}件")
    return index


def main():
    print("🚀 alogo-money.dev 記事自動生成スタート")
    print(f"   モデル: {MODEL}")
    print(f"   日時: {datetime.datetime.now()}")
    print()

    # テーマ選定
    topic = pick_topic()
    print(f"📝 テーマ: {topic['title']}")
    print(f"   カテゴリ: {topic['category']}")
    print(f"   タグ: {', '.join(topic['tags'])}")
    print()

    # 記事生成
    article = generate_article(topic)
    print("✍️  記事生成完了")

    # 保存
    slug = save_article(article)

    # インデックス更新
    update_articles_index()

    # SNS投稿用テキスト出力
    sns_text = f"""📝 新着記事を公開しました！

{article['title']}

👉 {SITE_URL}/articles/{slug}.html

{' '.join('#' + t for t in article['tags'][:5])} #副業 #在宅ワーク"""
    print(f"\n📱 SNS投稿テキスト:\n{sns_text}")

    # SNSテキストをファイルに保存（GitHub Actionsで使う）
    sns_path = os.path.join(os.path.dirname(__file__), "..", "latest_sns.txt")
    with open(sns_path, "w", encoding="utf-8") as f:
        f.write(sns_text)

    print("\n🎉 全工程完了！")


if __name__ == "__main__":
    main()
