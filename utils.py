# No eliminar créditos @VJ_Botz
# Suscríbete al canal de YouTube para Bots Increíbles @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging, asyncio, os, re, random, pytz, aiohttp, requests, string, json, http.client
# Importa todas las variables de configuración global (mantener por si hay otras dependencias no obvias)
from info import *
from imdb import Cinemagoer
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import enums
from pyrogram.errors import *
from typing import Union, List # Importar List
from Script import script # Asumo que este archivo está traducido y actualizado.
from datetime import datetime, date
from database.users_chats_db import db # Base de datos de usuarios y chats (para usuarios, chats, settings, bans)
# Importar la base de datos de conexiones si se usa aquí (parece que no, se usa en commands.py y pm_filter.py)
# from database.connections_mdb import mydb # Si se usa mydb en utils para algo, importarlo
# from database.ia_filterdb import col, sec_col # Si se usan las colecciones de ia_filterdb directamente en utils, importarlas
from bs4 import BeautifulSoup # Se mantiene para search_gagala
from shortzy import Shortzy # Se mantiene para get_shortlink

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Eliminada importación de MongoClient ya que no se usa aquí
# Eliminada importación DuplicateKeyError ya que no se usa aquí
# Eliminada importación re duplicada

# Eliminado: TOKENS, VERIFIED (Relacionado con Verificación por usuario)
BANNED = {} # Se mantiene para funciones de baneo
# Eliminado: SECOND_SHORTENER (Relacionado con verificación shortener)
SMART_OPEN = '“' # Se mantiene para parser de filtros
SMART_CLOSE = '”' # Se mantiene para parser de filtros
START_CHAR = ('\'', '"', SMART_OPEN) # Se mantiene para parser de filtros

# Variables temporales (se mantienen las necesarias para funcionalidades activas)
class temp(object):
    BANNED_USERS = [] # Para baneo temporal en memoria
    BANNED_CHATS = [] # Para baneo temporal en memoria
    ME = None # Info del bot
    BOT = None # Objeto bot client (Pyrogram)
    CURRENT = int(os.environ.get("SKIP", 2)) # Para indexación? (mantener por ahora)
    CANCEL = False # Para cancelar indexación? (mantener por ahora)
    MELCOW = {} # Para mensajes de bienvenida? (mantener por ahora)
    U_NAME = None # Username del bot (se actualiza en bot.py o start handler)
    B_NAME = None # Nombre del bot (se actualiza en bot.py o start handler)
    GETALL = {} # Cache para "Enviar Todos" de resultados de búsqueda (pm_filter.py lo usa)
    SHORT = {} # Cache temporal (usado para shortlinks/archivos en PV, pm_filter.py lo usa)
    SETTINGS = {} # Cache de settings de grupo
    IMDB_CAP = {} # Cache de captions IMDB (pm_filter.py lo usa)
    # Eliminado cualquier otra variable si era específicamente para Referidos/Premium/Verificación

# --- Funciones de Soporte ---

# Modificado: Renombrada humanbytes a get_size
def get_size(size):
    """Get size in readable format"""
    # Código original de humanbytes
    if size == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return "%s %s" % (s, size_name[i])


# Modificado: pub_is_subscribed (simplificada)
async def pub_is_subscribed(bot, query, channel_ids: List[int]):
    """Verifica si un usuario está suscrito a una lista de canales públicos/privados."""
    btn = []
    # Itera sobre la lista de IDs de canales proporcionada
    for channel_id in channel_ids:
        try:
            chat = await bot.get_chat(int(channel_id))
            # Intenta obtener al miembro del chat
            await bot.get_chat_member(int(channel_id), query.from_user.id)
            # Si no hay excepción, el usuario está suscrito, no hacer nada.
        except UserNotParticipant:
            # Si el usuario no participa, añadir botón para unirse
            # Asegúrate de que el bot pueda obtener invite_link (ser admin para canales privados)
            invite_link = chat.invite_link
            if not invite_link: # Si el bot no es admin para obtener link, intentar crear uno (puede fallar)
                 try:
                      # Usar create_chat_invite_link si es posible
                      invite_link_obj = await bot.create_chat_invite_link(int(channel_id), creates_join_request=False) # No relacionado con REQUEST_TO_JOIN_MODE global
                      invite_link = invite_link_obj.invite_link
                 except Exception as e:
                      logger.error(f"Error al crear link de invitación para {channel_id}: {e}")
                      # Si falla crear link, intentar con el username si existe
                      if chat.username:
                           invite_link = f"https://t.me/{chat.username}"
                      else:
                           # Si no hay username ni se puede crear link, saltar este canal
                           continue # Saltar este canal si no se puede obtener/crear link
            btn.append(
                [InlineKeyboardButton(f'Unirse a {chat.title}', url=invite_link)]
            )
        except Exception as e:
            logger.error(f"Error al verificar suscripción en canal {channel_id}: {e}")
            # Si ocurre otro error (ej: PeerIdInvalid si el ID es inválido), ignora este canal.
            pass
    # Devuelve la lista de botones. Si está vacía, el usuario está suscrito a todos.
    return btn


# Modificado: is_subscribed (simplificada, solo verifica AUTH_CHANNEL)
async def is_subscribed(bot, query):
    """Verifica si un usuario está suscrito al canal de autorización global (AUTH_CHANNEL)."""
    # Esta función ahora solo verifica la suscripción al canal global AUTH_CHANNEL
    # si está configurado. La lógica de fsub por grupo usa pub_is_subscribed.
    if AUTH_CHANNEL: # Si AUTH_CHANNEL está configurado (variable de info.py)
        try:
            user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
            # Verificar que el status no sea BANNED ni RESTRICTED
            if user.status not in [enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.RESTRICTED]:
                return True # Está suscrito y no restringido/baneado
            else:
                return False # Está baneado o restringido
        except UserNotParticipant:
            return False # No está suscrito
        except Exception as e:
            logger.exception(e)
            # Si hay un error al verificar (ej: bot no admin en canal, ID inválido), registra el error
            # y asume que no está suscrito o hay un problema, por seguridad.
            return False
    else:
        # Si AUTH_CHANNEL no está configurado, la suscripción global no es obligatoria
        return True


# Se mantiene get_poster, search_gagala

# Eliminado: get_clone_shortlink (Relacionado con la función de clonar bot)

# Modificado: get_shortlink para usar solo configuración global
async def get_shortlink(chat_id, link):
    """Genera un shortlink usando la configuración global."""
    # Ignora chat_id, siempre usa las variables globales SHORTLINK_API y SHORTLINK_URL de info.py
    API = SHORTLINK_API
    URL = SHORTLINK_URL

    if not API or not URL:
        logger.warning("SHORTLINK_API o SHORTLINK_URL no configurados. No se puede generar shortlink.")
        return link # Devuelve el link original si no está configurado

    if URL == "api.shareus.io":
        url = f'https://{URL}/easy_api'
        params = {
            "key": API,
            "link": link,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.text()
                    if response.status == 200: # Verificar que la respuesta sea exitosa
                        return data # Retorna el shortlink en texto
                    else:
                         logger.error(f"Error HTTP {response.status} al generar shortlink shareus.io: {data}")
                         return link # Devuelve el link original si falla
        except Exception as e:
            logger.error(f"Excepción al generar shortlink con shareus.io: {e}")
            return link # Devuelve el link original si falla
    else:
        # Usa Shortzy para otros servicios
        try:
            shortzy = Shortzy(api_key=API, base_site=URL)
            shortened_link = await shortzy.convert(link)
            return shortened_link # Retorna el shortlink
        except Exception as e:
            logger.error(f"Error al generar shortlink con Shortzy ({URL}): {e}")
            return link # Devuelve el link original si falla


# Eliminado: get_tutorial (Función de tutorial por grupo eliminada)

# Eliminado: get_verify_shorted_link, check_token, get_token, verify_user, check_verification (Relacionado con Verificación por usuario)

# Eliminado: get_seconds (Relacionado con Premium/Referidos)


# Modificado: send_all para usar Shortlink Global o enviar directo, sin checks de Premium/Verificación/Shortlink per-grupo, AÑADIDA AUTO-ELIMINACIÓN
async def send_all(bot, userid, files, ident, chat_id_origin, user_name, query):
    """Envía una lista de archivos a un usuario en PV, aplicando shortlink global si está activado o enviando directo. Incluye auto-eliminación."""
    # Obtener settings del chat de origen para verificar la opción de auto-eliminación
    settings = await get_settings(chat_id_origin) # Esta función ya devuelve defaults si el chat no existe

    # Asegurarse de que auto_delete_enabled sea False por defecto si el chat_id_origin es 0 o None (ej. si el usuario viene de un start link sin grupo)
    auto_delete_enabled = settings.get('auto_delete', False) if chat_id_origin else False
    messages_to_delete = [] # Lista para guardar los mensajes enviados al PV

    try:
        if SHORTLINK_MODE: # Si el Shortlink Global está activado
            # Enviar un mensaje CON Shortlink para cada archivo en la lista
            for file in files:
                title = file.get("file_name")
                size = get_size(file.get("file_size", 0)) # <-- Llama a get_size
                file_id_to_send = file.get("file_id")

                if not file_id_to_send: continue # Saltar si no hay file_id

                # Crear el link de inicio que lleva al usuario de vuelta al bot con el ID del archivo
                # Usar prefijo 'files_' para listas (siempre)
                start_link = f"https://telegram.me/{temp.U_NAME}?start=files_{file_id_to_send}"

                # Generar shortlink global
                shortlink_url = await get_shortlink(None, start_link) # Usar None para chat_id para config global

                # Texto del mensaje con información básica del archivo (traducido)
                message_text = f"<b>Hola {user_name} 👋\n\n✅ Tu enlace seguro para el archivo ha sido generado. Por favor, haz clic en el botón de descarga.\n\n🗃️ Nombre del Archivo: {title}\n🔖 Tamaño: {size}</b>"

                # Botón para el shortlink
                button = [[InlineKeyboardButton("📥 Descargar 📤", url=shortlink_url if shortlink_url else start_link)]] # Usar shortlink si se generó, si no, el link directo

                # Enviar el mensaje al usuario en PV
                msg = await bot.send_message(
                    chat_id=userid, # ID del usuario en PV
                    text=message_text,
                    reply_markup=InlineKeyboardMarkup(button),
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True # Deshabilitar preview para links shorteados
                )
                messages_to_delete.append(msg) # Añadir mensaje a la lista para auto-eliminación
                await asyncio.sleep(0.5) # Pequeña pausa

        else: # Si el Shortlink Global está desactivado
            # Enviar cada archivo directamente al usuario en PV
            for file in files:
                file_id_to_send = file.get("file_id")
                if not file_id_to_send: continue # Saltar si no hay file_id

                f_caption = file.get("caption")
                title = file.get("file_name")
                size = get_size(file.get("file_size", 0)) # <-- Llama a get_size

                # Construir caption usando la plantilla global CUSTOM_FILE_CAPTION si existe
                caption_text = f"{title}" # Caption por defecto
                if CUSTOM_FILE_CAPTION: # Asumo que CUSTOM_FILE_CAPTION está configurado globalmente
                    try:
                        caption_text = CUSTOM_FILE_CAPTION.format(
                            file_name='' if title is None else title,
                            file_size='' if size is None else size,
                            file_caption='' if f_caption is None else f_caption
                        )
                    except Exception as e:
                        logger.exception(e)
                        # Usar un caption de fallback si la plantilla falla
                        caption_text = f"Archivo: {title}\nTamaño: {size}\n" + (f"Descripción: {f_caption}" if f_caption else "")

                # Botones estándar para envío directo (traducidos)
                button = [[
                    InlineKeyboardButton('Grupo de Soporte', url=SUPPORT_CHAT), # Usar variable global
                    InlineKeyboardButton('Canal de Actualizaciones', url=CHNL_LNK) # Usar variable global
                ],[
                     InlineKeyboardButton("Dueño del Bot", url=OWNER_LNK) # Usar variable global
                ]]

                # Enviar el archivo cacheado al usuario en PV
                msg = await bot.send_cached_media(
                    chat_id=userid, # ID del usuario en PV
                    file_id=file_id_to_send,
                    caption=caption_text,
                    protect_content=PROTECT_CONTENT, # Usar variable global PROTECT_CONTENT
                    reply_markup=InlineKeyboardMarkup(button)
                )
                messages_to_delete.append(msg) # Añadir mensaje a la lista para auto-eliminación
                await asyncio.sleep(0.5) # Pequeña pausa

    except UserIsBlocked:
        await query.answer('¡Desbloquea el bot!', show_alert=True) # Traducido
        return # Salir si el usuario bloqueó el bot
    except PeerIdInvalid:
        await query.answer('¡Hola! Inicia el bot primero y haz clic en Enviar Todos.', show_alert=True) # Traducido
        return # Salir si el ID del usuario es inválido
    except Exception as e:
        logger.exception(e)
        await query.answer('Ocurrió un error al enviar los archivos. Asegúrate de haber iniciado el bot.', show_alert=True) # Traducido
        return # Salir si hay otro error


    # --- Lógica de Auto-Eliminación (aplicada si auto_delete está activado) ---
    if auto_delete_enabled and messages_to_delete:
        # Enviar mensaje de advertencia de auto-eliminación
        # Asegurarse de que el userid es válido antes de enviar
        if userid and userid != 0:
             warning_msg = await bot.send_message(
                 chat_id=userid,
                 text=f"<blockquote><b><u>❗️❗️❗️IMPORTANTE❗️️❗️❗️</u></b>\n\nEstos {len(messages_to_delete)} mensajes serán eliminados en <b><u>10 minutos</u> 🫥 <i></b>(Debido a problemas de derechos de autor)</i>.\n\n<b><i>Por favor, reenvía estos mensajes a tus mensajes guardados o a cualquier chat privado si deseas conservarlos.</i></b></blockquote>",
                 parse_mode=enums.ParseMode.HTML
             )
             await asyncio.sleep(600) # Esperar 10 minutos

             # Auto-eliminar los mensajes enviados y el mensaje de advertencia
             for msg in messages_to_delete:
                 try: await msg.delete()
                 except: pass # Ignorar errores si el mensaje ya fue borrado
             try: await warning_msg.delete() # Eliminar el mensaje de advertencia
             except: pass # Ignorar si ya fue borrado
    # --- Fin Lógica de Auto-Eliminación ---


# Modificado: get_cap para traducir hardcoded strings y usar get_size renombrado, eliminar remaining_seconds
async def get_cap(settings, files, query, total_results, search):
    """Construye el caption para el mensaje de resultados de búsqueda."""
    # Eliminado 'remaining_seconds' de los argumentos, ya no se usa
    cap = "" # Caption a construir

    # Obtener info de IMDB si está activado y hay archivos (solo necesitamos el primero para el poster)
    imdb_info = await get_poster(search, file=(files[0])["file_name"]) if settings.get("imdb", False) and files else None

    if imdb_info:
        # Usar la plantilla de script.py (asumo que está traducida y limpia)
        TEMPLATE = script.IMDB_TEMPLATE_TXT
        try:
            # get_poster devuelve un diccionario que coincide con los placeholders de la plantilla
            cap = TEMPLATE.format(
                qurey=search, # Búsqueda original
                title=imdb_info.get('title', 'N/A'),
                votes=imdb_info.get('votes', 'N/A'),
                # Años, aka, etc. ya vienen formateados o se formatean en get_poster
                aka=imdb_info.get("aka", "N/A"),
                seasons=imdb_info.get("seasons", "N/A"),
                box_office=imdb_info.get('box_office', 'N/A'),
                localized_title=imdb_info.get('localized_title', 'N/A'),
                kind=imdb_info.get("kind", "N/A"),
                imdb_id=imdb_info.get("imdb_id", "N/A"), # get_poster ya formatea a ttID
                cast=imdb_info.get("cast", "N/A"),
                runtime=imdb_info.get("runtime", "N/A"),
                countries=imdb_info.get("countries", "N/A"),
                certificates=imdb_info.get("certificates", "N/A"),
                languages=imdb_info.get("languages", "N/A"),
                director=imdb_info.get("director", "N/A"),
                writer=imdb_info.get("writer", "N/A"),
                producer=imdb_info.get("producer", "N/A"),
                composer=imdb_info.get("composer", "N/A") ,
                cinematographer=imdb_info.get("cinematographer", "N/A"),
                music_team=imdb_info.get("music_team", "N/A"),
                distributors=imdb_info.get("distributors", "N/A"),
                release_date=imdb_info.get('release_date', 'N/A'),
                year=imdb_info.get('year', 'N/A'),
                genres=imdb_info.get('genres', 'N/A'),
                poster=imdb_info.get('poster', 'N/A'),
                plot=imdb_info.get('plot', 'N/A'),
                rating=imdb_info.get('rating', 'N/A'),
                url=imdb_info.get('url', 'N/A'), # get_poster ya formatea a URL
            )
            # Cachear el caption IMDB para la paginación
            temp.IMDB_CAP[query.from_user.id] = cap

        except Exception as e:
             logger.exception(e)
             # Fallback si la plantilla falla (traducido)
             cap = f"<b>🔍 Resultados IMDB (Error en plantilla) para:</b> {search}\n\n"
             if imdb_info and imdb_info.get('plot'): cap += f"<b>Sinopsis:</b> {imdb_info['plot']}\n"

        # Añadir lista de archivos al caption (traducido)
        # Solo si se usan botones (en modo texto la lista ya va en el caption principal)
        if settings.get("button", True):
             cap += "<b>\n\n<u>🍿 Archivos Encontrados 👇</u></b>\n\n" # Traducido
             for file in files:
                  # Usar formato de link de inicio para referenciar archivos
                  # get_size se usa aquí
                  cap += f"<b>📁 <a href='https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}'>[{get_size(file['file_size'])}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file['file_name'].split()))}</a>\n\n</b>"
        else:
            # Si no se usan botones, la lista de archivos se añade en auto_filter al caption simple.
            # No duplicar aquí si settings['button'] es False.
            pass


    else:
        # Si IMDB está desactivado, usar un caption simple (traducido)
        cap = f"<b>🔍 Resultados para:</b> {search}\n\n" # Traducido
        cap += f"<b>👤 Solicitado por:</b> {query.from_user.mention}\n\n" # Mantener mención
        cap += f"<b>⚙️ Proporcionado por:</b> {query.message.chat.title}\n\n" # Mantener título del chat
        # Mensaje de advertencia de auto-eliminación (traducido)
        cap += "⚠️ Este mensaje podría ser eliminado automáticamente después de un tiempo (por derechos de autor).\n\n" # Traducido
        # Añadir lista de archivos (traducido)
        # Solo si se usan botones (en modo texto la lista ya va en el caption principal)
        if settings.get("button", True):
             cap += "<b><u>🍿 Archivos Encontrados 👇</u></b>\n\n" # Traducido
             for file in files:
                  # Usar formato de link de inicio para referenciar archivos
                  # get_size se usa aquí
                  cap += f"<b>📁 <a href='https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}'>[{get_size(file['file_size'])}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file['file_name'].split()))}</a>\n\n</b>"
        else:
            # Si no se usan botones, la lista de archivos se añade en auto_filter al caption simple.
            # No duplicar aquí si settings['button'] es False.
            pass


    return cap


# Se mantienen get_file_id, extract_user, list_to_str, last_online, split_quotes, gfilterparser, parser, remove_escapes

# Eliminada la función humanbytes duplicada
# def humanbytes(size): ... (Eliminada)


# --- Funciones relacionadas con la base de datos de settings (Mover a users_chats_db.py?) ---
# Nota: Originalmente, get_settings y save_group_settings interactuaban con db (users_chats_db)
# Es mejor que estas funciones estén en users_chats_db.py o que utils solo llame a métodos de db.
# Ya ajustamos users_chats_db.py para tener metodos get_settings y update_settings.
# Estas funciones get_settings y save_group_settings en utils.py actúan como wrappers o usan cache.
# Es aceptable mantenerlas aquí si usan cache o lógica adicional.
# get_settings aquí usa el cache temp.SETTINGS y luego llama a db.get_settings.
# save_group_settings llama a db.update_settings.
# Esto es válido. Las mantendremos aquí.

async def get_settings(group_id):
    """Obtiene la configuración de un grupo desde la base de datos o cache."""
    # Usar cache si está disponible
    if group_id in temp.SETTINGS:
        return temp.SETTINGS[group_id]

    # Obtener settings de DB. db.get_settings ya devuelve defaults si no existe.
    settings = await db.get_settings(group_id)

    # Almacenar en cache
    temp.SETTINGS[group_id] = settings

    return settings


async def save_group_settings(group_id, key, value):
    """Guarda una configuración específica para un grupo en DB y actualiza cache."""
    # Obtener settings actuales (usará cache si está disponible)
    current = await get_settings(group_id)

    # Asegúrate de que la clave que guardas es una de las esperadas
    valid_keys = ['button', 'file_secure', 'imdb', 'spell_check', 'welcome', 'auto_delete', 'auto_ffilter', 'max_btn', 'fsub', 'template']
    if key in valid_keys:
        current[key] = value # Actualiza el diccionario en memoria/cache
        await db.update_settings(group_id, current) # Guarda en DB
        # El cache ya está actualizado porque 'current' es el mismo diccionario.
    else:
         logger.warning(f"Intento de guardar configuración inválida: {key}={value} para grupo {group_id}")
         # Ignorar o registrar intento de guardar clave no válida

# --- Fin de Funciones relacionadas con settings ---


# --- Funciones relacionadas con Broadcast (Eliminadas) ---
# Estas funciones ya no existen en esta versión de utils.py.
# Si se quieren re-añadir, deberán ser reimplementadas.
# async def broadcast_messages(bot, message, users): ... (Eliminada)
# async def broadcast_messages_group(bot, message, groups): ... (Eliminada)
# --- Fin de Funciones relacionadas con Broadcast ---


# --- Fin de Funciones de Soporte ---
