import logging

# resolve current path / parents / ... for pipenv calll
import os, sys
current_dir = os.path.dirname(os.path.realpath(__file__))
relative_path = os.path.join(current_dir, '..')
sys.path.append(relative_path)

from sql_app.db.init_db import init_db
from sql_app.db.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
  db = SessionLocal()
  init_db(db)


def main() -> None:
  logger.info("Creating initial data")
  init()
  logger.info("Initial data created")


if __name__ == "__main__":
  main()
