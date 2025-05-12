# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

class script(object):
    START_TXT = """<b><blockquote>Hola {} 👋,</blockquote>

Soy un bot de filtrado automático avanzado y poderoso.
Puedes usarme en tu grupo para encontrar archivos fácilmente.</b>"""

    HELP_TXT = """<b>Hola {} 👋,

Aquí tienes un resumen de las funciones y cómo puedo ayudarte:</b>"""

    ABOUT_TXT = """<b><blockquote>⍟───[ DETALLES DEL BOT ]───⍟</blockquote>

‣ Nombre: <a href="https://t.me/{}">{}</a>
‣ Desarrollador: <a href="{}">@WayK</a> (Adaptado y Mejorado)
‣ Librería: <a href='https://docs.pyrogram.org/'>Pyrogram</a>
‣ Lenguaje: <a href='https://www.python.org/'>Python 3</a>
‣ Base de Datos: <a href='https://www.mongodb.com/'>MongoDB</a>
‣ Alojamiento: (Ej: Heroku, VPS, etc. - Especificar si se desea)
‣ Estado: v3.0.0 [Beta]</b>"""

    SUBSCRIPTION_TXT = """<b>Invita a tus amigos usando tu enlace de referido para obtener acceso Premium gratis por {refer_premium_time}.

🔗 Tu Enlace de Referido: https://t.me/{}?start=REF-{}

Cuando {refer_count} usuarios únicos inicien el bot con tu enlace, ¡se te activará Premium automáticamente!

También puedes consultar nuestros planes pagos con /planes.</b>"""

    MANUELFILTER_TXT = """<b>Ayuda: Filtros Manuales</b>

Los filtros te permiten configurar respuestas automáticas para palabras clave específicas. Cuando alguien mencione esa palabra clave, responderé automáticamente.

<b>Notas Importantes:</b>
1.  Debo tener permisos de administrador en el grupo.
2.  Solo los administradores del grupo pueden añadir o gestionar filtros.
3.  Los botones de alerta tienen un límite de 64 caracteres para su mensaje.

<b>Comandos y Uso:</b>
•   <code>/filter nombre_filtro respuesta</code> - Añade un nuevo filtro.
    <i>Ej: /filter hola ¡Hola! ¿Cómo estás?</i>
•   <code>/filters</code> - Muestra todos los filtros activos en el chat.
•   <code>/stop nombre_filtro</code> - Elimina un filtro específico.
    <i>Ej: /stop hola</i>
•   <code>/stopall</code> - Elimina TODOS los filtros del chat (solo el dueño del grupo o admins del bot)."""

    BUTTON_TXT = """<b>Ayuda: Formato de Botones para Filtros</b>

Puedes añadir botones a tus respuestas de filtros manuales. Soporto botones con enlaces URL y botones que muestran una alerta.

<b>Notas:</b>
1.  Es necesario incluir texto junto con los botones.
2.  Puedes usar botones con respuestas de solo texto o con archivos multimedia.
3.  Usa el formato Markdown correcto para definir los botones.

<b>Botones con Enlace URL:</b>
<code>[Texto del Botón](buttonurl:https://ejemplo.com)</code>
<i>Ej: [Visita Nuestra Web](buttonurl:https://miweb.com)</i>

<b>Botones con Mensaje de Alerta:</b>
<code>[Texto del Botón](buttonalert:Este es el mensaje de alerta)</code>
<i>Ej: [Mostrar Info](buttonalert:Versión 1.2 del Bot)</i>

<b>Para añadir múltiples botones en la misma línea:</b>
<code>[Botón 1](buttonurl:enlace1.com) [Botón 2](buttonalert:alerta2:same)</code>
(Usa <code>:same</code> después de la URL/alerta del segundo botón en adelante en la misma fila)"""

    AUTOFILTER_TXT = """<b>Ayuda: Filtro Automático e Indexación</b>

<b>Indexar Archivos (para que el bot los encuentre):</b>
1.  Si tu canal de archivos es privado, hazme administrador allí.
2.  Asegúrate de que el canal no contenga contenido inapropiado.
3.  Para indexar, usa el comando <code>/index</code> en un grupo donde yo sea admin y esté conectado a tu canal de archivos. (Esta función puede variar según la configuración del bot).

<b>Funcionamiento del Filtro Automático (en grupos):</b>
1.  Añádeme como administrador a tu grupo.
2.  Si usas la función de "conexiones", conecta tu grupo a mi chat privado con <code>/connect</code> en el grupo.
3.  Activa el "Auto-Filtro" en el menú de <code>/settings</code> (accesible desde el grupo si eres admin). Cuando los usuarios escriban nombres de películas o series, buscaré automáticamente en mi base de datos."""

    CONNECTION_TXT = """<b>Ayuda: Conexiones PM-Grupo</b>

Esta función te permite vincular un grupo a tu chat privado conmigo. Así puedes gestionar filtros y configuraciones del grupo desde mi chat privado, evitando llenar el grupo de comandos.

<b>Notas:</b>
1.  Solo los administradores del grupo pueden crear o gestionar conexiones.
2.  Para crear una conexión, ve al grupo y usa el comando <code>/connect</code>. Te enviaré un mensaje de confirmación.

<b>Comandos y Uso (generalmente en mi chat privado después de conectar):</b>
•   <code>/connections</code> - Muestra todos los grupos que has conectado.
•   <code>/disconnect</code> - Desactiva la conexión activa actual.
•   <i>(Desde el menú de <code>/connections</code>, puedes activar/desactivar o eliminar conexiones individuales).</i>"""

    ADMIN_TXT = """<b>Ayuda: Comandos de Administración del Bot</b>

Estos comandos son solo para los administradores globales del bot.

•   <code>/stats</code> - Muestra estadísticas del bot (archivos, usuarios, chats).
•   <code>/broadcast</code> - Envía un mensaje a todos los usuarios del bot.
•   <code>/gbroadcast</code> - Envía un mensaje a todos los grupos donde está el bot.
•   <code>/users</code> - Lista los usuarios de la base de datos.
•   <code>/chats</code> - Lista los chats donde está el bot.
•   <code>/logs</code> - Muestra los logs recientes del bot.
•   <code>/leave chat_id</code> - Hace que el bot abandone un chat específico.
•   <code>/disable chat_id</code> - Deshabilita el bot en un chat específico.
•   <code>/ban_user user_id</code> - Banea a un usuario del uso del bot.
•   <code>/unban_user user_id</code> - Desbanea a un usuario.
    
<b>Gestión de Filtros Globales:</b>
•   <code>/gfilter</code> - Añade un filtro global.
•   <code>/gfilters</code> - Lista todos los filtros globales.
•   <code>/stopg nombre_filtro_global</code> - Elimina un filtro global específico.
•   <code>/stopallg</code> - Elimina todos los filtros globales.

<b>Gestión de Archivos (Base de Datos):</b>
•   <code>/delete file_id_o_unique_id</code> - Elimina un archivo específico de la base de datos.
•   <code>/deletefiles query_keyword</code> - Elimina archivos que coincidan con una palabra clave (ej. 'CAMRip').
"""
    # Mantenido SEC_STATUS_TXT con su nombre original
    SEC_STATUS_TXT = """<b>★ Usuarios Totales: <code>{}</code>
★ Chats Totales: <code>{}</code>
★ Archivos Totales: <code>{}</code>
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Libre: <code>{} MB</code></b>""" # Traducción ligera y "Gratis" a "Libre"

    STATUS_TXT = """<b>Archivos Totales en Todas las Bases de Datos: <code>{}</code>

BASE DE USUARIOS :-
★ Usuarios Totales: <code>{}</code>
★ Chats Totales: <code>{}</code>

PRIMERA BASE DE ARCHIVOS :-
★ Archivos Totales: <code>{}</code>
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Libre: <code>{} MB</code>

SEGUNDA BASE DE ARCHIVOS :-
★ Archivos Totales: <code>{}</code>
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Libre: <code>{} MB</code>

OTRA BASE DE DATOS :-
★ Almacenamiento Usado: <code>{} MB</code>
★ Almacenamiento Libre: <code>{} MB</code></b>""" # Traducción ligera

    LOG_TEXT_G = """#NuevoGrupo
Nombre: {} (<code>{}</code>)
Total de Miembros: <code>{}</code>
Añadido por: {}"""

    LOG_TEXT_P = """#NuevoUsuario
ID: <code>{}</code>
Nombre: {}"""

    ALRT_TXT = """<b>Hola {}</b> 👋,  

Estos botones son para el usuario que hizo la solicitud original. Por favor, realiza tu propia búsqueda. 😊"""

    OLD_ALRT_TXT = """<b>¡Oye {}</b>! 👋,  

Parece que estás interactuando con un mensaje de búsqueda antiguo cuyos datos han expirado. Por favor, realiza la búsqueda de nuevo. 😊"""

    CUDNT_FND = """<b>🤔 No pude encontrar nada relacionado con "<code>{}</code>".</b>

¿Quizás quisiste decir alguna de estas opciones?"""

    I_CUDNT = """<b>😔 Lo siento, no se encontraron archivos para tu solicitud: <code>{}</code></b>

Por favor, revisa la ortografía o prueba con diferentes términos.

<b>📽️ Formato para solicitar películas:</b>
<blockquote><code>Uncharted</code>, <code>Uncharted 2022</code>, <code>Uncharted En</code></blockquote>

<b>📺 Formato para solicitar series:</b>
<blockquote><code>Loki S01</code>, <code>Loki S01E04</code>, <code>Lucifer S03E24</code></blockquote>

<b>🚫 Por favor, evita usar caracteres especiales como:</b>
<blockquote><code>:(!,./</code></blockquote>"""

    MVE_NT_FND = """⚠️ <b>Película o serie no encontrada en la base de datos.</b>"""

    TOP_ALRT_MSG = """🔎 <b>Buscando tu solicitud en la base de datos... ¡Un momento!</b>"""

    MELCOW_ENG = """<b>¡Hola {}! 😍 Bienvenido/a al grupo {}. ¡Esperamos que disfrutes tu estadía! ❤️</b>"""

    SHORTLINK_INFO = """ℹ️ <b>Información sobre Acortadores</b>

Cuando esta función está activada por el administrador y no eres usuario Premium, algunos enlaces de descarga pueden pasar primero por un acortador de URL. Esto ayuda a mantener el bot.

Los usuarios Premium siempre reciben enlaces directos. ✨"""

    REQINFO = """
⚠️ <b>INFORMACIÓN IMPORTANTE</b> ⚠️

Este mensaje de resultados se eliminará automáticamente después de 5 minutos.

Si no ves el archivo que buscas en esta página, y hay más resultados, usa los botones de paginación (⬅️ Siguiente / Anterior ➡️) para ver más.
"""

    SELECT = """Por favor, selecciona tu idioma, calidad, temporada o episodio deseado si la búsqueda ofrece múltiples opciones."""

    SINFO = """
🤔 Para obtener este archivo, primero debes unirte al canal de actualización (si se requiere) y luego reintentar.
Si el problema persiste, contacta al administrador."""

    NORSLTS = """ 
★ #SIN_RESULTADOS ★

ID Usuario: <code>{}</code>
Nombre Usuario: {}
Búsqueda: "<code>{}</code>"
"""

    CAPTION = """<b>📂 Archivo:</b> <code>{file_name}</code>
<b>⚖️ Tamaño:</b> <code>{file_size}</code>

<i><a href="https://t.me/NessCloud">「Nᴇss Cʟᴏᴜᴅ」</a></i>"""

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

⏱️ <i>Respuesta en {search_time} segundos.</i>
👤 Solicitado por: {requester}
"""

    ALL_FILTERS = """<b>Hola {} 👋,

Puedes configurar filtros manuales para respuestas automáticas.
Usa los botones de abajo para aprender cómo darles formato.</b>"""

    GFILTER_TXT = """<b>Filtros Globales</b>

Los filtros globales son definidos por los administradores del bot y funcionan en todos los grupos donde el bot está presente.

<b>Comandos (Solo Admins del Bot):</b>
•   <code>/gfilter nombre respuesta</code> - Añade un filtro global.
•   <code>/gfilters</code> - Lista todos los filtros globales.
•   <code>/stopg nombre</code> - Elimina un filtro global.
•   <code>/stopallg</code> - Elimina todos los filtros globales."""

    STICKER_TXT = """<b>Obtener ID de un Sticker</b>

Para obtener el ID único de un sticker, simplemente responde al sticker con el comando:
<code>/stickerid</code>
O envía el sticker y luego usa <code>/stickerid</code> respondiendo a tu propio mensaje con el sticker."""

    # Mantenido FONT_TXT
    FONT_TXT = """<b>Uso:</b>
Puedes usar este módulo para cambiar el estilo de la fuente.
  
<b>Comando:</b> <code>/font tu texto</code> (el texto es opcional, si no se provee, se usará el texto al que respondes)
<b>Ejemplo:</b> <code>/font Hola Mundo</code>
""" # Traducido y clarificado

    PROGRESS_BAR = """\n
╭━━━━❰ Procesando... ❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """

    # Mantenido RESTART_TXT
    RESTART_TXT = """
<b>✅ ¡Bot Reiniciado Exitosamente! ✅</b>

📅 Fecha: <code>{}</code>
⏰ Hora: <code>{}</code>
🌐 Zona Horaria: <code>Asia/Kolkata</code> (Ajusta si es diferente)
🛠️ Estado de Compilación: <code>v3.0.0 [Beta]</code> (Actualiza versión)
""" # Traducido y con placeholders para personalización
