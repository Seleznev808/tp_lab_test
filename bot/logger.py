import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log',
    encoding='utf-8'
)
logging.getLogger().setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
