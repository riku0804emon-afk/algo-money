#!/usr/bin/env python3
"""
サイトマップ自動生成スクリプト
記事一覧からsitemap.xmlを生成する
"""

import os
import json
import datetime

SITE_URL = "https://algo-money.dev"


def generate_sitemap():
    base_dir = os.path.join(os.path.dirname(__file__), "..")
    articles_index = os.path.join(base_dir, "articles", "index.json")

    urls = [
        {
            "loc": SITE_URL + "/",
            "lastmod": datetime.datetime.now().strftime("%Y-%m-%d"),
            "changefreq": "daily",
            "priority": "1.0",
        }
    ]

    if os.path.exists(articles_index):
        with open(articles_index, "r", encoding="utf-8") as f:
            articles = json.load(f)
        for article in articles:
            urls.append({
                "loc": f"{SITE_URL}/{article['url']}",
                "lastmod": article.get("date", datetime.datetime.now().strftime("%Y-%m-%d")),
                "changefreq": "monthly",
                "priority": "0.8",
            })

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += "  <url>\n"
        xml += f"    <loc>{url['loc']}</loc>\n"
        xml += f"    <lastmod>{url['lastmod']}</lastmod>\n"
        xml += f"    <changefreq>{url['changefreq']}</changefreq>\n"
        xml += f"    <priority>{url['priority']}</priority>\n"
        xml += "  </url>\n"
    xml += "</urlset>\n"

    sitemap_path = os.path.join(base_dir, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"✅ sitemap.xml 生成完了: {len(urls)}件のURL")

    # robots.txt も生成
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    robots_path = os.path.join(base_dir, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots)
    print("✅ robots.txt 生成完了")


if __name__ == "__main__":
    generate_sitemap()
