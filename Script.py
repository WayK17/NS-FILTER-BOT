# Créditos al desarrollador original
# Canal de YouTube: Tech_VJ 
# Soporte en Telegram: KingVJ01

class script(object):
    START_TXT = """<b><blockquote>¡Hola {} 👋!</blockquote>
    
Soy un bot avanzado de filtrado automático. Puedes usarme en tu grupo</b>"""

    HELP_TXT = """<b>Hola {}
Aquí están todas mis funciones útiles:</b>"""

    ABOUT_TXT = """<b><blockquote>⍟───[ MIS DETALLES ]───⍟</blockquote>
    
‣ Nombre : <a href=https://t.me/{}>{}</a>
‣ Creador : <a href={}>@WayK</a> 
‣ Biblioteca : <a href='https://docs.pyrogram.org/'>Pyrogram</a> 
‣ Lenguaje : <a href='https://www.python.org/download/releases/3.0/'>Python 3</a> 
‣ Base de datos : <a href='https://www.mongodb.com/'>Mongo DB</a> 
‣ Servidor : <a href='https://heroku.com'>Heroku</a> 
‣ Versión : v2.7.1 [Estable]</b>"""

    MANUELFILTER_TXT = """<b>Ayuda: Filtros
- Crea respuestas automáticas para palabras clave

Notas:
1. Necesito ser admin
2. Solo admines pueden agregar filtros
3. Los botones tienen límite de 64 caracteres

Comandos:
• /filter - Agregar filtro
• /filters - Listar filtros
• /del - Eliminar filtro
• /delall - Borrar todos los filtros (solo dueño)</b>"""

    BUTTON_TXT = """<b>Ayuda: Botones
Soporta botones de URL y alertas

Ejemplos:
[Texto](buttonurl:https://t.me/vjupdates2/3) - Botón de URL
[Texto](buttonalert:Mensaje de alerta) - Botón de alerta</b>"""

    AUTOFILTER_TXT = """<b>Ayuda: Auto-Filtro
1. Agrégame como admin en tu canal
2. Envíame el último mensaje del canal
3. Activa Auto-Filtro en /settings</b>"""

    CONNECTION_TXT = """<b>Ayuda: Conexiones
Conecta el bot a tu PM para gestionar filtros

Comandos:
• /connect - Conectar chat
• /disconnect - Desconectar
• /connections - Listar conexiones</b>"""

    EXTRAMOD_TXT = """<b>Módulos Extra:
    
⪼ /id - Obtener ID de usuario
⪼ /info - Ver información de usuario
⪼ /song - Descargar música
⪼ /telegraph - Subir medios (hasta 5MB)
⪼ /tts - Convertir texto a voz
⪼ /video - Descargar de YouTube
⪼ /font - Generar texto estilizado</b>"""

    ADMIN_TXT = """<b>Comandos de Admin:
• /logs - Ver registros
• /stats - Estadísticas
• /delete - Eliminar archivo
• /users - Listar usuarios
• /chats - Listar chats
• /leave - Abandonar chat
• /disable - Desactivar chat
• /ban - Banear usuario
• /unban - Desbanear
• /broadcast - Transmisión masiva</b>"""

    SEC_STATUS_TXT = """<b>📊 Estadísticas:
    
🗃️ Archivos totales: {}
👤 Usuarios: {}
👥 Chats: {}
💾 Espacio usado: {}
🆓 Espacio libre: {}</b>"""

    LOG_TEXT_G = """#NuevoGrupo
Grupo: {}({})
Miembros: {}
Agregado por: {}"""

    LOG_TEXT_P = """#NuevoUsuario
ID: {}
Nombre: {}"""

    CAPTION = """<b>📂 Nombre: {file_name}

⚙️ Tamaño: {file_size}</b>"""

    IMDB_TEMPLATE_TXT = """<b>Consulta: {query}

🎬 Título: <a href={url}>{title}</a>
🎭 Géneros: {genres}
📅 Año: {year}
⭐ Rating: {rating}/10
⏳ Duración: {runtime} mins
📆 Estreno: {release_date}
🌐 Idiomas: {languages}

⌛ Resultado en: {remaining_seconds} segundos
👤 Solicitado por: {message.from_user.mention}</b>"""

    RENAME_TXT = """<b>🖼️ Configurar Miniatura:
• /set_thumb - Establecer thumbnail
• /del_thumb - Eliminar thumbnail
• /view_thumb - Ver thumbnail actual

📝 Configurar Subtítulo:
• /set_caption - Establecer texto personalizado
• /see_caption - Ver subtítulo
• /del_caption - Eliminar subtítulo

🔄 Renombrar Archivos:
• /rename - Renombrar archivos (seleccionar tipo)</b>"""

    STREAM_TXT = """<b>🔗 Obtener enlace de transmisión:
    
Usa /stream para obtener enlace descargable de cualquier archivo</b>"""

    PROGRESS_BAR = """\n
╭━━━━❰ Renombrando... ❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """

    LOGO = """
 ____  _   _  ____    _____  _  _       _____  ______  ____     ____    ___   _____
|  _ \| | | |/ ___|  |  ___|| || |     |_   _||  ____||  _ \   | __ )  / _ \ |_   _|
| |_) | | | |\___ \  | |_   | || |_      | |  | |__   | |_) |  |  _ \ | | | |  | |  
|  _ <| |_| | ___) | |  _|  |__   _|     | |  |  __|  |  _ <   | |_) || |_| |  | |  
|_| \_\\___/ |____/  |_|       |_|       |_|  |_|     |_| \_\  |____/  \___/   |_|  
    """
    
    RESTART_TXT = """<b>𝖡𝗈𝗍 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝖾𝖽 !

📅 𝖣𝖺𝗍𝖾 : {}
⏰ 𝖳𝗂𝗆𝖾 : {}</b>"""