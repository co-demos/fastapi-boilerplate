import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

# resolve current path / parents / ... for pipenv calll
import os, sys
current_dir = os.path.dirname(os.path.realpath(__file__))
relative_path = os.path.join(current_dir, '..')
sys.path.append(relative_path)

from sql_app.db.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
  stop=stop_after_attempt(max_tries),
  wait=wait_fixed(wait_seconds),
  before=before_log(logger, logging.INFO),
  after=after_log(logger, logging.WARN),
)
def init() -> None:
  try:
    db = SessionLocal()
    # Try to create session to check if DB is awake
    db.execute("SELECT 1")
  except Exception as e:
    logger.error(e)
    raise e


def main() -> None:
  logger.info("Initializing service")
  init()
  logger.info("Service finished initializing")


if __name__ == "__main__":
  main()
