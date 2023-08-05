"""setting module for your project"""
import os
import logging
import asyncio

from ant_nest.exceptions import ExceptionFilter

# your ant`s class modules or packages
ANT_PACKAGES = ["ants"]
ANT_ENV = os.getenv("ANT_ENV", "development")

if ANT_ENV in ("development", "testing"):
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().set_debug(True)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().addFilter(ExceptionFilter())


# custom setting, eg:
# MYSQL_HOST = '127.0.0.1'
