# coding: utf-8
import sys
from loguru import logger


class BaseSettings:
    logger.remove()
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "\
          "<level>{level}</level> | "\
          "<cyan>{name}</cyan> <line {line}>: <level>{message}</level>"
    logger.add(sys.stdout, format=fmt)
    logger.add('log/aio-crawler.log', format=fmt, rotation='10 MB')
    LOGGER = logger

    REDIS_URL = None
    REDIS_PROJECT_NAME = None

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = None
    MYSQL_DB = None

    CONCURRENT_REQUESTS = 16
    CONCURRENT_WORDS = 16
    DEFAULT_TIMEOUT = 20
    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
    }

    DOWNLOAD_DALEY = 0
    PROCESS_DALEY = 0.01

    ALLOWED_CODES = []

    DOWNLOADER_MIDDLEWARES = []
