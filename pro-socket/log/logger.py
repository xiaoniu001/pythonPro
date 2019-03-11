
import logging.config


logging.config.fileConfig("log/logging.conf")

debug_logger = logging.getLogger("debugLogger")

error_logger = logging.getLogger("errorLogger")