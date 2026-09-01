import requests
from bs4 import BeautifulSoup
from email.utils import format_datetime
from datetime import datetime, timezone
from xml.sax.saxutils import escape

URL = "https://iribtv.ir/tag/43987"
BASE_URL = "https://iribtv.ir"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

items = []

for article in soup.select("article.catitemlist"):

    link_tag = article.select_one('a[href^="/news/"]')
    title_tag = article.select_one('h4 a[href^="/news/"]')
    description_tag = article.select_one("h5")

    if not link_tag or not title_tag:
        continue

    link = BASE_URL + link_tag["href"]

    title = title_tag.get_text(" ", strip=True)

    description = (
        description_tag.get_text(" ", strip=True)
        if description_tag else ""
    )

    items.append({
        "title": title,
        "link": link,
        "description": description
    })


rss_items = []

for item in items:

    rss_items.append(f"""
    <item>
        <title>{escape(item["title"])}</title>
        <link>{escape(item["link"])}</link>
        <guid isPermaLink="true">{escape(item["link"])}</guid>
        <description>{escape(item["description"])}</description>
    </item>
    """)


rss = f"""<?xml version="1.0" encoding="UTF-8"?>

<rss version="2.0">

    <channel>

        <title>شبکه مستند - اخبار تگ 43987</title>

        <link>{URL}</link>

        <description>آخرین اخبار مرتبط با تگ 43987</description>

        <language>fa</language>

        <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>

        {''.join(rss_items)}

    </channel>

</rss>
"""


with open("feed.xml", "w", encoding="utf-8") as f:

    f.write(rss)


print(f"RSS generated successfully: {len(items)} items")
