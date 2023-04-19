import threading
import time
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.depends import get_db
from app.crud import CRUD
from app.utils.parser.parser import Parser


class ParsingDaemon:
    def __init__(self) -> None:
        self.parser = Parser()
        self.thread = threading.Thread(target=self.parse)

    def parse(self):
        db = SessionLocal()

        while True:
            print("Background parsing started...")

            sources = CRUD.rss_sources_methods.get_all_sources(db)
            posts = self.parser.parseSync(sources)

            CRUD.rss_posts_methods.create_posts(db, posts)

            print(f"Background parsing complete. There are {len(posts)} posts in DB.")

            time.sleep(900)

    def start(self):
        self.thread.start()
