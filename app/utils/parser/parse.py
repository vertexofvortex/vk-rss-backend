import feedparser
import aiohttp
from app.models.rss_post_model import RSSPostModel
from app.schemas.rss_post_schema import RSSPostCreate
from app.schemas.rss_source_schema import RSSSource


class Parser:
    def __init__(self) -> None:
        pass

    def _strip_feed(self, source: RSSSource, feed) -> list[RSSPostCreate]:
        stripped_feed = []

        for item in feed:
            stripped_feed.append(
                RSSPostCreate(
                    source_id=source.id,
                    title=(item.title if hasattr(item, "title") else None),
                    description=(
                        item.description if hasattr(item, "description") else None
                    ),
                    image_url=(
                        item.enclosures[0].href
                        if item.enclosures[0].href.endswith((".png", ".jpg", ".jpg"))
                        else None
                    )
                    if len(item.enclosures) > 0
                    else None,
                    post_url=(item.link if hasattr(item, "link") else None),
                    categories=(item.category if hasattr(item, "category") else None),
                    publish_date=(
                        item.published if hasattr(item, "published") else None
                    ),
                )
            )

        return stripped_feed

    def _checkFeed(self, feed):
        check_results = {
            "total_posts": 0,
            "titles": 0,
            "descriptions": 0,
            "image_urls": 0,
            "post_urls": 0,
            "categories": 0,
            "publish_dates": 0,
        }

        for item in feed:
            check_results["total_posts"] += 1
            if hasattr(item, "title"):
                check_results["titles"] += 1
            if hasattr(item, "description"):
                check_results["descriptions"] += 1
            if hasattr(item, "image_url"):
                check_results["image_urls"] += 1
            if hasattr(item, "post_url"):
                check_results["post_urls"] += 1
            if hasattr(item, "category"):
                check_results["categories"] += 1
            if hasattr(item, "publish_date"):
                check_results["publish_dates"] += 1

        return check_results

    async def parse(self, sources: list[RSSSource]) -> list[RSSPostCreate]:
        posts: RSSPostCreate = []

        for source in sources:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(source.rss_url) as response:
                        print(f"Fetching {source.title} feed...")
                        feed = feedparser.parse(await response.text())
                        stripped_feed = self._strip_feed(source, feed.entries)

                        posts += stripped_feed
            except:
                print(f"An error occured while parsing the next feed: {source.title}")

        return posts

    async def checkFeed(self, source_url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source_url) as response:
                    feed = feedparser.parse(await response.text())
                    check_results = self._checkFeed(feed.entries)

                return check_results
        except:
            return False
