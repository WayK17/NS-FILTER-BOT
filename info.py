# No Eliminar Créditos @VJ_Botz
# Suscríbete al Canal de YouTube Para Bots Increíbles @Tech_VJ
# Consulta Dudas en Telegram @KingVJ01


import re
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')

# Información del Bot
SESSION = environ.get('SESSION', 'TechVJBot')
API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', "")


# Estas Imágenes Son Para El Mensaje de Inicio, Puedes Agregar Múltiples Separándolas Con Un Espacio.
PICS = (environ.get('PICS', 'https://graph.org/file/ce1723991756e48c35aa1.jpg')).split()


# Administradores y Usuarios
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()] # Para Múltiples IDs Usa Un Espacio Entre Cada Uno.
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]  # Para Múltiples IDs Usa Un Espacio Entre Cada Uno.
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

# Este Canal Es Para Cuando Un Usuario Inicia Tu Bot, El Bot Envía Ese Nombre De Usuario E ID A Este Canal De Registro, Igual Para Grupos.
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', ''))

# Este Es El Canal De Archivos Donde Subes Tu Archivo Y El Bot Automáticamente Lo Guarda En La Base De Datos
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '').split()]  # Para Múltiples IDs Usa Un Espacio Entre Cada Uno.

# auth_channel significa canal de suscripción forzada.
# Si REQUEST_TO_JOIN_MODE es verdadero, entonces la suscripción forzada funciona como solicitud para unirse, si es falso funciona como suscripción forzada normal.
REQUEST_TO_JOIN_MODE = bool(environ.get('REQUEST_TO_JOIN_MODE', False)) # Establecer True o False
TRY_AGAIN_BTN = bool(environ.get('TRY_AGAIN_BTN', False)) # Establecer True o False (Este botón de intentar de nuevo es solo para solicitud de unión, no para suscripción forzada normal)

# Este Es El Canal De Suscripción Forzada, también conocido como Canal de Autorización
auth_channel = environ.get('AUTH_CHANNEL', '') # coloca tu ID de canal de suscripción forzada aquí, déjalo en blanco si no lo usas
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# Este Canal Es Para Cuando El Usuario Solicita Cualquier Nombre De Archivo Con Comando o Hashtag como - /solicitud o #solicitud
reqst_channel = environ.get('REQST_CHANNEL', '')
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None

# Este Canal Es Para Solicitudes De Índice
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))

# Este Es El ID De Tu Grupo De Soporte Del Bot, Aquí El Bot No Dará Archivos Porque Es Un Grupo De Soporte.
support_chat_id = environ.get('SUPPORT_CHAT_ID', '')
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None

# Este Canal Es Para Almacenar Archivos Del Comando /batch.
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]  # Para Múltiples IDs Usa Un Espacio Entre Cada Uno.

# Este Canal Es Para Eliminar Archivos Del Índice, Reenvía Tu Archivo A Este Canal Que Deseas Eliminar Y El Bot Automáticamente Lo Eliminará De La Base De Datos.
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]  # Para Múltiples IDs Usa Un Espacio Entre Cada Uno.


# Información de MongoDB
DATABASE_URI = environ.get('DATABASE_URI', "")   # Si Múltiples Bases De Datos Es Falso, Entonces Llena Solo Esta URL De Base De Datos.
DATABASE_NAME = environ.get('DATABASE_NAME', "techvjclonefilterbot")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'vjcollection')

MULTIPLE_DATABASE = bool(environ.get('MULTIPLE_DATABASE', False)) # Establecer True o False

# Si Múltiples Bases De Datos Es Verdadero, Entonces Llena Las Tres URLs De Base De Datos A Continuación, De Lo Contrario Obtendrás Un Error.
O_DB_URI = environ.get('O_DB_URI', "")   # Esta Base De Datos Es Para Almacenar Otros Datos
F_DB_URI = environ.get('F_DB_URI', "")   # Esta Base De Datos Es Para Almacenar Datos De Archivos
S_DB_URI = environ.get('S_DB_URI', "")   # Esta Base De Datos Es Para Almacenar Datos De Archivos Cuando La Primera Base De Datos Esté Llena.


# Configuración Premium y de Referidos
PREMIUM_AND_REFERAL_MODE = bool(environ.get('PREMIUM_AND_REFERAL_MODE', True)) # Establecer True o False

# Si PREMIUM_AND_REFERAL_MODE es True Entonces Llena Las Variables A Continuación, Si Es False No Es Necesario Llenarlas.
REFERAL_COUNT = int(environ.get('REFERAL_COUNT', '20')) # número de cuenta de referidos
REFERAL_PREMEIUM_TIME = environ.get('REFERAL_PREMEIUM_TIME', '1mes') # tiempo en semana, día, mes.
PAYMENT_QR = environ.get('PAYMENT_QR', 'https://graph.org/file/ce1723991756e48c35aa1.jpg') # URL de imagen del código de pago.
PAYMENT_TEXT = environ.get('PAYMENT_TEXT', '<b>- PLANES DISPONIBLES - \n\n- 30Rs - 1 semana\n- 50Rs - 1 mes\n- 120Rs - 3 meses\n- 220Rs - 6 meses\n\n🎁 CARACTERÍSTICAS PREMIUM 🎁\n\n○ No necesitas verificar\n○ No necesitas abrir enlaces\n○ Archivos directos\n○ Experiencia sin anuncios\n○ Enlaces de descarga de alta velocidad\n○ Enlaces de transmisión multiusuario\n○ Películas y series ilimitadas\n○ Soporte completo del administrador\n○ Las solicitudes se completarán en 1h si están disponibles\n\n✨ ID UPI - <code>demo@okxyz</code>\n\nHaz clic para verificar tu plan activo /myplan\n\n💢 Debes enviar captura de pantalla después del pago\n\n‼️ Después de enviar una captura de pantalla, danos tiempo para agregarte a premium</b>')


# Información de Clonación: Si El Modo De Clonación Es Verdadero Entonces El Bot Clona Otros Bots.
CLONE_MODE = bool(environ.get('CLONE_MODE', False)) # Establecer True o False
CLONE_DATABASE_URI = environ.get('CLONE_DATABASE_URI', "") # Necesario Si el modo de clonación es verdadero
PUBLIC_FILE_CHANNEL = environ.get('PUBLIC_FILE_CHANNEL', '') # Nombre de Usuario del Canal Público Sin @ o sin https://t.me/ y El Bot Es Administrador Con Todos Los Derechos.


# Enlaces
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/vj_bot_disscussion')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/vj_botz')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'vj_bot_disscussion') # Enlace de Chat de Soporte Sin https:// o @
OWNER_LNK = environ.get('OWNER_LNK', 'https://t.me/kingvj01')

# True o False
AI_SPELL_CHECK = bool(environ.get('AI_SPELL_CHECK', True))
PM_SEARCH = bool(environ.get('PM_SEARCH', True))
BUTTON_MODE = bool(environ.get('BUTTON_MODE', True))
MAX_BTN = bool(environ.get('MAX_BTN', True))
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', False))
IMDB = bool(environ.get('IMDB', False))
AUTO_FFILTER = bool(environ.get('AUTO_FFILTER', True))
AUTO_DELETE = bool(environ.get('AUTO_DELETE', True))
LONG_IMDB_DESCRIPTION = bool(environ.get("LONG_IMDB_DESCRIPTION", False))
SPELL_CHECK_REPLY = bool(environ.get("SPELL_CHECK_REPLY", True))
MELCOW_NEW_USERS = bool(environ.get('MELCOW_NEW_USERS', True))
PROTECT_CONTENT = bool(environ.get('PROTECT_CONTENT', False))
PUBLIC_FILE_STORE = bool(environ.get('PUBLIC_FILE_STORE', True))
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", False))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))


# Información de Verificación de Token:
VERIFY = bool(environ.get('VERIFY', False))
VERIFY_SHORTLINK_URL = environ.get('VERIFY_SHORTLINK_URL', '')
VERIFY_SHORTLINK_API = environ.get('VERIFY_SHORTLINK_API', '')
VERIFY_TUTORIAL = environ.get('VERIFY_TUTORIAL', '')

# Si Llenas El Segundo Acortador, El Bot Adjuntará Tanto El Primer Como El Segundo Acortador Y Lo Usará Para Verificar.
VERIFY_SECOND_SHORTNER = bool(environ.get('VERIFY_SECOND_SHORTNER', False))
# si verificar segundo acortador es True entonces llena la URL y API a continuación
VERIFY_SND_SHORTLINK_URL = environ.get('VERIFY_SND_SHORTLINK_URL', '')
VERIFY_SND_SHORTLINK_API = environ.get('VERIFY_SND_SHORTLINK_API', '')


# Información de Acortador de Enlaces
SHORTLINK_MODE = bool(environ.get('SHORTLINK_MODE', False)) # Establecer True o False
SHORTLINK_URL = environ.get('SHORTLINK_URL', '')
SHORTLINK_API = environ.get('SHORTLINK_API', '')
TUTORIAL = environ.get('TUTORIAL', '') # Enlace del Video de Cómo Abrir el Acortador, Enlace del Canal Donde Subiste Tu Video.


# Otros
CACHE_TIME = int(environ.get('CACHE_TIME', 1800))
MAX_B_TN = environ.get("MAX_B_TN", "5")
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', '¡Hola mis queridos amigos ❤️')
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)


# Configuración de Opciones
LANGUAGES = ["español", "esp", "malayalam", "mal", "tamil", "tam", "english", "eng", "hindi", "hin", "telugu", "tel", "kannada", "kan"]
SEASONS = ["temporada 1", "temporada 2", "temporada 3", "temporada 4", "temporada 5", "temporada 6", "temporada 7", "temporada 8", "temporada 9", "temporada 10"]
EPISODES = ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29", "E30", "E31", "E32", "E33", "E34", "E35", "E36", "E37", "E38", "E39", "E40"]
QUALITIES = ["360p", "480p", "720p", "1080p", "1440p", "2160p"]
YEARS = ["1900", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]


                           # No Eliminar Créditos @VJ_Botz
                           # Suscríbete al Canal de YouTube Para Bots Increíbles @Tech_VJ
                           # Consulta Dudas en Telegram @KingVJ01


# Transmisión y Descarga En Línea
STREAM_MODE = bool(environ.get('STREAM_MODE', True)) # Establecer True o False

# Si El Modo De Transmisión Es Verdadero Entonces Llena Todas Las Variables Requeridas, Si Es Falso No Las Llenes.
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutos
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://testofvjfilter-1fa60b1b8498.herokuapp.com/")


# Información de Renombrar: Si Es Verdadero Entonces El Bot Renombra El Archivo, Si No, No
RENAME_MODE = bool(environ.get('RENAME_MODE', False)) # Establecer True o False


# Información de Aprobación Automática: Si Es Verdadero Entonces El Bot Aprueba Las Nuevas Solicitudes De Unión Entrantes, Si No, No
AUTO_APPROVE_MODE = bool(environ.get('AUTO_APPROVE_MODE', False)) # Establecer True o False


# Reacciones al Comando de Inicio
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"] #no agregar ningún emoji porque tg no soporta todas las reacciones de emoji


if MULTIPLE_DATABASE == False:
    USER_DB_URI = DATABASE_URI
    OTHER_DB_URI = DATABASE_URI
    FILE_DB_URI = DATABASE_URI
    SEC_FILE_DB_URI = DATABASE_URI
else:
    USER_DB_URI = DATABASE_URI    # Esta Base De Datos es para Almacenar Datos De Usuario
    OTHER_DB_URI = O_DB_URI       # Esta Base De Datos Es Para Almacenar Otros Datos
    FILE_DB_URI = F_DB_URI        # Esta Base De Datos Es Para Almacenar Datos De Archivos
    SEC_FILE_DB_URI = S_DB_URI    # Esta Base De Datos Es Para Almacenar Datos De Archivos Cuando La Primera Base De Datos Esté Llena.


# No Eliminar Créditos @VJ_Botz
# Suscríbete al Canal de YouTube Para Bots Increíbles @Tech_VJ
# Consulta Dudas en Telegram @KingVJ01