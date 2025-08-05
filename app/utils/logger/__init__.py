import logging

# ================= COMMON FORMATTER =================
formatter = logging.Formatter(
    "[%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# ====================================================

# ================= APPLICATION LOGGER ===============
logger = logging.getLogger("APPLICATION")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
# ====================================================

# ================= ENGINE LOGGER ====================
engineLogger = logging.getLogger("ENGINE")
engineLogger.setLevel(logging.DEBUG)

engineHandler = logging.StreamHandler()
engineHandler.setFormatter(formatter)

engineLogger.addHandler(engineHandler)
# ====================================================
