import logging
from asyncua import ua

_logger = logging.getLogger(__name__)

# Share variables for files
TEMP_NORMAL_LEVEL = 25.5

POWER_SCALE = 2

status_good = ua.StatusCodes.Good
status_bad = ua.StatusCodes.Bad
