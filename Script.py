# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

class script(object):
    START_TXT = """<b>👋 ¡Hola {}!</b>

<i>Soy un bot de filtrado automático avanzado que te ayudará a encontrar archivos rápidamente.</i>

<blockquote>Simplemente escribe el nombre de lo que buscas en el chat y te mostraré los resultados disponibles.</blockquote>"""


    
    HELP_TXT = """<b>Hola {}
Aquí están mis funciones principales:</b>"""

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

    # Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

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

    # Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

    EXTRAMOD_TXT = """ʜᴇʟᴘ: Exᴛʀᴀ Mᴏᴅᴜʟᴇs
<b>ɴᴏᴛᴇ:</b>
 <b>✯ Maintained by : <a href={}>Owner</a></b>
  
 <b>✯ Join here : <a href={}>Update Channel</a></b> 
  
 ./id - <code>ɢᴇᴛ ɪᴅ ᴏꜰ ᴀ ꜱᴘᴇᴄɪꜰɪᴇᴅ ᴜꜱᴇʀ.</ 
 code> 
  
 ./info  - <code>ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜꜱᴇʀ.</code> 
  
 ./song - Download any song [<code>example /song vaa vaathi song</code>] 
  
 ./telegraph - <code>Telegraph generator sen under 5MB video or photo I give telegraph link</code> 
  
 ./tts - <code>This command usage text to voice converter</code> 
  
 ./video - This command usage any YouTube video download hd [<code>example /video https://youtu.be/example...</code>]

./font - This command usage stylish and cool font generator [<code>example /font hi</code>]"""


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

    ALRT_TXT = """👋 Hola {},

Esta no es tu solicitud.
Realiza tu propia búsqueda."""

    OLD_ALRT_TXT = """Hey {},  

Estás usando uno de mis mensajes antiguos.  
Por favor, envía la solicitud de nuevo. 😊"""

    CUDNT_FND = """<b>❌ No pude encontrar nada relacionado con <code>{}</code>.</b>

¿Querías decir alguno de estos?"""

    I_CUDNT = """<b>😔 Lo siento, no se encontraron archivos para tu solicitud: <code>{}</code></b>

Por favor, revisa la ortografía o prueba con diferentes términos.

<b>📽️ Formato para solicitar películas:</b>
<blockquote><code>Uncharted</code>, <code>Uncharted 2022</code>, <code>Mufasa</code></blockquote>

<b>📺 Formato para solicitar series:</b>
<blockquote><code>Loki S01</code>, <code>Loki</code>, <code>Suits</code></blockquote>

<b>🚫 Por favor, evita usar caracteres especiales como:</b>
<blockquote><code>:(!,./</code></blockquote>"""

    I_CUD_NT = """<b>🔍 No pude encontrar ninguna película relacionada con <code>{}</code>.</b>

Por favor, revisa la ortografía en Google o IMDB y vuelve a intentarlo."""

    MVE_NT_FND = """⚠️ <b>Película/serie no encontrada en la base de datos.</b>"""

    TOP_ALRT_MSG = """🔎 <b>Buscando película/serie en la base de datos...</b>"""

    MELCOW_ENG = """<b>Hola {} 😍, y bienvenido al grupo {} ❤️</b>"""

    SHORTLINK_INFO = """

🫵 Select Your Language And Earn Money 💰"""

    REQINFO = """
⚠ INFORMACIÓN ⚠

Después de 5 Minutos Este Mensaje Se Eliminará Automáticamente.

Si no ves el archivo de película/serie solicitado, revisa la siguiente página"""

    SELECT = """SELECCIONA tu idioma preferido, calidad, temporada y episodio"""

    SINFO = """
🫣 Para la película, únete primero y luego haz clic en el botón "Inténtalo de nuevo" 😅"""

    NORSLTS = """ 
★ #SIN RESULTADOS ★

ID <b>: {}</b>

Nombre <b>: {}</b>

Mensaje <b>: {}</b>"""

    CAPTION = """<b>📂 Archivo:</b> <code>{file_name}</code>

<b>⚙️ Tamaño:</b> <code>{file_size}</code>

<a href="https://t.me/NessCloud">「Nᴇss Cʟᴏᴜᴅ」</a>""" 

    IMDB_TEMPLATE_TXT = """
✨ <b>¡Información Encontrada!</b> ✨

---

🎬 <b>{title}</b>
<a href="{url}">🔗 Ver detalles</a>

---

📊 <b>Datos Clave</b>

⭐ Calificación: <b>{rating}</b> / 10 (<a href="{url}/ratings">Votos</a>)
🎭 Géneros: <i>{genres}</i>
📅 Año: {year}
🌐 Idiomas: <code>{languages}</code>
⏳ Duración: {runtime} min.
🗓️ Lanzamiento: {release_date}
🌍 País: {countries}

---

🔎 <i>Búsqueda original: {qurey}</i>

⏱️ <i>Respuesta en {remaining_seconds} segundos.</i>
👤 Solicitado por: {message.from_user.mention}
 """
    
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



    PROGRESS_BAR = """\n
╭━━━━❰ Renombrando Archivo... ❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """
  

  
    STICKER_TXT = """<b>Puedes usar este módulo para encontrar cualquier ID de sticker.
  
Uso: para obtener el ID del sticker, simplemente escribe: /stickerid
</b>""" 
  
    FONT_TXT= """<b>Uso:
Puedes usar este módulo para cambiar el estilo de la fuente.
  
Comando: /font tu texto (opcional)
Ejemplo: /font hola
</b>""" 
  
    PURGE_TXT = """<b>Purgar

Elimina muchos mensajes de los grupos!
(Administrador)

◉ /purge: elimina todos los mensajes desde el mensaje al que respondes hasta el mensaje actual.</b>""" 
  

  
    PIN_TXT = """ """

 
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
 """

    ENGLISH_INFO = """
 """

    TELUGU_INFO = """
 """

    HINDI_INFO = """
 """

    MALAYALAM_INFO = """
 """

    URTU_INFO = """
"""

    GUJARATI_INFO = """
 """

    KANNADA_INFO = """
 """

    BANGLADESH_INFO = """
 """

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


    
