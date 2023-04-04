import feedparser
import aiohttp
from app.models.rss_post import RSSPost
from app.schemas.rss_post import RSSPostCreate
from app.schemas.rss_source import RSSSource


class Parser():
    def __init__(self) -> None:
        pass

    def _strip_feed(self, source: RSSSource, feed) -> RSSPostCreate:
        stripped_feed = []

        for item in feed:
            stripped_feed.append(RSSPostCreate(
                source_id = source.id,
                title= (
                    item.title
                    if hasattr(item, "title")
                    else None
                ),
                description = (
                    item.description
                    if hasattr(item, "description")
                    else None
                ),
                image_url = (
                    item.enclosures[0].href
                    if item.enclosures[0].href.endswith((".png", ".jpg", ".jpg"))
                    else None
                ) if len(item.enclosures) > 0 else None,
                post_url = (
                    item.link
                    if hasattr(item, "link")
                    else None
                ),
                categories = (
                    item.category
                    if hasattr(item, "category")
                    else None
                ),
                publish_date = (
                    item.published
                    if hasattr(item, "published")
                    else None
                ),
            ))
        
        return stripped_feed


    async def parse(self, sources: list[RSSSource]) -> list[RSSPostCreate]:
        posts: RSSPostCreate = []

        for source in sources:
            async with aiohttp.ClientSession() as session:
                async with session.get(source.rss_url) as response:
                    feed = feedparser.parse(await response.text())
                    stripped_feed = self._strip_feed(source, feed.entries)
                    
                    # feeds.append({
                    #     "name": source.title,
                    #     #"description": feed.feed.description if hasattr(feed.feed, "description") else None,
                    #     "description": source.description,
                    #     "rss_url": source.rss_url,
                    #     "items": stripped_feed,
                    # })

                    posts += stripped_feed

        return posts