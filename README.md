# alogo-money.dev 自動ブログシステム

副業・在宅ワーク特化のアフィリエイトブログを完全自動運用するシステム。

## 🏗️ アーキテクチャ

```
GitHub Actions (毎日自動実行)
    ↓
OpenRouter API (Claude/GPT) で記事生成
    ↓
アフィリリンク自動挿入 + SEOメタタグ生成
    ↓
HTML生成 → GitHub リポジトリにコミット
    ↓
Cloudflare Workers/Pages でホスティング
    ↓
(オプション) X/Twitter 自動投稿
```

## 📁 ディレクトリ構造

```
.
├── index.html              # トップページ
├── sitemap.xml             # 自動生成サイトマップ
├── robots.txt              # 自動生成
├── articles/               # 生成された記事
│   ├── index.json          # 記事インデックス
│   └── *.html              # 各記事ページ
├── static/
│   └── article.css         # 記事ページ用CSS
├── scripts/
│   ├── generate_article.py # メイン: 記事生成
│   ├── generate_sitemap.py # サイトマップ生成
│   ├── update_index.py     # トップページ更新
│   └── post_sns.py         # SNS自動投稿
└── .github/
    └── workflows/
        └── generate.yml    # GitHub Actions 自動実行
```

## 🚀 セットアップ手順

### 1. GitHub Secrets を設定

リポジトリの `Settings` → `Secrets and variables` → `Actions` で以下を設定:

**必須:**
| Secret名 | 説明 |
|-----------|------|
| `OPENROUTER_API_KEY` | OpenRouter の APIキー |

**アフィリエイトリンク (任意・後から設定OK):**
| Secret名 | 説明 |
|-----------|------|
| `AFF_CROWDWORKS` | CrowdWorks アフィリリンクURL |
| `AFF_LANCERS` | Lancers アフィリリンクURL |
| `AFF_COCONALA` | ココナラ アフィリリンクURL |
| `AFF_LEVTECH` | レバテック アフィリリンクURL |
| `AFF_SHELIKES` | SHElikes アフィリリンクURL |
| `AFF_MACROMILL` | マクロミル アフィリリンクURL |
| `AFF_A8` | A8.net アフィリリンクURL |
| `AFF_MOSHIMO` | もしもアフィリエイト アフィリリンクURL |
| `AFF_SBIFX` | SBI FXトレード アフィリリンクURL |
| `AFF_COINCHECK` | Coincheck アフィリリンクURL |

**SNS自動投稿 (任意):**
| Secret名 | 説明 |
|-----------|------|
| `TWITTER_API_KEY` | X/Twitter API Key |
| `TWITTER_API_SECRET` | X/Twitter API Secret |
| `TWITTER_ACCESS_TOKEN` | X/Twitter Access Token |
| `TWITTER_ACCESS_SECRET` | X/Twitter Access Secret |

### 2. Variables を設定 (任意)

`Settings` → `Secrets and variables` → `Actions` → `Variables` タブ:

| Variable名 | 説明 | デフォルト |
|-------------|------|-----------|
| `MODEL` | 使用するAIモデル | `anthropic/claude-sonnet-4-20250514` |

おすすめモデル:
- `anthropic/claude-sonnet-4-20250514` (高品質・バランス◎)
- `anthropic/claude-haiku-3.5` (安い・速い)
- `google/gemini-2.0-flash-001` (コスパ最強)
- `openai/gpt-4o-mini` (安い)

### 3. GitHub Actions を有効化

リポジトリの `Actions` タブで Workflow を有効化。

### 4. 手動実行テスト

`Actions` → `🚀 ブログ記事自動生成 & デプロイ` → `Run workflow` で手動実行してテスト。

## ⏰ 自動実行スケジュール

- **毎日 JST 9:00** に自動実行（1記事生成）
- 手動で実行する場合は最大3記事まで同時生成可能

cron を変更する場合は `.github/workflows/generate.yml` を編集:
```yaml
schedule:
  - cron: '0 0 * * *'     # 毎日9時(JST)
  - cron: '0 0 * * 1,4'   # 月・木の9時(JST) に変更する例
```

## 💰 ランニングコスト

| 項目 | コスト |
|------|--------|
| Cloudflare Workers/Pages | 無料 |
| GitHub Actions | 無料 (月2000分) |
| OpenRouter API (Claude Sonnet) | 約$0.01〜0.03/記事 |
| OpenRouter API (Gemini Flash) | ほぼ無料 |
| **合計 (月30記事)** | **約$0.3〜1.0/月** |

## 📝 カスタマイズ

### 記事テーマを追加
`scripts/generate_article.py` の `ARTICLE_TOPICS` リストに追加。

### アフィリリンクを追加
`scripts/generate_article.py` の `AFFILIATE_LINKS` に追加。

### デザインを変更
- トップページ: `index.html`
- 記事ページ: `static/article.css`
