import logging, sys
from Tools.BasePara import error_log_path

# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(message)s')
# handler.setFormatter(formatter)
#
# ===============
handler = logging.FileHandler(error_log_path)
handler.setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)

logger.addHandler(handler)

# logger.info("Start print log")
# logger.debug("Do something")

# logger.warning("Finish")
