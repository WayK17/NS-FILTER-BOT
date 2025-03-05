# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

class script(object):
    START_TXT = """<b><blockquote>Hola {} 👋,</blockquote>
    
Soy el Bot de filtro automático más avanzado y poderoso. Puedes usarme en tu Grupo.. </b>"""

    CLONE_START_TXT = """<b><blockquote>Hola {}, mi nombre es <a href=https://t.me/{}>{}</a></blockquote>
    
Soy un bot de filtro automático avanzado y poderoso con increíbles funciones. Solo escribe lo que quieras y mira mi poder 💘</b>"""

    HELP_TXT = """<b>Hola {}
Aquí están todas mis funciones útiles.</b>"""

    ABOUT_TXT = """<b><blockquote>⍟───[ MIS DETALLES ]───⍟</blockquote>
    
‣ Mi nombre : <a href=https://t.me/{}>{}</a>
‣ Desarrollador : <a href={}>@WayK</a>
‣ Librería : <a href='https://docs.pyrogram.org/'>Pyrogram</a>
‣ Lenguaje : <a href='https://www.python.org/download/releases/3.0/'>Python 3</a>
‣ Base de datos : <a href='https://www.mongodb.com/'>MongoDB</a>
‣ Servidor del bot : <a href='https://heroku.com'>Heroku</a>
‣ Estado de compilación : v2.7.1 [estable]</b>"""

    SUBSCRIPTION_TXT = """
<b>Refiere tu enlace a tus amigos, familia, canal y grupo para obtener premium gratis para {}

Enlace de referido - https://telegram.me/{}?start=VJ-{}

Si un usuario único {} inicia el bot con tu enlace de referido, se añadirá automáticamente a la lista premium.

Compra plan de pago con - /plan</b>"""

    MANUELFILTER_TXT = """Ayuda: <b>Filtros</b>
- Filtro es una función donde los usuarios pueden configurar respuestas automatizadas para una palabra clave en particular y yo responderé cada vez que se encuentre esa palabra en el mensaje.
<b>Nota:</b>
1. Este bot debe tener privilegios de administrador.
2. Solo los administradores pueden agregar filtros en un chat.
3. Los botones de alerta tienen un límite de 64 caracteres.
Comandos y Uso:
• /filter - <code>agregar un filtro en un chat</code>
• /filters - <code>listar todos los filtros de un chat</code>
• /del - <code>eliminar un filtro específico en un chat</code>
• /delall - <code>eliminar todos los filtros en un chat (solo el dueño del chat)</code>"""

    BUTTON_TXT = """Ayuda: <b>Botones</b>
- Este bot soporta botones de URL y botones de alerta en línea.
<b>Nota:</b>
1. Telegram no permitirá enviar botones sin contenido, por lo que el contenido es obligatorio.
2. Este bot soporta botones con cualquier tipo de medio de Telegram.
3. Los botones deben ser correctamente interpretados en formato markdown.
<b>Botones URL:</b>
<code>[Texto del Botón](buttonurl:https://t.me/vjupdates2/3)</code>
<b>Botones de alerta:</b>
<code>[Texto del Botón](buttonalert:Esto es un mensaje de alerta)</code>"""

    AUTOFILTER_TXT = """Ayuda: <b>Auto Filtro</b>
<b>Nota: Índice de archivos</b>
1. Hazme administrador de tu canal si es privado.
2. Asegúrate de que tu canal no contenga contenido para adultos, pornografía ni archivos falsos.
3. Reenvía el último mensaje a mí con comillas. Añadiré todos los archivos de ese canal a mi base de datos.

<b>Nota: AutoFiltro</b>
1. Agrega el bot como administrador en tu grupo.
2. Usa /connect y conecta tu grupo al bot.
3. Usa /settings en el mensaje privado del bot y activa AutoFiltro en el menú de configuración."""

    CONNECTION_TXT = """Ayuda: <b>Conexiones</b>
- Se utiliza para conectar el bot al mensaje privado para gestionar filtros 
- Ayuda a evitar el spam en los grupos.
<b>Nota:</b>
1. Solo los administradores pueden añadir una conexión.
2. Envía <code>/connect</code> para conectar conmigo en tu mensaje privado.
Comandos y Uso:
• /connect  - <code>conectar un chat en particular a tu mensaje privado</code>
• /disconnect  - <code>desconectar de un chat</code>
• /connections - <code>listar todas tus conexiones</code>"""

    EXTRAMOD_TXT = """Ayuda: <b>Módulos Extra</b>
<b>Nota:</b>
 <b>✯ Mantenido por : <a href={}>Elaina</a></b>
  
 <b>✯ Únete aquí : <a href={}>https://t.me/NessCloud</a></b>
  
 ./id - <code>obtener el ID de un usuario especificado.</code>
  
 ./info  - <code>obtener información sobre un usuario.</code>
  
 ./song - Descargar cualquier canción [<code>ejemplo /song vaa vaathi song</code>]
  
 ./telegraph - <code>Generador de Telegraph para enviar video o foto menores a 5MB; te doy el enlace de Telegraph</code>
  
 ./tts - <code>Este comando convierte texto a voz</code>
  
 ./video - Este comando descarga cualquier video de YouTube en HD [<code>ejemplo /video https://youtu.be/example...</code>]

./font - Este comando genera fuentes elegantes y modernas [<code>ejemplo /font hi</code>]"""

    ADMIN_TXT = """Ayuda: Módulos de Admin
<b>Nota:</b>
Este módulo solo funciona para mis administradores
Comandos y Uso:
• /logs - <code>para obtener los errores recientes</code>
• /stats - <code>para obtener el estado de archivos en la base de datos. [Este comando puede ser usado por cualquiera]</code>
• /delete - <code>para eliminar un archivo específico de la base de datos.</code>
• /users - <code>para obtener la lista de mis usuarios e IDs.</code>
• /chats - <code>para obtener la lista de mis chats e IDs</code>
• /leave  - <code>para salir de un chat.</code>
• /disable  -  <code>para deshabilitar un chat.</code>
• /ban  - <code>para banear a un usuario.</code>
• /unban  - <code>para desbanear a un usuario.</code>
• /channel - <code>para obtener la lista de todos los canales conectados</code>
• /broadcast - <code>para difundir un mensaje a todos los usuarios</code>
• /grp_broadcast - <code>para difundir un mensaje a todos los grupos conectados.</code>
• /gfilter - <code>para agregar filtros globales</code>
• /gfilters - <code>para ver la lista de todos los filtros globales</code>
• /delg - <code>para eliminar un filtro global específico</code>
• /request - <code>para enviar una solicitud de película/series a los administradores del bot. Solo funciona en el grupo de soporte. [Este comando puede ser usado por cualquiera]</code>
• /delallg - <code>para eliminar todos los filtros globales de la base de datos del bot.</code>
• /deletefiles - <code>para eliminar archivos de CamRɪᴘ y PreDVD de la base de datos del bot.</code>"""

    SEC_STATUS_TXT = """<b>★ Total de Usuarios: <code>{}</code>
★ Total de Chats: <code>{}</code>
★ Total de Archivos: <code>{}</code>
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Gratis: <code>{} MB</code></b>"""

    STATUS_TXT = """<b>Total de Archivos de Todas las Bases de Datos: <code>{}</code>

BASE DE USUARIOS :-
★ Total de Usuarios: <code>{}</code>
★ Total de Chats: <code>{}</code>

PRIMERA BASE DE ARCHIVOS :-
★ Total de Archivos: <code>{}</code>
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Gratis: <code>{} MB</code>

SEGUNDA BASE DE ARCHIVOS :-
★ Total de Archivos: <code>{}</code>
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Gratis: <code>{} MB</code>

OTRA BASE DE DATOS :-
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Gratis: <code>{} MB</code></b>"""

    LOG_TEXT_G = """#NuevoGrupo
Grupo = {} (<code>{}</code>)
Total de Miembros = <code>{}</code>
Añadido por - {}"""

    LOG_TEXT_P = """#NuevoUsuario
ID - <code>{}</code>
Nombre - {}"""

    ALRT_TXT = """Hola {},
esto no es tu solicitud de película,
solicita la tuya..."""

    OLD_ALRT_TXT = """Hey {},
estás usando uno de mis mensajes antiguos, 
por favor envía la solicitud de nuevo."""

    CUDNT_FND = """No pude encontrar nada relacionado con {}
¿Querías decir alguno de estos?"""

    I_CUDNT = """<b>Lo siento, no se encontraron archivos para tu solicitud {} 😕
  
Revisa tu ortografía en Google y prueba de nuevo 😃

Formato de solicitud de película 👇

Ejemplo : Uncharted o Uncharted 2022 o Uncharted En

Formato de solicitud de series 👇

Ejemplo : Loki S01 o Loki S01E04 o Lucifer S03E24

🚯 No uses ➠ ':(!,./</b>"""

    I_CUD_NT = """No pude encontrar ninguna película relacionada con {}.
Por favor, revisa la ortografía en Google o IMDb..."""

    MVE_NT_FND = """Película no encontrada en la base de datos..."""

    TOP_ALRT_MSG = """Buscando película en la base de datos..."""

    MELCOW_ENG = """<b>Hola {} 😍, y bienvenido al grupo {} ❤️</b>"""

    SHORTLINK_INFO = """

🫵 No hay nada de Información"""

    REQINFO = """
⚠ INFORMACIÓN ⚠

Después de 5 minutos este mensaje se eliminará automáticamente.

Si no ves el archivo de película/serie solicitado, revisa la siguiente página"""  # ✅ Correcto

    SELECT = """SELECCIONA tu idioma preferido, calidad, temporada y episodio"""

    SINFO = """
🫣 Para la película, únete primero y luego haz clic en el botón "Inténtalo de nuevo" 😅"""

    NORSLTS = """ 
★ #SIN RESULTADOS ★

ID <b>: {}</b>

Nombre <b>: {}</b>

Mensaje <b>: {}</b>"""

    CAPTION = """<b>📂 Nombre del Archivo: {file_name}

⚙️ Tamaño: {file_size}</b>"""

    IMDB_TEMPLATE_TXT = """
<b>Resultado de Búsqueda 🔍: {qurey}
🎬 | IMDB Detalles:
━━━━━━━━━━━━━━━
🏷 | <b>Título</b>: <a href={url}>{title}</a>
🎭 | Géneros: {genres}
📆 | Año: <a href={url}/releaseinfo>{year}</a>
🌟 | Calificación: <a href={url}/ratings>{rating}</a> / 10 (basado en {votes} valoraciones de usuarios.)
☀️ | Idioma: <code>{languages}</code>
📀 | Duración: {runtime} minutos
📆 | Fecha de lanzamiento: {release_date}
🎛 | País: <code>{countries}</code>
━━━━━━━━━━━━━━━
⏰ Resultado mostrado en: {remaining_seconds} <i>segundos</i> 🔥
━━━━━━━━━━━━━━━
📨 | Solicitado Por: {message.from_user.mention}</b>"""

    ALL_FILTERS = """
<b>Hola {}, estos son mis tres tipos de filtros.</b>"""

    GFILTER_TXT = """
<b>Bienvenido a los Filtros Globales. Los filtros globales son aquellos establecidos por los administradores del bot que funcionarán en todos los grupos.</b>
    
Comandos disponibles:
• /gfilter - <code>Para crear un filtro global.</code>
• /gfilters - <code>Para ver todos los filtros globales.</code>
• /delg - <code>Para eliminar un filtro global en particular.</code>
• /delallg - <code>Para eliminar todos los filtros globales.</code>"""

    FILE_STORE_TXT = """
<b>El Almacenamiento de Archivos es la función que creará un enlace compartible para un solo archivo o múltiples archivos.</b>

Comandos disponibles:
• /batch - <code>Para crear un enlace de lote de múltiples archivos.</code>
• /link - <code>Para crear un enlace de almacenamiento para un solo archivo.</code>
• /pbatch - <code>Similar a /batch, pero los archivos se enviarán con restricciones de reenvío.</code>
• /plink - <code>Similar a /link, pero el archivo se enviará con restricciones de reenvío.</code>"""

    SONG_TXT = """<b>Módulo de Descarga de Canciones</b> 
      
<b>Módulo de descarga de canciones, para aquellos que aman la música. Puedes usar esta función para descargar cualquier canción a súper velocidad. Funciona solo en bot y grupos...</b> 
  
<b>Comandos</b>: <b>𝄟⃝.  /song nombre de la canción</b>"""

    YTDL_TXT = """<b>Ayuda para descargar videos desde YouTube. 

Uso: Puedes descargar cualquier video desde YouTube.
  
Cómo usar: escribe - /video o /mp4
  
Ejemplo: <code>/mp4 https://youtu.be/example...</code></b>"""

    TTS_TXT = """<b>Módulo TTS 🎤: Convierte texto a voz.
  
Comandos y uso: /tts</b>"""

    GTRANS_TXT = """<b>Ayuda: Traductor de Google
  
Este comando te ayuda a traducir un texto a cualquier idioma que desees. Funciona tanto en mensajes privados como en grupos.
  
Comandos y uso: /tr - para traducir textos a un idioma específico.
  
Nota: al usar /tr, debes especificar el código del idioma.
  
Ejemplo: /tr ml 
 • en = inglés 
 • ml = malayalam 
 • hi = hindi</b>"""

    TELE_TXT = """<b>Ayuda: Módulo Telegraph de Telegram
  
Uso: /telegraph - Envíame una imagen o video (menos de 5MB)
  
Nota:
Este comando está disponible en grupos y mensajes privados.
Puede ser usado por cualquier persona</b>"""

    CORONA_TXT = """<b>Ayuda: Covid
  
Este comando te ayuda a obtener información diaria sobre el Covid.
  
Comandos y uso: 
 /covid - Usa este comando seguido del nombre de tu país para obtener información sobre Covid.
 Ejemplo: <code>/covid India</code>
  
⚠️ Este servicio ha sido detenido.
  
</b>"""

    PROGRESS_BAR = """\n
╭━━━━❰ Renombrando Archivo... ❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """

    ABOOK_TXT = """<b>Ayuda: Audiolibro
  
Puedes convertir un archivo PDF a un archivo de audio usando este comando ✯ 
  
Comandos y uso: 
/audiobook: Responde a este comando en cualquier PDF para generar el audio
</b>"""

    PINGS_TXT = """<b>Prueba de Ping: te ayuda a conocer tu ping 🪄 
  
Comandos: 
 • /alive - para verificar que estás activo. 
 • /help - para obtener ayuda. 
 • /ping - para obtener tu ping.
  
Uso: 
 • Estos comandos pueden usarse en mensajes privados y en grupos.
 • Estos comandos pueden ser usados por cualquiera en grupos y en mensajes privados.
 • Comparte con nosotros para más funciones
</b>"""

    STICKER_TXT = """<b>Puedes usar este módulo para encontrar cualquier ID de sticker.
  
Uso: para obtener el ID del sticker, simplemente escribe: /stickerid
</b>"""

    FONT_TXT = """<b>Uso:
Puedes usar este módulo para cambiar el estilo de la fuente.
  
Comando: /font tu texto (opcional)
Ejemplo: /font hola
</b>"""

    PURGE_TXT = """<b>Purgar

Elimina muchos mensajes de los grupos!
(Administrador)

◉ /purge: elimina todos los mensajes desde el mensaje al que respondes hasta el mensaje actual.</b>"""

    WHOIS_TXT = """<b>Módulo Whois

Nota: Proporciona detalles de un usuario.
Uso: /whois para obtener detalles completos de un usuario 📑
</b>"""

    JSON_TXT = """<b>
JSON:
El bot devuelve JSON para todos los mensajes respondidos con /json.

Funciones:

- Edición de mensajes en JSON
- Soporte en mensajes privados
- Soporte en grupos

Nota:

Todos pueden usar este comando; si se produce spam, el bot te baneará automáticamente del grupo.
</b>"""

    URLSHORT_TXT = """<b>Ayuda: Acortador de URL
  
<i><b>Este comando te ayuda a acortar URLs.</b></i>
  
Comandos y uso:
  
/short: <b>Usa este comando con tu enlace para obtener un enlace corto.</b>
Ejemplo: <code>/short https://youtu.be/example...</code>
</b>"""

    CARB_TXT = """<b>Ayuda para Carbon

Carbon es una función que hace que la imagen se muestre en la parte superior con tus textos.
Para usar este módulo, simplemente envía el texto y ejecútalo con el comando /carbon; el bot responderá con la imagen de Carbon.
</b>"""

    GEN_PASS = """<b>Ayuda: Generador de Contraseñas
  
No hay nada más que saber. Envíame el límite de tu contraseña.
- Te proporcionaré una contraseña con ese límite.
  
Comandos y uso: 
• /genpassword o /genpw 20
  
NOTA: 
• Solo se permiten dígitos.
• El máximo permitido es hasta 64.
  (No puedo generar contraseñas de longitud superior a 64)
• IMDb debe tener privilegios de administrador.
• Estos comandos funcionan tanto en mensajes privados como en grupos.
• Estos comandos pueden ser usados por cualquier miembro de grupo.</b>"""

    SHARE_TXT = """<b>Obtén tu URL para compartir texto.
  
Ejemplo: /share
</b>"""

    PIN_TXT = """<b>Módulo de Fijación
  
Fija un mensaje...
Todos los comandos relacionados con fijar mensajes se pueden encontrar aquí:
  
📌 Comandos y uso 📌 
  
/pin : para fijar el mensaje en tus chats 
/unpin : para quitar la fijación del mensaje actual</b>"""

    RESTART_TXT = """
<b>¡El bot se ha reiniciado!

📅 | Fecha: <code>{}</code>
⏰ | Hora <code>{}</code>
🌐 | Zona horaria: <code>Asia/Kolkata</code>
🛠️ | Estado de compilación: <code>v2.7.1 [Estable]</code></b>"""

    LOGO = """
████████╗███████╗███████╗██╗  ██╗    ╔██        ██╗       ██╗
╚═ ██╔══╝██╔════╝██╔════╝██║  ██║     ║██      ██║        ██║
   ██║    █████╗  ██║      ███████║      ║██    ██║         ██║
   ██║    ██╔══╝  ██║      ██╔══██║       ║██  ██║  ╔██     ██║
   ██║    ███████╗███████╗██║  ██║        ║████║   ║████████║
   ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝        ╚════╝   ╚════════╝"""

    TAMIL_INFO = """
-_- """

    ENGLISH_INFO = """
-_- """

    TELUGU_INFO = """
     -_- """

    HINDI_INFO = """
     -_- """

    MALAYALAM_INFO = """
"""

    URTU_INFO = """
     -_- """

    GUJARATI_INFO = """
 -_- """

    KANNADA_INFO = """
 -_- ."""

    BANGLADESH_INFO = """
 -_- """

    RENAME_TXT = """
🌌 <b><u>CÓMO CONFIGURAR LA MINIATURA</u></b>
  
•> /set_thumb - envía cualquier imagen para configurar automáticamente la miniatura.
•> /del_thumb - usa este comando para eliminar tu miniatura anterior.
•> /view_thumb - usa este comando para ver tu miniatura actual.

📑 <b><u>CÓMO CONFIGURAR CAPTION PERSONALIZADA</u></b>

•> /set_caption - establecer caption personalizada
•> /see_caption - visualiza tu caption personalizada
•> /del_caption - eliminar caption personalizada

Ejemplo:- /set_caption 📕 Nombre del Archivo: {filename}
💾 Tamaño: {filesize}
⏰ Duración: {duration}

✏️ <b><u>CÓMO RENOMBRAR UN ARCHIVO</u></b>

•> /rename - envía cualquier archivo, haz clic en la opción de renombrar, escribe el nuevo nombre del archivo y
luego selecciona [ documento, video, audio ] 👈 elige esta opción.
"""


# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
