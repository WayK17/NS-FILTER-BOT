# No Eliminar Créditos @VJ_Botz
# Suscríbete al Canal de YouTube Para Bots Increíbles @Tech_VJ
# Consulta Dudas en Telegram @KingVJ01

import re
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')

# Información del Bot
SESSION = environ.get('SESSION', 'TechVJBot')
API_ID = int(environ.get('API_ID', '15353803'))  # COMPLETAR CON TU API_ID
API_HASH = environ.get('API_HASH', '0dc88c619c52613806822fd600eec006')   # COMPLETAR CON TU API_HASH
BOT_TOKEN = environ.get('BOT_TOKEN', "6875902533:AAGMgm-VDchnuUqfceSy96Zle5o6RFDU9wk") # COMPLETAR CON TU BOT_TOKEN

# Imágenes para el mensaje de inicio
PICS = (environ.get('PICS', 'https://envs.sh/bu7.jpg')).split()

# Administradores y Usuarios
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

# Configuración de Canales
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '')) # COMPLETAR CON ID DE CANAL DE LOGS
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '').split()]

# Configuración de Suscripción
REQUEST_TO_JOIN_MODE = bool(environ.get('REQUEST_TO_JOIN_MODE', False))
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL', '')) if environ.get('AUTH_CHANNEL') else None

# Configuración de Solicitudes
REQST_CHANNEL = int(environ.get('REQST_CHANNEL', '')) if environ.get('REQST_CHANNEL') else None
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
SUPPORT_CHAT_ID = int(environ.get('SUPPORT_CHAT_ID', '')) if environ.get('SUPPORT_CHAT_ID') else None

# Configuración de Archivos
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]

# Configuración de MongoDB
DATABASE_URI = environ.get('DATABASE_URI', "")    # COMPLETAR CON TU URL DE MONGODB
DATABASE_NAME = environ.get('DATABASE_NAME', "techvjclonefilterbot")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'vjcollection')

# Configuración de Enlaces
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/tu_grupo') # COMPLETAR CON TU ENLACE
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/tu_canal') # COMPLETAR CON TU ENLACE
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'tu_grupo_soporte') # COMPLETAR CON TU GRUPO
OWNER_LNK = environ.get('OWNER_LNK', 'https://t.me/tu_usuario') # COMPLETAR CON TU USUARIO

# Configuración de Funcionalidades
AI_SPELL_CHECK = bool(environ.get('AI_SPELL_CHECK', True))
PM_SEARCH = bool(environ.get('PM_SEARCH', True))
BUTTON_MODE = bool(environ.get('BUTTON_MODE', True))
MAX_BTN = bool(environ.get('MAX_BTN', True))
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', False))
IMDB = bool(environ.get('IMDB', true))
AUTO_FFILTER = bool(environ.get('AUTO_FFILTER', True))
AUTO_DELETE = bool(environ.get('AUTO_DELETE', True))
LONG_IMDB_DESCRIPTION = bool(environ.get("LONG_IMDB_DESCRIPTION", false))
SPELL_CHECK_REPLY = bool(environ.get("SPELL_CHECK_REPLY", True))
MELCOW_NEW_USERS = bool(environ.get('MELCOW_NEW_USERS', True))
PROTECT_CONTENT = bool(environ.get('PROTECT_CONTENT', False))
PUBLIC_FILE_STORE = bool(environ.get('PUBLIC_FILE_STORE', True))
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", False))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Configuración de Acortador
SHORTLINK_MODE = bool(environ.get('SHORTLINK_MODE', False))
SHORTLINK_URL = environ.get('SHORTLINK_URL', '')
SHORTLINK_API = environ.get('SHORTLINK_API', '')
TUTORIAL = environ.get('TUTORIAL', '') # COMPLETAR CON TU TUTORIAL

# Otras Configuraciones
CACHE_TIME = int(environ.get('CACHE_TIME', 1800))
MAX_B_TN = environ.get("MAX_B_TN", "5")
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', '¡Hola mis queridos amigos ❤️')
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)

# Transmisión y Descarga
STREAM_MODE = bool(environ.get('STREAM_MODE', True))
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
ON_HEROKU = 'DYNO' in environ
URL = environ.get("URL", "https://tuapp.herokuapp.com/") # COMPLETAR CON TU URL

# Configuración Adicional
RENAME_MODE = bool(environ.get('RENAME_MODE', False))
AUTO_APPROVE_MODE = bool(environ.get('AUTO_APPROVE_MODE', False))
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]

if MULTIPLE_DATABASE == False:
    USER_DB_URI = DATABASE_URI
    OTHER_DB_URI = DATABASE_URI
    FILE_DB_URI = DATABASE_URI
    SEC_FILE_DB_URI = DATABASE_URI
else:
    USER_DB_URI = DATABASE_URI
    OTHER_DB_URI = O_DB_URI
    FILE_DB_URI = F_DB_URI
    SEC_FILE_DB_URI = S_DB_URI