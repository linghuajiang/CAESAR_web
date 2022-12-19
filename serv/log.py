"""HiRes server log."""
import os
import logging
import hirespy

# Config logger
PATH = hirespy.app.config['LOG_FOLDER']
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s \
- %(name)s \
- %(levelname)s \
- %(message)s')

# Add file handler
HANDLER = logging.FileHandler(os.path.join(PATH, "log.txt"))
HANDLER.setLevel(logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s \
- %(name)s \
- %(levelname)s \
- %(message)s')
HANDLER.setFormatter(FORMATTER)
logging.getLogger().addHandler(HANDLER)

# Test logger
LOGGER = logging.getLogger(__name__)
LOGGER.warning("Logger initialized.")
