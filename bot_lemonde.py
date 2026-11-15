import os
import feedparser
import requests

RSS_URL = "https://www.lemonde.fr/rss/une.xml"
# Tu peux réutiliser le même salon Discord ou créer un 2e secret DISCORD_WEBHOOK_LEMONDE
WEBHOOK_DISCORD = os.environ.get("DISCORD_WEBHOOK_LEMONDE")

feed = feedparser.parse(RSS_URL)

for entry in feed.entries[:3]:
    titre = entry.title
    lien = entry.link
    resume = entry.get("summary", "")

    requests.post(
        WEBHOOK_DISCORD,
        json={
            "embeds": [{
                "title": titre[:256],
                "url": lien,
                "description": resume[:300] + "...",
                "color": 1122867,
            }]
        },
    )
