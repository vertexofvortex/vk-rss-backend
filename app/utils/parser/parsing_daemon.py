import threading
import time

from app.crud import CRUD
from app.db.database import SessionLocal
from app.settings import settings
from app.utils.parser.parser import Parser


class ParsingDaemon:
    def __init__(self) -> None:
        self.parser = Parser()
        self.thread = threading.Thread(target=self.parse)
        self.interval = settings.BG_PARSING_INTERVAL_SECONDS

    def parse(self):
        db = SessionLocal()

        while True:
            print("Background parsing started...")

            sources = CRUD.rss_sources_methods.get_all_sources(db)
            posts = self.parser.parseSync(sources)

            CRUD.rss_posts_methods.create_posts(db, posts)

            print(
                f"Background parsing complete. There are {len(posts)} posts in DB. The next parsing is scheduled in {int(self.interval / 60)} minutes."
            )

            time.sleep(self.interval)

    def start(self):
        self.thread.start()
