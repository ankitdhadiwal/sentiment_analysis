
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(override=True)


class NewsFetcher:

    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")

    def fetch_from_newsapi(self, ticker, days=7):
        """Fetch stock news from NewsAPI."""

        from_date = (
            datetime.now() - timedelta(days=days)
        ).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"

        params = {
            "q": f"{ticker} stock",
            "from": from_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": self.newsapi_key
        }

        try:
            print(f"Fetching news for {ticker}...", flush=True)

            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            data = response.json()

            print(f"NewsAPI Status: {response.status_code}", flush=True)

            if response.status_code == 200:
                articles = data.get("articles", [])

                print(f"Articles received: {len(articles)}", flush=True)

                return articles

            print(f"NewsAPI Error: {data.get('message')}")
            return []

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def fetch_stock_news(self, ticker):
        """Fetch, clean and deduplicate stock news."""

        ticker = ticker.strip().upper()

        ticker_mapping = {
            "APPLE": "AAPL",
            "GOOGLE": "GOOGL",
            "MICROSOFT": "MSFT",
            "TESLA": "TSLA",
            "AMAZON": "AMZN",
            "NVIDIA": "NVDA",
            "META": "META"
        }

        ticker = ticker_mapping.get(ticker, ticker)

        api_articles = self.fetch_from_newsapi(ticker)

        unique_articles = []
        titles = set()

        for article in api_articles:

            title = article.get("title") or ""
            description = article.get("description") or ""
            content = article.get("content") or ""

            if not title or title == "[Removed]":
                continue

            if title in titles:
                continue

            combined_content = " ".join(
                [title, description, content]
            ).strip()

            article["content"] = combined_content

            titles.add(title)
            unique_articles.append(article)

        print(
            f"Returning {len(unique_articles)} articles for {ticker}",
            flush=True
        )

        return unique_articles

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(override=True)


class NewsFetcher:

    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")

    def fetch_from_newsapi(self, ticker, days=7):
        """Fetch stock news from NewsAPI."""

        from_date = (
            datetime.now() - timedelta(days=days)
        ).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"

        params = {
            "q": f"{ticker} stock",
            "from": from_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": self.newsapi_key
        }

        try:
            print(f"Fetching news for {ticker}...", flush=True)

            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            data = response.json()

            print(f"NewsAPI Status: {response.status_code}", flush=True)

            if response.status_code == 200:
                articles = data.get("articles", [])

                print(f"Articles received: {len(articles)}", flush=True)

                return articles

            print(f"NewsAPI Error: {data.get('message')}")
            return []

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def fetch_stock_news(self, ticker):
        """Fetch, clean and deduplicate stock news."""

        ticker = ticker.strip().upper()

        ticker_mapping = {
            "APPLE": "AAPL",
            "GOOGLE": "GOOGL",
            "MICROSOFT": "MSFT",
            "TESLA": "TSLA",
            "AMAZON": "AMZN",
            "NVIDIA": "NVDA",
            "META": "META"
        }

        ticker = ticker_mapping.get(ticker, ticker)

        api_articles = self.fetch_from_newsapi(ticker)

        unique_articles = []
        titles = set()

        for article in api_articles:

            title = article.get("title") or ""
            description = article.get("description") or ""
            content = article.get("content") or ""

            if not title or title == "[Removed]":
                continue

            if title in titles:
                continue

            combined_content = " ".join(
                [title, description, content]
            ).strip()

            article["content"] = combined_content

            titles.add(title)
            unique_articles.append(article)

        print(
            f"Returning {len(unique_articles)} articles for {ticker}",
            flush=True
        )

        return unique_articles
