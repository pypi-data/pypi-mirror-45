__version__ = '1.0.5'
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info(f'zuper-auth {__version__}')
