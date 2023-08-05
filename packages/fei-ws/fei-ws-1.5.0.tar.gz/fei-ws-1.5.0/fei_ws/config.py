import logging

FEI_WS_USERNAME = ''
FEI_WS_PASSWORD = ''
FEI_WS_BASE_URL = 'https://data.fei.org/'

logger = logging.getLogger('fei-ws.client')

try:
    from django.conf import settings
    if hasattr(settings, 'FEI_BASE_URL'):
        FEI_WS_BASE_URL = settings.FEI_WS_BASE_URL
    if hasattr(settings, 'FEI_WS_USERNAME'):
        FEI_WS_USERNAME = settings.FEI_WS_USERNAME
    if hasattr(settings, 'FEI_WS_PASSWORD'):
        FEI_WS_PASSWORD = settings.FEI_WS_PASSWORD
except ImportError as e:
    logger.info('Could not load django.conf')

