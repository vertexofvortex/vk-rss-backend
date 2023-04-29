import threading
import time

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.crud import CRUD
from app.db.database import SessionLocal
from app.models.rss_post_model import RSSPostModel
from app.settings import settings
from app.utils.parser.parser import Parser


class ParsingDaemon:
    def __init__(self) -> None:
        self.parser = Parser()
        self.thread = threading.Thread(target=self.parse)
        self.parsing_interval = settings.BG_PARSING_INTERVAL_SECONDS
        self.cleanup_interval = settings.BG_CLEANUP_INTERVAL_SECONDS
        self.db = SessionLocal()

    def parse(self):
        while True:
            print("Background parsing started...")

            sources = CRUD.rss_sources_methods.get_all_sources(self.db)
            posts = self.parser.parseSync(sources)

            CRUD.rss_posts_methods.create_posts(self.db, posts)

            print(
                f"Background parsing completed. There are {len(posts)} posts in DB. The next parsing is scheduled in {int(self.parsing_interval / 60)} minutes."
            )

            self.cleanup(len(posts))

            time.sleep(self.parsing_interval)

    def cleanup(self, posts_was_count: int):
        print(
            f"Old posts cleanup started, removing posts older than {int(self.cleanup_interval / 3600)} hours..."
        )

        posts_became_count = CRUD.rss_posts_methods.clear_old_posts(self.db)

        print(
            f"Posts cleanup completed, {posts_was_count - posts_became_count} posts removed, {posts_became_count} is now in the database."
        )

    def start(self):
        self.thread.start()
