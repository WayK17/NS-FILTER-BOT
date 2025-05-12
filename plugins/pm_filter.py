# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, logging, string, asyncio, time, re, ast, random, math, pytz, pyrogram
from datetime import datetime, timedelta, date, time
# Necesitarás traducir las variables en Script.py
from Script import script
# Asegúrate de que estas variables globales estén en info.py o config.py
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, ChatPermissions, WebAppInfo
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
# Asegúrate de que estas funciones y la DB estén disponibles y actualizadas
from utils import get_size, is_subscribed, pub_is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink, get_tutorial, send_all, get_cap
from database.users_chats_db import db
from database.ia_filterdb import col, sec_col, db as vjdb, sec_db, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import del_all, find_filter, get_filters
from database.connections_mdb import mydb, active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from database.gfilters_mdb import find_gfilter, get_gfilters, del_allg
from urllib.parse import quote_plus
# Asegúrate de que estas funciones existen
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
lock = asyncio.Lock()

# --- Diccionarios para estado temporal ---
BUTTON = {} # Parece no usarse, considerar eliminar si es cierto
BUTTONS = {} # Parece no usarse, considerar eliminar si es cierto
FRESH = {} # Almacena la búsqueda actual por mensaje
BUTTONS0 = {} # Relacionado con spell check/send_fsall? - Revisar uso
BUTTONS1 = {} # Relacionado con spell check/send_fsall? - Revisar uso
BUTTONS2 = {} # Relacionado con spell check/send_fsall? - Revisar uso
SPELL_CHECK = {} # Almacena sugerencias de corrección ortográfica

MSG_ALRT = "Comando procesado ✅" # Mensaje genérico para query.answer

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    # Evitar procesar en el grupo de soporte si está definido
    if SUPPORT_CHAT_ID and message.chat.id == SUPPORT_CHAT_ID:
        # Respuesta específica para el grupo de soporte
        search = message.text
        temp_files, temp_offset, total_results = await get_search_results(chat_id=message.chat.id, query=search.lower(), offset=0, filter=True)
        if total_results == 0:
            return
        else:
            # Usar variables de info.py para enlaces
            grp_link = GRP_LNK or "tu grupo principal"
            return await message.reply_text(f"Hola {message.from_user.mention}, encontré {str(total_results)} resultados para '{search}'.\n\nEste es un grupo de soporte, no se entregan archivos aquí.\n\nBusca en {grp_link}")

    # --- Force Subscribe (Implementación con Mute en Grupo) ---
    settings = await get_settings(message.chat.id)
    chatid = message.chat.id
    user_id = message.from_user.id if message.from_user else 0

    # Verificar si Force Subscribe está habilitado para este grupo
    fsub_channel_id = settings.get('fsub')
    if fsub_channel_id:
        try:
            # pub_is_subscribed debería devolver los botones si no está suscrito, None si sí lo está
            btn = await pub_is_subscribed(client, message, fsub_channel_id)
            if btn:
                # Botón para desmutearse (llama al callback 'unmuteme')
                btn.append([InlineKeyboardButton("✅ Ya me uní, desmutearme", callback_data=f"unmuteme#{int(user_id)}")])
                # Restringir al usuario (mutear)
                await client.restrict_chat_member(chatid, user_id, ChatPermissions(can_send_messages=False))
                await message.reply_photo(
                    photo=random.choice(PICS), # Usar PICS de info.py
                    caption=f"👋 Hola {message.from_user.mention},\n\nPara poder hablar aquí, únete a nuestro canal y luego presiona el botón de abajo.",
                    reply_markup=InlineKeyboardMarkup(btn),
                    parse_mode=enums.ParseMode.HTML
                )
                return # Detener procesamiento si está muteado
        except Exception as e:
            print(f"Error en Force Subscribe para chat {chatid}, usuario {user_id}: {e}")
            # Considerar enviar un mensaje al admin si falla constantemente

    # --- Procesamiento de Filtros ---
    # 1. Filtros Manuales (por grupo)
    manual = await manual_filters(client, message)
    if manual: # Si un filtro manual coincidió, ya se envió respuesta
        return

    # 2. Filtros Globales (si los manuales no coincidieron)
    # Implementación de filtros globales (si existe la función global_filters y la DB gfilters_mdb)
    # Nota: La función global_filters no estaba definida en el código original, asumiendo que existe
    # if GFILTER_ENABLED: # Añadir una variable global para habilitar/deshabilitar filtros globales
    #     global_f = await global_filters(client, message)
    #     if global_f:
    #         return

    # 3. Filtro Automático (si no hubo coincidencias manuales/globales y está activado)
    try:
        if settings.get('auto_ffilter', AUTO_FILTER_ENABLED_BY_DEFAULT): # Usar valor de config si no está en settings
            ai_search = True # ¿Es necesaria esta variable?
            reply_msg = await message.reply_text(f"Buscando '<i>{message.text}</i>'...", parse_mode=enums.ParseMode.HTML)
            await auto_filter(client, message.text, message, reply_msg, ai_search)
    except Exception as e:
        print(f"Error en Auto Filter para chat {chatid}: {e}")
        # Podríamos intentar guardar el setting por defecto si falla por KeyError
        # grpid = await active_connection(str(message.from_user.id)) if message.from_user else message.chat.id
        # await save_group_settings(grpid, 'auto_ffilter', AUTO_FILTER_ENABLED_BY_DEFAULT)
        # reintentar auto_filter... (cuidado con bucles infinitos)


@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id

    # Ignorar comandos y hashtags
    if content.startswith("/") or content.startswith("#"):
        return

    # Verificar si la búsqueda en PM está habilitada globalmente
    if not PM_SEARCH:
         # await message.reply_text("La búsqueda por mensaje privado está desactivada.") # Opcional: informar al usuario
         return

    # Proceder con la búsqueda automática en PM
    ai_search = True # ¿Necesario?
    # Usar reply para mantener el contexto
    reply_msg = await message.reply_text(f"Buscando '<i>{content}</i>'...", parse_mode=enums.ParseMode.HTML)
    await auto_filter(bot, content, message, reply_msg, ai_search)

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset_str = query.data.split("_")
    req_user_id = int(req)
    try:
        offset = int(offset_str)
    except:
        offset = 0

    # Verificar que el usuario que hace clic es el que inició la búsqueda
    if req_user_id != query.from_user.id and req_user_id != 0: # 0 para búsquedas globales? revisar
        return await query.answer(f"❌ ¡Ups! Estos botones son para {query.from_user.first_name}.", show_alert=True)

    # Obtener la búsqueda original guardada
    search = FRESH.get(key)
    if not search:
        await query.answer("⚠️ Esta búsqueda ha expirado o es muy antigua. Por favor, realiza la búsqueda de nuevo.", show_alert=True)
        # Considerar borrar el mensaje si la búsqueda expiró
        # await query.message.delete()
        return

    # Obtener resultados de la base de datos
    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)

    if not files:
        return await query.answer("No hay más resultados en esta página.", show_alert=True)

    # Guardar temporalmente los archivos de esta página (¿para 'Enviar Todo'?)
    temp.GETALL[key] = files
    # Guardar chat_id para redirigir clics de archivo/enviar todo (revisar si es necesario globalmente)
    # temp.SHORT[query.from_user.id] = query.message.chat.id

    settings = await get_settings(query.message.chat.id)
    # Determinar prefijo para callbacks de archivo ('filep' o 'file')
    file_cb_prefix = 'filep' if settings.get('file_secure') else 'file'
    # Determinar si se muestran botones individuales o solo texto/enlaces
    show_buttons = settings.get('button', True) # Botones por defecto
    # Determinar máximo de botones por página
    max_buttons_per_page = 10 if settings.get('max_btn', True) else MAX_B_TN # Usa MAX_B_TN de config

    btn = []

    # Botón Premium "Enviar Todo"
    # Nota: La verificación real se hace en el callback 'sendfiles'
    btn.append([
        InlineKeyboardButton("✨ Enviar Todo (Premium)", callback_data=f"sendfiles#{key}")
    ])

    # Botones individuales para cada archivo (si show_buttons es True)
    if show_buttons:
        for file in files:
            # Limpiar nombre de archivo para mostrar en botón
            file_name_display = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.get('file_name', 'archivo').split()))
            btn.append([
                InlineKeyboardButton(
                    text=f"[{get_size(file['file_size'])}] {file_name_display}",
                    callback_data=f'{file_cb_prefix}#{file["file_id"]}'
                )
            ])

    # Botones de Paginación
    prev_offset = offset - max_buttons_per_page if offset >= max_buttons_per_page else 0
    has_prev = offset > 0
    has_next = n_offset != 0 # n_offset es el offset para la *siguiente* página

    pagination_row = []
    if has_prev:
        pagination_row.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"next_{req_user_id}_{key}_{prev_offset}"))
    else:
        # Añadir un placeholder o nada si no hay anterior
        pagination_row.append(InlineKeyboardButton(" ", callback_data="noop")) # No operativo

    # Mostrar página actual y total (aproximado)
    current_page = math.ceil(offset / max_buttons_per_page) + 1
    total_pages = math.ceil(total / max_buttons_per_page)
    if total_pages > 0:
       pagination_row.append(InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="noop")) # No operativo
    else:
       # No mostrar si solo hay una página o total es 0
       pass


    if has_next:
        pagination_row.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"next_{req_user_id}_{key}_{n_offset}"))
    else:
         # Añadir un placeholder o nada si no hay siguiente
        pagination_row.append(InlineKeyboardButton(" ", callback_data="noop")) # No operativo


    if pagination_row:
        btn.append(pagination_row)


    # --- Generar Caption ---
    # Usar plantilla si los botones individuales están desactivados
    if not show_buttons:
        # Construir el caption con enlaces directos (manejar shortlink aquí si es necesario)
        is_premium_user = await db.has_premium_access(query.from_user.id)
        use_shortlink = SHORTLINK_ENABLED and not is_premium_user

        cap = f"Resultados para: <b>{search}</b> (Página {current_page}/{total_pages})\n\n"
        for file in files:
            # Construir el enlace /start que será procesado por el bot
            start_link_payload = f"{file_cb_prefix}_{file['file_id']}"
            # Aplicar Shortlink si corresponde
            if use_shortlink and SHORTLINK_URL and SHORTLINK_API:
                 final_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f"https://t.me/{temp.U_NAME}?start={start_link_payload}")
            else:
                 final_link = f"https://t.me/{temp.U_NAME}?start={start_link_payload}"

            file_name_display = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.get('file_name', 'archivo').split()))
            cap += f"📁 <a href='{final_link}'>[{get_size(file['file_size'])}] {file_name_display}</a>\n"

        try:
            await query.message.edit_text(
                text=cap,
                reply_markup=InlineKeyboardMarkup(btn),
                disable_web_page_preview=True, # Importante para que no carguen los t.me
                parse_mode=enums.ParseMode.HTML
            )
        except MessageNotModified:
            pass
    else:
        # Si se usan botones, solo editar el markup (asume que el caption ya existe)
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass

    await query.answer()

@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_idx_str = query.data.split('#')
    req_user_id = int(user)

    # Verificar usuario
    if req_user_id != 0 and query.from_user.id != req_user_id:
        return await query.answer(f"❌ ¡Oye! Estos botones son para otro usuario.", show_alert=True)

    # Obtener sugerencias guardadas
    # Usar query.message.reply_to_message.id podría fallar si el mensaje original fue borrado
    # Es más seguro usar query.message.id si el mensaje con botones es el editado
    movies = SPELL_CHECK.get(query.message.id) # Usar ID del mensaje actual (el que tiene los botones)
    if not movies:
        return await query.answer("⚠️ Esta sugerencia ha expirado o no se encontró. Intenta buscar de nuevo.", show_alert=True)

    # Manejar botón de cierre
    if movie_idx_str == "close_spellcheck":
        await query.message.delete()
        # Limpiar del diccionario para liberar memoria
        try:
            del SPELL_CHECK[query.message.id]
        except KeyError:
            pass
        return await query.answer("Sugerencias cerradas.")

    try:
        movie_idx = int(movie_idx_str)
        if not (0 <= movie_idx < len(movies)):
            return await query.answer("Índice de película inválido.", show_alert=True)
        selected_movie = movies[movie_idx]
    except (ValueError, IndexError):
        return await query.answer("Error al seleccionar la sugerencia.", show_alert=True)

    # Limpiar nombre de película seleccionado
    cleaned_movie = re.sub(r"[:\-]", " ", selected_movie)
    cleaned_movie = re.sub(r"\s+", " ", cleaned_movie).strip()

    await query.answer(f"✅ Buscando '{cleaned_movie}'...")

    # Limpiar diccionario
    try:
        del SPELL_CHECK[query.message.id]
    except KeyError:
        pass

    # Iniciar búsqueda automática con el término corregido
    ai_search = True
    # Editar el mensaje de sugerencias para mostrar que se está buscando
    reply_msg = await query.message.edit_text(f"Buscando '<i>{cleaned_movie}</i>'...", parse_mode=enums.ParseMode.HTML)

    # Ejecutar auto_filter con el término corregido
    # Nota: auto_filter necesita `message` original para settings y user info
    # Si el mensaje original se borró, esto podría fallar.
    # Se podría pasar `query.message` y adaptar `auto_filter` o buscar el msg original si es posible.
    # Por ahora, asumimos que `query.message.reply_to_message` es el mensaje del usuario original
    if query.message.reply_to_message:
         await auto_filter(bot, cleaned_movie, query.message.reply_to_message, reply_msg, ai_search)
    else:
         # Si no hay reply_to_message, intentar usar el mensaje actual, puede faltar info del usuario original
         # await auto_filter(bot, cleaned_movie, query.message, reply_msg, ai_search)
         await reply_msg.edit_text("Error: No se pudo encontrar el mensaje original de la búsqueda.")


# Handler principal de Callbacks
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):

    # Ignorar callbacks ya procesados (next, spol)
    if query.data.startswith("next") or query.data.startswith("spol"):
        # Ya manejados por sus respectivas funciones
        # Podríamos añadir un query.answer() aquí por si acaso, pero debería ser redundante
        try:
            await query.answer()
        except Exception:
            pass # Ignorar si ya se respondió
        return

    # Callback para no hacer nada (placeholders en botones)
    if query.data == "noop":
        return await query.answer()

    # Callback para cerrar mensaje
    elif query.data == "close_data":
        await query.message.delete()
        try:
            # Borrar también el mensaje al que responde (si existe)
            if query.message.reply_to_message:
                 await query.message.reply_to_message.delete()
        except Exception as e:
            logger.warning(f"No se pudo borrar el mensaje reply_to_message: {e}")
        return await query.answer("Mensaje cerrado.") # Opcional

    # --- Callbacks de Trial / Premium ---
    elif query.data == "get_trail":
        # Lógica para obtener prueba gratuita (si está implementada en DB)
        user_id = query.from_user.id
        free_trial_status = await db.get_free_trial_status(user_id) # Asume que existe
        if not free_trial_status:
            await db.give_free_trail(user_id) # Asume que existe
            await query.message.edit_text(text="🎉 ¡Prueba gratuita activada! Tienes acceso premium por tiempo limitado. Disfruta.")
        else:
            await query.message.edit_text(text="⚠️ Ya has utilizado tu prueba gratuita. Considera nuestros planes /premium.")
        return await query.answer(MSG_ALRT)

    elif query.data == "buy_premium":
         # Mostrar información de pago (QR, texto, enlace a admin)
         btn = [[InlineKeyboardButton("Contactar Administrador", url=OWNER_LINK)]] # Usar OWNER_LINK de config
         # Opcionalmente, añadir botón de cerrar
         btn.append([InlineKeyboardButton("Cerrar", callback_data="close_data")])
         caption_text = PAYMENT_TEXT or "Contacta al administrador para opciones de pago." # Usar PAYMENT_TEXT de config
         qr_photo = PAYMENT_QR # Usar PAYMENT_QR de config

         if qr_photo:
             try:
                 await query.message.reply_photo(
                     photo=qr_photo,
                     caption=caption_text,
                     reply_markup=InlineKeyboardMarkup(btn)
                 )
             except Exception as e:
                  logger.error(f"Error al enviar QR de pago: {e}")
                  await query.message.reply_text(caption_text, reply_markup=InlineKeyboardMarkup(btn)) # Fallback a texto
         else:
              await query.message.reply_text(caption_text, reply_markup=InlineKeyboardMarkup(btn))
         return await query.answer("Información de pago mostrada.")

    # --- Callbacks de Filtros (Manual/Global) ---
    elif query.data == "gfiltersdeleteallconfirm":
        # Verificar permisos de admin global
        if str(query.from_user.id) not in ADMINS:
             return await query.answer("❌ Solo los administradores globales pueden hacer esto.", show_alert=True)
        await del_allg(query.message, 'gfilters') # Asume que del_allg existe y funciona
        await query.answer("✅ Filtros globales eliminados.", show_alert=True)
        await query.message.delete() # Borrar mensaje de confirmación
        return
    elif query.data == "gfiltersdeleteallcancel":
        await query.message.delete() # Borrar mensaje de confirmación
        await query.answer("Operación cancelada.")
        return

    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        grp_id = None
        title = None

        if chat_type == enums.ChatType.PRIVATE:
            # Obtener conexión activa para el usuario en PM
            grp_id_str = await active_connection(str(userid)) # Asume que existe
            if grp_id_str:
                grp_id = int(grp_id_str)
                try:
                    chat = await client.get_chat(grp_id)
                    title = chat.title
                except Exception as e:
                    logger.error(f"Error obteniendo chat {grp_id} para /delall: {e}")
                    await query.message.edit_text("⚠️ Error al obtener información del grupo conectado. Asegúrate de que sigo en él.")
                    return await query.answer("Error", show_alert=True)
            else:
                await query.message.edit_text("❌ No estás conectado a ningún grupo. Usa /connect para vincular un grupo.", quote=True)
                return await query.answer(MSG_ALRT)

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title
        else:
            # No debería ocurrir en teoría
            return await query.answer("Comando no aplicable aquí.", show_alert=True)

        # Verificar Permisos (Admin del Bot o Admin/Owner del Grupo)
        is_admin = str(userid) in ADMINS
        is_chat_admin = False
        if not is_admin and grp_id:
            try:
                member = await client.get_chat_member(grp_id, userid)
                if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
                    is_chat_admin = True
            except Exception as e:
                 logger.error(f"Error verificando permisos en {grp_id} para {userid}: {e}")

        if is_admin or is_chat_admin:
             await del_all(query.message, grp_id, title) # Asume que del_all existe
             await query.answer(f"✅ Filtros eliminados para {title}.", show_alert=True)
        else:
             await query.answer("❌ Necesitas ser Administrador del bot o del grupo para hacer esto.", show_alert=True)
        return

    elif query.data == "delallcancel":
        # Cancelar borrado de filtros, borrar mensaje de confirmación
        # Verificar permisos básicos para borrar el mensaje de confirmación (evitar abuso)
        # (Opcional, pero buena práctica)
        await query.message.delete()
        try:
            if query.message.reply_to_message: # Borrar el mensaje original que activó el /delall
                 await query.message.reply_to_message.delete()
        except Exception:
            pass
        await query.answer("Operación cancelada.")
        return

    # --- Callbacks de Conexiones (PM <-> Grupo) ---
    elif query.data.startswith("groupcb"):
        await query.answer()
        try:
            _, group_id_str, act = query.data.split(":")
            group_id = int(group_id_str)
        except ValueError:
             return await query.message.edit_text("Error: Callback inválido.")

        try:
            hr = await client.get_chat(group_id)
            title = hr.title
        except Exception as e:
            logger.error(f"Error obteniendo chat {group_id} en groupcb: {e}")
            # Quizás el bot fue expulsado, eliminar conexión?
            # await delete_connection(str(query.from_user.id), str(group_id))
            return await query.message.edit_text(f"⚠️ No se pudo obtener información del grupo ID: {group_id}. Quizás ya no estoy allí.")

        # Definir botones de acción para esta conexión
        stat = "Desconectar" if act else "Conectar"
        cb = "disconnect" if act else "connectcb"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("Eliminar Conexión", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("⬅️ Volver", callback_data="backcb")]
        ])
        await query.message.edit_text(
            f"Grupo: **{title}**\nID: `{group_id}`\nEstado: {'Activa' if act else 'Inactiva'}",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    elif query.data.startswith("connectcb"):
        await query.answer()
        try:
            _, group_id_str = query.data.split(":")
            group_id = int(group_id_str)
        except ValueError:
             return await query.message.edit_text("Error: Callback inválido.")

        try:
            hr = await client.get_chat(group_id)
            title = hr.title
        except Exception as e:
            logger.error(f"Error obteniendo chat {group_id} en connectcb: {e}")
            return await query.message.edit_text(f"⚠️ No se pudo obtener información del grupo ID: {group_id}.")

        user_id = query.from_user.id
        mkact = await make_active(str(user_id), str(group_id)) # Asume que existe

        if mkact:
            await query.message.edit_text(
                f"✅ Conectado exitosamente al grupo **{title}**.",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            # Podría fallar si la conexión ya existe, etc.
            await query.message.edit_text('⚠️ Ocurrió un error al intentar conectar. ¿Ya estabas conectado?', parse_mode=enums.ParseMode.MARKDOWN)
        return # No necesita MSG_ALRT si edita el mensaje

    elif query.data.startswith("disconnect"):
        await query.answer()
        try:
            _, group_id_str = query.data.split(":")
            group_id = int(group_id_str) # No se usa realmente para desconectar, pero se recibe
        except ValueError:
             return await query.message.edit_text("Error: Callback inválido.")

        user_id = query.from_user.id
        mkinact = await make_inactive(str(user_id)) # Asume que existe

        if mkinact:
            await query.message.edit_text(
                f"✅ Desconectado de la sesión activa.",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"⚠️ Ocurrió un error al desconectar. ¿No tenías ninguna conexión activa?",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return

    elif query.data.startswith("deletecb"):
        await query.answer()
        try:
            _, group_id_str = query.data.split(":")
            group_id = int(group_id_str)
        except ValueError:
             return await query.message.edit_text("Error: Callback inválido.")

        user_id = query.from_user.id
        delcon = await delete_connection(str(user_id), str(group_id)) # Asume que existe

        if delcon:
            await query.message.edit_text(
                "✅ Conexión eliminada exitosamente."
            )
            # Volver a mostrar la lista de conexiones restantes
            await show_connections(client, query.message, user_id)
        else:
            await query.message.edit_text(
                f"⚠️ Ocurrió un error al eliminar la conexión.",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return

    elif query.data == "backcb":
        await query.answer()
        userid = query.from_user.id
        await show_connections(client, query.message, userid) # Función auxiliar para mostrar conexiones
        return

    # --- Callbacks de Alertas (Filtros Manuales/Globales) ---
    elif query.data.startswith("gfilteralert") or query.data.startswith("alertmessage"):
        try:
            # Extraer datos del callback
            parts = query.data.split(":")
            alert_type = parts[0] # 'gfilteralert' o 'alertmessage'
            index = int(parts[1])
            keyword = parts[2]
            grp_id = query.message.chat.id # El grupo donde se mostró el filtro

            # Obtener datos del filtro correspondiente
            if alert_type == 'gfilteralert':
                 reply_text, btn, alerts_str, fileid = await find_gfilter('gfilters', keyword)
            else: # alertmessage
                 reply_text, btn, alerts_str, fileid = await find_filter(grp_id, keyword)

            # Procesar y mostrar la alerta
            if alerts_str:
                 alerts = ast.literal_eval(alerts_str) # Convertir string a lista
                 if 0 <= index < len(alerts):
                     alert_text = alerts[index].replace("\\n", "\n").replace("\\t", "\t")
                     await query.answer(alert_text, show_alert=True)
                 else:
                     await query.answer("Índice de alerta inválido.", show_alert=True)
            else:
                 await query.answer("No hay alertas definidas para este filtro.", show_alert=True)

        except (ValueError, IndexError, SyntaxError, TypeError) as e:
            logger.error(f"Error procesando callback de alerta ({query.data}): {e}")
            await query.answer("Error al mostrar la alerta.", show_alert=True)
        return

    # --- Callbacks de Archivos (Clic en botón individual) ---
    elif query.data.startswith("file") or query.data.startswith("filep"): # file o filep (protegido)
        clicked_user_id = query.from_user.id
        original_requester_id = 0
        # Intentar obtener el ID del usuario que hizo la búsqueda original
        try:
            # Asume que el mensaje con botones es una respuesta al mensaje del usuario
            if query.message.reply_to_message and query.message.reply_to_message.from_user:
                 original_requester_id = query.message.reply_to_message.from_user.id
        except Exception:
            # Si falla, usar el ID del que hizo clic como fallback (menos seguro)
            original_requester_id = clicked_user_id
            logger.warning("No se pudo determinar el solicitante original, usando el ID del clicker.")

        # Verificar si el que hace clic es el solicitante original (si PING_MESSAGE está activado)
        if PING_MESSAGE and clicked_user_id != original_requester_id:
             return await query.answer(
                 f"👋 ¡Hola {query.from_user.first_name}! Este botón es para el usuario que hizo la solicitud original. Por favor, haz tu propia búsqueda.",
                 show_alert=True
            )

        # Extraer ID del archivo
        try:
            ident, file_id = query.data.split("#")
        except ValueError:
            return await query.answer("Callback de archivo inválido.", show_alert=True)

        # Obtener detalles del archivo
        file_details = await get_file_details(file_id)
        if not file_details:
            return await query.answer('❌ No se encontró este archivo en la base de datos. Puede haber sido eliminado.', show_alert=True)

        # --- Lógica de Shortlink (Global y Premium) ---
        is_premium = await db.has_premium_access(clicked_user_id)
        use_shortlink = SHORTLINK_ENABLED and not is_premium

        # Construir el payload para el enlace /start
        start_payload = f"{ident}_{file_id}" # ident es 'file' o 'filep'

        # Generar el enlace final (directo o con shortlink)
        final_url = f"https://t.me/{temp.U_NAME}?start={start_payload}"

        if use_shortlink and SHORTLINK_URL and SHORTLINK_API:
            try:
                 shortened_url = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, final_url)
                 if shortened_url: # Verificar si el acortador funcionó
                     final_url = shortened_url
                 else:
                     logger.warning(f"El acortador falló para {final_url}, usando enlace directo.")
            except Exception as e:
                 logger.error(f"Error al acortar enlace {final_url}: {e}")
                 # Usar enlace directo como fallback

        # Responder al callback con la URL para que Telegram la abra
        try:
            await query.answer(url=final_url)
        except UserIsBlocked:
            await query.answer('⚠️ ¡Debes desbloquearme para que pueda enviarte el archivo!', show_alert=True)
        except PeerIdInvalid:
            # Este error a veces ocurre, intentar de nuevo puede funcionar
            await query.answer(url=final_url)
        except Exception as e:
            logger.error(f"Error inesperado en query.answer(url=...): {e}")
            # Como último recurso, intentar enviar la URL como mensaje
            try:
                 await query.message.reply_text(f"No pude abrir el enlace directamente. Aquí tienes: {final_url}", quote=True)
            except Exception:
                 pass # Si incluso enviar mensaje falla
        return

    # --- Callbacks de "Enviar Todo" (Premium) ---
    elif query.data.startswith("sendfiles"):
        clicked_user_id = query.from_user.id
        original_requester_id = 0
        try:
            if query.message.reply_to_message and query.message.reply_to_message.from_user:
                 original_requester_id = query.message.reply_to_message.from_user.id
        except Exception:
            original_requester_id = clicked_user_id

        # Verificar solicitante original si PING_MESSAGE está activo
        if PING_MESSAGE and clicked_user_id != original_requester_id:
             return await query.answer(
                 f"👋 ¡Hola {query.from_user.first_name}! Este botón es para el usuario que hizo la solicitud original.",
                 show_alert=True
            )

        # --- VERIFICACIÓN PREMIUM ---
        is_premium = await db.has_premium_access(clicked_user_id)
        if not is_premium:
            # Si NO es premium, mostrar alerta y detener
            return await query.answer("⭐ ¡Ups! La función 'Enviar Todo' es exclusiva para usuarios Premium.", show_alert=True)

        # Si ES premium, proceder:
        try:
            ident, key = query.data.split("#") # ident es 'sendfiles'
        except ValueError:
            return await query.answer("Callback 'Enviar Todo' inválido.", show_alert=True)

        # Obtener la clave de búsqueda (si aún existe)
        search_query = FRESH.get(key)
        if not search_query:
            return await query.answer("⚠️ Esta búsqueda ha expirado. Realiza la búsqueda de nuevo.", show_alert=True)

        # Obtener configuración de protección de contenido
        settings = await get_settings(query.message.chat.id)
        file_prefix = 'allfilesp' if settings.get('file_secure') else 'allfiles'

        # Construir payload /start (sin shortlink, ya que es premium)
        start_payload = f"{file_prefix}_{key}" # prefijo + key de búsqueda
        final_url = f"https://t.me/{temp.U_NAME}?start={start_payload}"

        try:
            await query.answer(url=final_url)
        except UserIsBlocked:
            await query.answer('⚠️ ¡Debes desbloquearme para que pueda enviarte los archivos!', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=final_url)
        except Exception as e:
            logger.error(f"Error inesperado en query.answer(url=...) para sendfiles: {e}")
            try:
                 await query.message.reply_text(f"No pude abrir el enlace directamente. Aquí tienes: {final_url}", quote=True)
            except Exception:
                 pass
        return

    # --- Callback Force Subscribe (Desmutear) ---
    elif query.data.startswith("unmuteme"):
        ident, user_id_to_unmute_str = query.data.split("#")
        user_id_to_unmute = int(user_id_to_unmute_str)

        # Verificar que el usuario que hace clic es el que debe ser desmuteado
        if query.from_user.id != user_id_to_unmute:
            return await query.answer("❌ Este botón no es para ti.", show_alert=True)

        # Obtener canal de suscripción forzada desde settings del grupo
        settings = await get_settings(query.message.chat.id)
        fsub_channel_id = settings.get('fsub')

        if not fsub_channel_id:
             # Si FS está desactivado, igual intentar desmutear por si acaso quedó muteado antes
             try:
                  await client.unban_chat_member(query.message.chat.id, user_id_to_unmute)
                  await query.answer("✅ ¡Listo! Ya puedes hablar.", show_alert=True)
                  await query.message.delete() # Borrar mensaje de "unirse"
             except Exception as e:
                  logger.error(f"Error al desmutear (FS desactivado) a {user_id_to_unmute} en {query.message.chat.id}: {e}")
                  await query.answer("Ocurrió un error al intentar desmutearte.", show_alert=True)
             return

        # Verificar si ahora SÍ está suscrito
        try:
            # pub_is_subscribed debe devolver None si está suscrito
            btns = await pub_is_subscribed(client, query, fsub_channel_id)
            if btns: # Si devuelve botones, significa que AÚN NO se ha unido
                await query.answer("🤔 Parece que todavía no te has unido al canal. Por favor, únete y vuelve a intentarlo.", show_alert=True)
            else: # Si devuelve None, SÍ se ha unido
                await client.unban_chat_member(query.message.chat.id, user_id_to_unmute) # unban = unmute
                await query.answer("✅ ¡Genial! Gracias por unirte. Ya puedes hablar.", show_alert=True)
                await query.message.delete() # Borrar mensaje de "unirse"
        except Exception as e:
            logger.error(f"Error verificando suscripción/desmuteando a {user_id_to_unmute} en {query.message.chat.id}: {e}")
            await query.answer("Ocurrió un error al verificar tu suscripción o desmutearte.", show_alert=True)
        return

    # --- Callback para eliminar archivos defectuosos (Admin) ---
    elif query.data.startswith("killfilesdq"):
         # Verificar si es admin del bot
         if str(query.from_user.id) not in ADMINS:
              return await query.answer("❌ Comando solo para administradores.", show_alert=True)

         try:
             ident, keyword = query.data.split("#")
         except ValueError:
              return await query.answer("Callback inválido.", show_alert=True)

         await query.message.edit_text(f"Buscando archivos para eliminar con el término: '{keyword}'...")
         files_to_delete, total_found = await get_bad_files(keyword) # Asume que existe

         if not files_to_delete:
              return await query.message.edit_text(f"No se encontraron archivos para eliminar con '{keyword}'.")

         await query.message.edit_text(f"Se encontraron {total_found} archivos para '{keyword}'.\nIniciando proceso de borrado en 5 segundos...")
         await asyncio.sleep(5)

         deleted_count = 0
         errors_count = 0
         async with lock: # Usar lock si hay riesgo de concurrencia
             try:
                 for file_doc in files_to_delete:
                     file_id_to_delete = file_doc.get("file_id")
                     file_name = file_doc.get("file_name", "N/A")
                     if not file_id_to_delete:
                         errors_count += 1
                         continue

                     # Intentar borrar de la colección principal
                     result1 = await col.delete_one({'file_id': file_id_to_delete})
                     # Si no se borró de la principal, intentar en la secundaria
                     result2 = None
                     if result1.deleted_count == 0 and sec_col: # Verificar si sec_col existe
                           result2 = await sec_col.delete_one({'file_id': file_id_to_delete})

                     if result1.deleted_count > 0 or (result2 and result2.deleted_count > 0):
                         deleted_count += 1
                         logger.info(f"Admin {query.from_user.id} eliminó archivo {file_id_to_delete} ({file_name}) usando keyword '{keyword}'.")
                     else:
                         logger.warning(f"No se pudo eliminar el archivo {file_id_to_delete} ({file_name}) con keyword '{keyword}'. ¿Ya estaba borrado?")
                         errors_count +=1 # Contar como error si no se borró de ninguna

                     # Actualizar estado cada 50 eliminaciones
                     if deleted_count > 0 and deleted_count % 50 == 0:
                          await query.message.edit_text(f"Borrando archivos para '{keyword}'...\nEliminados: {deleted_count}\nErrores: {errors_count}\nTotal encontrados: {total_found}\n\nPor favor espera...")

             except Exception as e:
                 logger.exception(f"Error durante la eliminación masiva con keyword '{keyword}': {e}")
                 await query.message.edit_text(f'Error durante el proceso: {e}')
             else:
                 await query.message.edit_text(f"✅ Proceso de borrado completado para '{keyword}'.\n\nEliminados exitosamente: {deleted_count}\nNo encontrados/Errores: {errors_count}\nTotal encontrados inicialmente: {total_found}")
         return

    # --- Callbacks de Configuración (/settings) ---
    elif query.data.startswith(("opnsetgrp", "opnsetpm")): # Abrir menú settings
         # Verificar permisos (Admin Bot o Admin Grupo)
         is_admin = str(query.from_user.id) in ADMINS
         is_chat_admin = False
         try:
             # Extraer group_id del callback
             ident, grp_id_str = query.data.split("#")
             grp_id = int(grp_id_str)
             # Verificar admin del chat si no es admin del bot
             if not is_admin:
                  member = await client.get_chat_member(grp_id, query.from_user.id)
                  if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
                       is_chat_admin = True
         except (ValueError, IndexError, Exception) as e:
             logger.error(f"Error procesando opnset* callback o verificando permisos: {e}")
             return await query.answer("Error al abrir configuración o verificar permisos.", show_alert=True)

         if not (is_admin or is_chat_admin):
              return await query.answer("❌ No tienes permisos para cambiar la configuración de este grupo.", show_alert=True)

         # Obtener settings actuales
         settings = await get_settings(grp_id)
         if settings is None:
              # Inicializar settings si no existen? O mostrar error?
              # await save_group_settings(grp_id, default_settings) # Necesitaría default_settings
              # settings = await get_settings(grp_id)
              # O mostrar error:
              logger.error(f"No se encontraron settings para el grupo {grp_id}")
              return await query.answer("Error: No se encontró la configuración de este grupo.", show_alert=True)

         # Construir botones del menú de configuración
         # Quitado: Shortlink (is_shortlink) - ahora es global
         buttons = [
             [
                 InlineKeyboardButton('Formato Resultados', callback_data=f'setgs#button#{settings.get("button", True)}#{grp_id}'),
                 InlineKeyboardButton('Botones' if settings.get("button", True) else 'Texto', callback_data=f'setgs#button#{settings.get("button", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Contenido Protegido', callback_data=f'setgs#file_secure#{settings.get("file_secure", False)}#{grp_id}'),
                 InlineKeyboardButton('🔒 Sí' if settings.get("file_secure", False) else '🔓 No', callback_data=f'setgs#file_secure#{settings.get("file_secure", False)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Mostrar Info IMDb', callback_data=f'setgs#imdb#{settings.get("imdb", True)}#{grp_id}'),
                 InlineKeyboardButton('🎬 Sí' if settings.get("imdb", True) else '🚫 No', callback_data=f'setgs#imdb#{settings.get("imdb", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Corrector Ortográfico', callback_data=f'setgs#spell_check#{settings.get("spell_check", True)}#{grp_id}'),
                 InlineKeyboardButton('✍️ Sí' if settings.get("spell_check", True) else '🚫 No', callback_data=f'setgs#spell_check#{settings.get("spell_check", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Mensaje Bienvenida', callback_data=f'setgs#welcome#{settings.get("welcome", True)}#{grp_id}'),
                 InlineKeyboardButton('👋 Sí' if settings.get("welcome", True) else '🚫 No', callback_data=f'setgs#welcome#{settings.get("welcome", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Auto-Borrado (Resultados)', callback_data=f'setgs#auto_delete#{settings.get("auto_delete", False)}#{grp_id}'),
                 InlineKeyboardButton(f'🗑️ {AUTO_DELETE_SECONDS // 60} min' if settings.get("auto_delete", False) else '🚫 No', callback_data=f'setgs#auto_delete#{settings.get("auto_delete", False)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Auto-Filtro (al buscar)', callback_data=f'setgs#auto_ffilter#{settings.get("auto_ffilter", True)}#{grp_id}'),
                 InlineKeyboardButton('🔍 Sí' if settings.get("auto_ffilter", True) else '🚫 No', callback_data=f'setgs#auto_ffilter#{settings.get("auto_ffilter", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Max Botones (Paginación)', callback_data=f'setgs#max_btn#{settings.get("max_btn", True)}#{grp_id}'),
                 InlineKeyboardButton('🔟 (10)' if settings.get("max_btn", True) else f'{MAX_B_TN}', callback_data=f'setgs#max_btn#{settings.get("max_btn", True)}#{grp_id}')
             ],
             [ # Botón para cerrar el menú de settings
                 InlineKeyboardButton("✅ Cerrar Configuración", callback_data="close_data")
             ]
         ]
         reply_markup = InlineKeyboardMarkup(buttons)
         chat_title = query.message.chat.title if query.message.chat else f"Grupo ID {grp_id}"

         # Decidir dónde mostrar el menú
         if ident == "opnsetgrp": # Mostrar en el grupo
             await query.message.edit_text(
                 text=f"⚙️ Configuración para <b>{chat_title}</b>:",
                 reply_markup=reply_markup,
                 parse_mode=enums.ParseMode.HTML
             )
         else: # opnsetpm - Enviar a PM
             try:
                 await client.send_message(
                     chat_id=query.from_user.id,
                     text=f"⚙️ Configuración para <b>{chat_title}</b>:",
                     reply_markup=reply_markup,
                     parse_mode=enums.ParseMode.HTML,
                     # reply_to_message_id=query.message.id # Puede fallar si el mensaje original en grupo se borra
                 )
                 # Confirmar en el grupo que se envió a PM
                 await query.message.edit_text(
                     f"✅ El menú de configuración para <b>{chat_title}</b> ha sido enviado a tus mensajes privados.",
                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Abrir PM", url=f"tg://user?id={query.from_user.id}")]])
                 )
             except UserIsBlocked:
                 await query.answer("⚠️ No puedo enviarte el menú porque me has bloqueado.", show_alert=True)
             except Exception as e:
                  logger.error(f"Error enviando settings a PM {query.from_user.id}: {e}")
                  await query.answer("Ocurrió un error al enviar la configuración a tu PM.", show_alert=True)
         return await query.answer(MSG_ALRT) # Answer al callback original

    elif query.data.startswith("setgs"): # Cambiar un setting específico
         # Verificar permisos (Admin Bot o Admin Grupo) - ¡IMPORTANTE!
         try:
             ident, set_type, status_str, grp_id_str = query.data.split("#")
             grp_id = int(grp_id_str)
             current_status = status_str == "True" # Estado actual antes del cambio
             new_status = not current_status # El nuevo estado a guardar
         except (ValueError, IndexError):
              return await query.answer("Callback de configuración inválido.", show_alert=True)

         # Re-verificar permisos antes de cambiar nada
         is_admin = str(query.from_user.id) in ADMINS
         is_chat_admin = False
         if not is_admin:
              try:
                   member = await client.get_chat_member(grp_id, query.from_user.id)
                   if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
                        is_chat_admin = True
              except Exception:
                   pass # Falló la verificación

         if not (is_admin or is_chat_admin):
              return await query.answer("❌ No tienes permisos para cambiar esta configuración.", show_alert=True)

         # Verificar conexión activa (si se edita desde PM)
         if query.message.chat.type == enums.ChatType.PRIVATE:
              active_grp_id = await active_connection(str(query.from_user.id))
              if str(grp_id) != active_grp_id:
                   await query.message.edit_text("⚠️ Tu conexión activa ha cambiado. Por favor, ve a /connections y selecciona el grupo correcto antes de cambiar su configuración.")
                   return await query.answer("Conexión cambiada", show_alert=True)

         # Guardar el nuevo setting
         await save_group_settings(grp_id, set_type, new_status) # Asume que existe y funciona

         # Refrescar el menú de settings con el valor actualizado
         settings = await get_settings(grp_id)
         if settings is None: # Fallback por si acaso
             return await query.answer("Error al recargar la configuración.", show_alert=True)

         # Reconstruir botones (similar a opnsetgrp/opnsetpm)
         # Quitado: Shortlink (is_shortlink)
         buttons = [
             [
                 InlineKeyboardButton('Formato Resultados', callback_data=f'setgs#button#{settings.get("button", True)}#{grp_id}'),
                 InlineKeyboardButton('Botones' if settings.get("button", True) else 'Texto', callback_data=f'setgs#button#{settings.get("button", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Contenido Protegido', callback_data=f'setgs#file_secure#{settings.get("file_secure", False)}#{grp_id}'),
                 InlineKeyboardButton('🔒 Sí' if settings.get("file_secure", False) else '🔓 No', callback_data=f'setgs#file_secure#{settings.get("file_secure", False)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Mostrar Info IMDb', callback_data=f'setgs#imdb#{settings.get("imdb", True)}#{grp_id}'),
                 InlineKeyboardButton('🎬 Sí' if settings.get("imdb", True) else '🚫 No', callback_data=f'setgs#imdb#{settings.get("imdb", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Corrector Ortográfico', callback_data=f'setgs#spell_check#{settings.get("spell_check", True)}#{grp_id}'),
                 InlineKeyboardButton('✍️ Sí' if settings.get("spell_check", True) else '🚫 No', callback_data=f'setgs#spell_check#{settings.get("spell_check", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Mensaje Bienvenida', callback_data=f'setgs#welcome#{settings.get("welcome", True)}#{grp_id}'),
                 InlineKeyboardButton('👋 Sí' if settings.get("welcome", True) else '🚫 No', callback_data=f'setgs#welcome#{settings.get("welcome", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Auto-Borrado (Resultados)', callback_data=f'setgs#auto_delete#{settings.get("auto_delete", False)}#{grp_id}'),
                 InlineKeyboardButton(f'🗑️ {AUTO_DELETE_SECONDS // 60} min' if settings.get("auto_delete", False) else '🚫 No', callback_data=f'setgs#auto_delete#{settings.get("auto_delete", False)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Auto-Filtro (al buscar)', callback_data=f'setgs#auto_ffilter#{settings.get("auto_ffilter", True)}#{grp_id}'),
                 InlineKeyboardButton('🔍 Sí' if settings.get("auto_ffilter", True) else '🚫 No', callback_data=f'setgs#auto_ffilter#{settings.get("auto_ffilter", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton('Max Botones (Paginación)', callback_data=f'setgs#max_btn#{settings.get("max_btn", True)}#{grp_id}'),
                 InlineKeyboardButton('🔟 (10)' if settings.get("max_btn", True) else f'{MAX_B_TN}', callback_data=f'setgs#max_btn#{settings.get("max_btn", True)}#{grp_id}')
             ],
             [
                 InlineKeyboardButton("✅ Cerrar Configuración", callback_data="close_data")
             ]
         ]
         reply_markup = InlineKeyboardMarkup(buttons)

         try:
             # Editar el mensaje actual con los botones actualizados
             await query.edit_message_reply_markup(reply_markup)
             await query.answer(f"✅ {set_type} {'activado' if new_status else 'desactivado'}")
         except MessageNotModified:
             await query.answer(f"{set_type} ya estaba {'activado' if new_status else 'desactivado'}")
         except Exception as e:
             logger.error(f"Error al editar markup en setgs: {e}")
             await query.answer("Error al actualizar la interfaz.", show_alert=True)
         return

    # --- Callbacks Menú Principal y Ayuda (/start, /help) ---
    # Se han eliminado callbacks de funciones no deseadas (ytdl, song, etc.)
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Añádeme a tu Grupo ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ],[
            InlineKeyboardButton('🫂 Grupo Principal', url=GRP_LNK), # Usar GRP_LNK de config
            InlineKeyboardButton('📣 Canal Updates', url=CHNL_LNK) # Usar CHNL_LNK de config
        ],[
            InlineKeyboardButton('❓ Ayuda', callback_data='help'),
            InlineKeyboardButton('ℹ️ Acerca de', callback_data='about')
        ]]
        # Añadir botón premium/referral si está activado
        if PREMIUM_AND_REFERAL_MODE:
             buttons.append([InlineKeyboardButton('⭐ Premium / Referidos', callback_data='subscription')])

        reply_markup = InlineKeyboardMarkup(buttons)
        # Usar InputMediaPhoto para evitar errores si PICS está vacío o tiene errores
        try:
            await client.edit_message_media(
                query.message.chat.id,
                query.message.id,
                InputMediaPhoto(random.choice(PICS) if PICS else "https://via.placeholder.com/600x300.png?text=Bot+Activo") # Fallback image
            )
        except Exception as e:
            logger.warning(f"Error al cambiar media en /start: {e}. Ignorando cambio de media.")

        # Texto de inicio desde Script.py (necesita traducción)
        start_text = script.START_TXT.format(mention=query.from_user.mention, bot_name=temp.B_NAME, bot_username=temp.U_NAME)
        await query.message.edit_text(
            text=start_text,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        await query.answer(MSG_ALRT)

    elif query.data == "help":
        # Botones de Ayuda (Simplificados)
        buttons = [[
             InlineKeyboardButton('👮 Comandos Admin', callback_data='admin'),
             InlineKeyboardButton('👤 Comandos Usuario', callback_data='user_cmds')
         ],[
             InlineKeyboardButton('⚙️ Conexiones PM-Grupo', callback_data='coct'),
             InlineKeyboardButton('💾 Filtros Manuales', callback_data='filters')
         ],[
             InlineKeyboardButton('🆔 Obtener ID Sticker', callback_data='sticker'),
             InlineKeyboardButton('⭐ Premium / Referidos', callback_data='subscription') # Si aplica
         ],[
             InlineKeyboardButton('🏠 Inicio', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        # Usar InputMediaPhoto
        try:
            await client.edit_message_media(
                query.message.chat.id,
                query.message.id,
                InputMediaPhoto(random.choice(PICS) if PICS else "https://via.placeholder.com/600x300.png?text=Ayuda") # Fallback
            )
        except Exception as e:
             logger.warning(f"Error al cambiar media en /help: {e}. Ignorando.")

        # Texto de ayuda desde Script.py (necesita traducción)
        help_text = script.HELP_TXT.format(mention=query.from_user.mention)
        await query.message.edit_text(
            text=help_text,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        await query.answer(MSG_ALRT)

    elif query.data == "about":
         buttons = [[
            InlineKeyboardButton('🫂 Grupo Soporte', url=GRP_LNK), # Usar GRP_LNK de config
            InlineKeyboardButton('📣 Canal Updates', url=CHNL_LNK) # Usar CHNL_LNK de config
         ],[
             InlineKeyboardButton(' Dᴏɴᴀʀ', url=DONATE_LINK), # Puedes definirlo en config.py
             InlineKeyboardButton('🧑‍💻 Dueño', url=OWNER_LINK) # Usar OWNER_LINK de config
         ],[
             InlineKeyboardButton('🏠 Inicio', callback_data='start'),
             InlineKeyboardButton('Cerrar', callback_data='close_data')
         ]]
         reply_markup = InlineKeyboardMarkup(buttons)
         try:
             await client.edit_message_media(
                 query.message.chat.id,
                 query.message.id,
                 InputMediaPhoto(random.choice(PICS) if PICS else "https://via.placeholder.com/600x300.png?text=Acerca+De") # Fallback
             )
         except Exception as e:
             logger.warning(f"Error al cambiar media en /about: {e}. Ignorando.")
         # Texto About desde Script.py (necesita traducción)
         about_text = script.ABOUT_TXT.format(bot_name=temp.B_NAME, bot_username=temp.U_NAME, owner_link=OWNER_LNK)
         await query.message.edit_text(
             text=about_text,
             reply_markup=reply_markup,
             parse_mode=enums.ParseMode.HTML,
             disable_web_page_preview=True
         )
         await query.answer(MSG_ALRT)

    elif query.data == "subscription":
         buttons = [[
             InlineKeyboardButton('⬅️ Volver', callback_data='start')
             # Añadir botón de planes si existe
             # InlineKeyboardButton('Ver Planes', callback_data='view_plans')
         ]]
         reply_markup = InlineKeyboardMarkup(buttons)
         try:
             await client.edit_message_media(
                 query.message.chat.id,
                 query.message.id,
                 InputMediaPhoto(random.choice(PICS) if PICS else "https://via.placeholder.com/600x300.png?text=Premium") # Fallback
             )
         except Exception as e:
             logger.warning(f"Error al cambiar media en /subscription: {e}. Ignorando.")

         # Texto Premium/Referral desde Script.py (necesita traducción y ajuste de variables)
         # Asegúrate que REFERAL_PREMIUM_TIME, REFERAL_COUNT estén definidos en config/info
         ref_time = REFERAL_PREMIUM_TIME or "un tiempo"
         ref_count = REFERAL_COUNT or 5
         sub_text = script.SUBSCRIPTION_TXT.format(
             refer_premium_time=ref_time,
             bot_username=temp.U_NAME,
             user_id=query.from_user.id,
             refer_count=ref_count
         )
         await query.message.edit_text(
             text=sub_text,
             reply_markup=reply_markup,
             parse_mode=enums.ParseMode.HTML,
             disable_web_page_preview=True
         )
         await query.answer(MSG_ALRT)

    # --- Secciones de Ayuda Específicas (Simplificadas) ---
    elif query.data == "filters": # Ayuda sobre filtros manuales
        buttons = [[
            InlineKeyboardButton('✍️ Formato Texto', callback_data='manuelfilter'),
            InlineKeyboardButton('🔘 Formato Botones', callback_data='button')
        ],[
            InlineKeyboardButton('⬅️ Volver a Ayuda', callback_data='help')
            # Considerar añadir botón a Filtros Globales si existe esa ayuda
            # InlineKeyboardButton('🌍 Filtros Globales', callback_data='global_filters_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        # Media
        try:
            await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /filters: {e}")
        # Texto (Desde Script.py)
        filters_text = script.ALL_FILTERS.format(mention=query.from_user.mention) # Asegúrate que existe en script
        await query.message.edit_text(
            text=filters_text,
            reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
        )

    elif query.data == "manuelfilter": # Ayuda formato texto filtro
        buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='filters') ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /manuelfilter: {e}")
        # Texto (Desde Script.py)
        manualfilter_text = script.MANUELFILTER_TXT # Asegúrate que existe en script
        await query.message.edit_text(
             text=manualfilter_text,
             reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
        )

    elif query.data == "button": # Ayuda formato botones filtro
        buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='filters') ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /button: {e}")
        # Texto (Desde Script.py)
        button_text = script.BUTTON_TXT # Asegúrate que existe en script
        await query.message.edit_text(
            text=button_text,
            reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
        )

    # elif query.data == "autofilter": # Ayuda sobre autofiltro (si es necesaria)
    #     buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='help') ]]
    #     # Media, Texto (desde Script.py: script.AUTOFILTER_TXT)

    elif query.data == "coct": # Ayuda sobre conexiones
        buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='help') ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /coct: {e}")
        # Texto (Desde Script.py)
        connection_text = script.CONNECTION_TXT # Asegúrate que existe en script
        await query.message.edit_text(
            text=connection_text,
            reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
        )

    elif query.data == "admin": # Ayuda Comandos Admin
        buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='help') ]]
             # Quizás añadir botón a comandos extra si existen
             # InlineKeyboardButton('Otros Comandos', callback_data='extra_admin_cmds')
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /admin: {e}")
        # Texto (Desde Script.py)
        admin_text = script.ADMIN_TXT # Asegúrate que existe en script
        await query.message.edit_text(
            text=admin_text,
            reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
        )

    elif query.data == "user_cmds": # Ayuda Comandos Usuario (si se separa de /help principal)
         buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='help') ]]
         reply_markup = InlineKeyboardMarkup(buttons)
         # Media...
         # Texto (Crear script.USER_CMDS_TXT o similar)
         user_cmds_text = "Aquí la lista de comandos para usuarios: /start, /help, /connect, /disconnect, /connections, /info, etc."
         await query.message.edit_text(
             text=user_cmds_text,
             reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
         )

    elif query.data == "sticker": # Ayuda Sticker ID
        buttons = [[ InlineKeyboardButton('⬅️ Volver', callback_data='help') ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /sticker: {e}")
        # Texto (Desde Script.py)
        sticker_text = script.STICKER_TXT # Asegúrate que existe en script
        await query.message.edit_text(
            text=sticker_text,
            reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
        )

    # --- Callbacks Estadísticas (/stats) ---
    # Mover /stats a comandos si es posible, pero si se queda en callback:
    elif query.data == "stats" or query.data == "rfrsh": # Mostrar o refrescar stats
        # Verificar permisos (Solo Admins del Bot)
        if str(query.from_user.id) not in ADMINS:
            return await query.answer("❌ Comando solo para administradores.", show_alert=True)

        if query.data == "rfrsh":
            await query.answer("Actualizando estadísticas...")

        buttons = [[
            InlineKeyboardButton('⬅️ Volver', callback_data='admin'), # O 'help' si se accede desde ahí
            InlineKeyboardButton('🔄 Refrescar', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)

        try: # Intentar editar media si no es un refresh rápido
            if query.data == "stats": # Solo cambiar imagen la primera vez
                await client.edit_message_media( query.message.chat.id, query.message.id, InputMediaPhoto(random.choice(PICS) if PICS else "fallback_image_url"))
        except Exception as e: logger.warning(f"Error media /stats: {e}")

        # Obtener datos
        total_users = await db.total_users_count()
        total_chats = await db.total_chat_count()
        files_main_db = await col.count_documents({}) if col else 0 # Contar en DB principal
        files_sec_db = await sec_col.count_documents({}) if sec_col else 0 # Contar en DB secundaria (si existe)
        total_files = files_main_db + files_sec_db

        # Obtener tamaño de DB (puede ser lento o requerir permisos especiales en Atlas)
        db_size_main = db_size_sec = db_size_conn = "N/A"
        try:
             if vjdb: # Si la conexión a la DB principal de archivos está activa
                  stats_main = await vjdb.command('dbStats')
                  db_size_main = f"{(stats_main.get('dataSize', 0) + stats_main.get('indexSize', 0)) / (1024*1024):.2f} MB"
             if sec_db: # Si la conexión a la DB secundaria de archivos está activa
                  stats_sec = await sec_db.command('dbStats')
                  db_size_sec = f"{(stats_sec.get('dataSize', 0) + stats_sec.get('indexSize', 0)) / (1024*1024):.2f} MB"
             if mydb: # Si la conexión a la DB de conexiones/usuarios está activa
                  stats_conn = await mydb.command('dbStats')
                  db_size_conn = f"{(stats_conn.get('dataSize', 0) + stats_conn.get('indexSize', 0)) / (1024*1024):.2f} MB"
        except Exception as e:
            logger.error(f"Error obteniendo dbStats: {e}")
            db_size_main = db_size_sec = db_size_conn = "Error"

        # Texto de Estadísticas (Usar script.STATUS_TXT y traducir/adaptar)
        stats_text = f"""📊 <b>Estadísticas del Bot</b> 📊

👤 <b>Usuarios Totales:</b> {total_users}
👥 <b>Chats Totales:</b> {total_chats}

🗂️ <b>Archivos Indexados:</b>
   - DB Principal: {files_main_db}
   - DB Secundaria: {files_sec_db}
   - <b>Total: {total_files}</b>

💾 <b>Tamaño Bases de Datos (aprox):</b>
   - Archivos (Main): {db_size_main}
   - Archivos (Sec): {db_size_sec}
   - Usuarios/Conexiones: {db_size_conn}
"""
        try:
            await query.message.edit_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        except MessageNotModified:
            # Si el texto no cambió (refresh rápido), solo responder al callback
            pass
        # Responder al callback original de stats o rfrsh
        if query.data == "stats":
           await query.answer(MSG_ALRT)
        # No es necesario responder a rfrsh si ya se hizo antes
        return


    # --- Callbacks residuales o desconocidos ---
    # Si llega aquí, es un callback no manejado explícitamente
    # Podríamos loggearlo o simplemente ignorarlo
    else:
        logger.warning(f"Callback no manejado recibido: {query.data}")
        await query.answer("Opción no reconocida o desactualizada.", show_alert=True) # Informar al usuario


# --- Funciones Auxiliares (Refactorizadas o Nuevas) ---

async def show_connections(client, message, user_id):
    """Función auxiliar para mostrar las conexiones de un usuario."""
    groupids = await all_connections(str(user_id)) # Asume que existe
    if not groupids:
        await message.edit_text("🔗 No tienes conexiones activas. Usa /connect en un grupo para empezar.")
        return

    buttons = []
    active_found = False
    for groupid_str in groupids:
        try:
            groupid = int(groupid_str)
            ttl = await client.get_chat(groupid)
            title = ttl.title
            active = await if_active(str(user_id), str(groupid)) # Asume que existe
            act_indicator = " (Activa)" if active else ""
            if active: active_found = True
            buttons.append(
                [InlineKeyboardButton(text=f"{title}{act_indicator}", callback_data=f"groupcb:{groupid}:{active}")]
            )
        except Exception as e:
             logger.warning(f"Error obteniendo info del grupo {groupid_str} para conexiones de {user_id}: {e}")
             # Opcional: Añadir botón para eliminar conexión rota?
             # buttons.append([InlineKeyboardButton(f"Grupo ID {groupid_str} (Error)", callback_data=f"deletecb:{groupid_str}")])
             pass # Ignorar grupos inaccesibles

    if not buttons: # Si todos los grupos dieron error
        await message.edit_text("🔗 No se pudieron cargar tus conexiones. Inténtalo de nuevo más tarde.")
        return

    # Añadir mensaje si ninguna conexión está activa
    conn_text = "🔗 Tus conexiones:\nSelecciona una para ver opciones."
    if not active_found:
        conn_text += "\n\n<i>(Ninguna conexión está activa. Haz clic en una y luego en 'Conectar' para activarla)</i>"

    # Añadir botón para cerrar
    buttons.append([InlineKeyboardButton("Cerrar", callback_data="close_data")])

    await message.edit_text(
        conn_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )


async def auto_filter(client, name, msg, reply_msg, ai_search, spoll=False):
    # Hora de inicio para calcular tiempo de búsqueda
    start_time_utc = datetime.now(pytz.utc)

    message = None
    search = ""
    files = []
    offset = 0
    total_results = 0
    user_id = 0
    chat_id = 0
    message_id = 0 # ID del mensaje original del usuario

    if not spoll: # Búsqueda normal (no desde corrección ortográfica)
        message = msg
        user_id = message.from_user.id if message.from_user else 0
        chat_id = message.chat.id
        message_id = message.id

        # Ignorar comandos y patrones no deseados
        if message.text.startswith("/") or re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            try: await reply_msg.delete() # Borrar "Buscando..." si es un comando
            except: pass
            return

        # Simplificar y limpiar consulta de búsqueda
        search = name.lower()
        # Eliminar palabras comunes/innecesarias (personalizar según idioma/uso)
        common_words = ["pelicula", "serie", "episodio", "temporada", "completa", "descargar", "ver", "online", "español", "latino", "subtitulado", "audio", "calidad", "hd", "fullhd", "4k", "castellano", "ingles", "original", "movie", "series", "episode", "season", "full", "download", "watch", "online", "spanish", "english", "audio", "quality", "dubbed", "subbed", "pls", "please", "busca", "encuentra", "quiero", "necesito", "puedes", "tienes"]
        # Quitar puntuación básica y espacios extra
        search = re.sub(r'[.,;:!?"\'`´’‘]', '', search)
        search_words = search.split()
        # Filtrar palabras comunes y reconstruir
        filtered_words = [word for word in search_words if word not in common_words]
        search = " ".join(filtered_words).strip()

        # Si la búsqueda queda vacía o muy corta, no buscar
        if not search or len(search) < 3:
            await reply_msg.edit_text(f"⚠️ Tu búsqueda '{name}' es muy corta o no contiene términos válidos. Intenta ser más específico.")
            return

        # Obtener resultados de la base de datos
        # Usar chat_id para filtros específicos si aplica, o global si es PM/configurado
        files, offset, total_results = await get_search_results(chat_id, search, offset=0, filter=True)

    else: # Búsqueda desde corrección ortográfica (spoll=True)
        # msg aquí es la CallbackQuery
        message = msg.message.reply_to_message # El mensaje original del usuario
        if not message: # Si el mensaje original fue borrado
             await reply_msg.edit_text("⚠️ Error: No se encontró el mensaje de búsqueda original.")
             return

        user_id = message.from_user.id if message.from_user else 0
        chat_id = message.chat.id
        message_id = message.id
        # Los datos vienen desempaquetados de `spoll`
        search, files, offset, total_results = spoll
        # El reply_msg ya existe (el mensaje de "Buscando...")

    # --- Manejo de Resultados ---
    settings = await get_settings(chat_id)

    # Si no hay resultados
    if not files or total_results == 0:
        # Intentar corrección ortográfica si está activada
        if settings.get("spell_check", True): # Activado por defecto
            return await advantage_spell_chok(client, name, msg, reply_msg, ai_search) # Pasamos `name` original
        else:
            no_results_text = f"❌ No encontré resultados para '<b>{search}</b>'."
            # Opcional: Mensaje de log si está activado
            if NO_RESULTS_MSG and LOG_CHANNEL:
                 try:
                      user_mention = message.from_user.mention if message.from_user else "Usuario Desconocido"
                      await client.send_message(LOG_CHANNEL, f"⚠️ Sin resultados para '{search}' solicitado por {user_mention} (ID: {user_id}) en chat {chat_id}.")
                 except Exception as log_err:
                      logger.error(f"Error enviando log de NO_RESULTS: {log_err}")
            return await reply_msg.edit_text(no_results_text, parse_mode=enums.ParseMode.HTML)

    # --- Si hay resultados, preparar respuesta ---
    # Prefijo para callbacks de archivo ('filep' o 'file')
    file_cb_prefix = 'filep' if settings.get('file_secure') else 'file'
    # Clave única para esta búsqueda (para paginación y 'Enviar Todo')
    key = f"{chat_id}-{message_id}"
    # Guardar búsqueda y archivos temporalmente
    FRESH[key] = search
    temp.GETALL[key] = files # Para 'Enviar Todo'
    # temp.SHORT[user_id] = chat_id # ¿Aún necesario? Revisar

    # Determinar si se usan botones o texto/enlaces
    show_buttons = settings.get('button', True) # Botones por defecto
    max_buttons_per_page = 10 if settings.get('max_btn', True) else MAX_B_TN # Usa MAX_B_TN de config

    btn = []

    # Botón Premium "Enviar Todo"
    btn.append([
        InlineKeyboardButton("✨ Enviar Todo (Premium)", callback_data=f"sendfiles#{key}")
    ])

    # Botones individuales (si aplica)
    if show_buttons:
        for file in files[:max_buttons_per_page]: # Limitar a la primera página
            file_name_display = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.get('file_name', 'archivo').split()))
            btn.append([
                InlineKeyboardButton(
                    text=f"[{get_size(file['file_size'])}] {file_name_display}",
                    callback_data=f'{file_cb_prefix}#{file["file_id"]}'
                )
            ])

    # Botones de Paginación (solo si hay más páginas)
    has_next = offset != 0 # offset aquí es el offset para la SIGUIENTE página

    if has_next:
        current_page = 1 # Siempre es la primera página aquí
        total_pages = math.ceil(total_results / max_buttons_per_page)
        pagination_row = [
             # Placeholder para Anterior (no aplica en la primera pág)
             InlineKeyboardButton(" ", callback_data="noop"),
             InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="noop"),
             InlineKeyboardButton("Siguiente ➡️", callback_data=f"next_{user_id}_{key}_{offset}")
        ]
        btn.append(pagination_row)
    # else: # Si solo hay una página, no añadir botones de paginación
    #     btn.append([InlineKeyboardButton(text="✅ Fin de Resultados", callback_data="noop")])

    # --- Generar Caption ---
    # Calcular tiempo de búsqueda
    end_time_utc = datetime.now(pytz.utc)
    time_difference = end_time_utc - start_time_utc
    search_time_seconds = f"{time_difference.total_seconds():.2f}"

    # Intentar obtener póster de IMDb si está activado
    imdb_data = None
    if settings.get("imdb", True): # Activado por defecto
        try:
             # Usar el nombre del primer archivo como pista si la búsqueda es ambigua
             imdb_data = await get_poster(search, file=(files[0])['file_name'])
        except Exception as e:
             logger.warning(f"Error obteniendo datos de IMDb para '{search}': {e}")

    final_caption = ""
    photo_to_send = None

    # Construir caption con plantilla IMDb si hay datos y póster
    if imdb_data and imdb_data.get('poster'):
        photo_to_send = imdb_data.get('poster')
        # Usar plantilla traducida de Script.py
        try:
             # Asegúrate que script.IMDB_TEMPLATE_TXT existe y está traducido
             # Pasar **locals() puede ser inseguro si hay variables inesperadas
             # Mejor pasar explícitamente lo necesario o usar un dict limpio
             template_data = {
                 'query': search, 'title': imdb_data.get('title', 'N/A'), 'votes': imdb_data.get('votes', 'N/A'),
                 'aka': imdb_data.get('aka', 'N/A'), 'seasons': imdb_data.get('seasons', 'N/A'),
                 'box_office': imdb_data.get('box_office', 'N/A'), 'localized_title': imdb_data.get('localized_title', 'N/A'),
                 'kind': imdb_data.get('kind', 'N/A'), 'imdb_id': imdb_data.get('imdb_id', 'N/A'),
                 'cast': ", ".join(imdb_data.get('cast', [])[:3]) + ('...' if len(imdb_data.get('cast', [])) > 3 else ''), # Limitar cast
                 'runtime': imdb_data.get('runtime', 'N/A'), 'countries': ", ".join(imdb_data.get('countries', [])),
                 'certificates': ", ".join(imdb_data.get('certificates', [])), 'languages': ", ".join(imdb_data.get('languages', [])),
                 'director': ", ".join(imdb_data.get('director', [])), 'writer': ", ".join(imdb_data.get('writer', [])),
                 'producer': ", ".join(imdb_data.get('producer', [])), 'composer': ", ".join(imdb_data.get('composer', [])),
                 'cinematographer': ", ".join(imdb_data.get('cinematographer', [])), 'music_team': ", ".join(imdb_data.get('music_team', [])),
                 'distributors': ", ".join(imdb_data.get('distributors', [])), 'release_date': imdb_data.get('release_date', 'N/A'),
                 'year': imdb_data.get('year', 'N/A'), 'genres': ", ".join(imdb_data.get('genres', [])),
                 'plot': imdb_data.get('plot', 'N/A')[:200] + ('...' if len(imdb_data.get('plot', 'N/A')) > 200 else ''), # Limitar plot
                 'rating': imdb_data.get('rating', 'N/A'), 'url': imdb_data.get('url', '#'),
                 'search_time': search_time_seconds,
                 'requester': message.from_user.mention if message.from_user else "N/A",
                 'total_results': total_results
             }
             final_caption = script.IMDB_TEMPLATE_TXT.format(**template_data)
        except Exception as template_err:
             logger.error(f"Error formateando plantilla IMDb: {template_err}")
             # Usar caption básico como fallback
             final_caption = f"Resultados para: <b>{search}</b> ({total_results} encontrados en {search_time_seconds}s)"

        # Si no se usan botones, añadir lista de archivos al caption IMDb
        if not show_buttons:
             final_caption += "\n\n<b>Archivos disponibles:</b>\n"
             is_premium_user = await db.has_premium_access(user_id)
             use_shortlink = SHORTLINK_ENABLED and not is_premium_user
             for file in files[:max_buttons_per_page]:
                 start_link_payload = f"{file_cb_prefix}_{file['file_id']}"
                 if use_shortlink and SHORTLINK_URL and SHORTLINK_API:
                      final_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f"https://t.me/{temp.U_NAME}?start={start_link_payload}")
                 else:
                      final_link = f"https://t.me/{temp.U_NAME}?start={start_link_payload}"
                 file_name_display = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.get('file_name', 'archivo').split()))
                 final_caption += f"📁 <a href='{final_link}'>[{get_size(file['file_size'])}] {file_name_display}</a>\n"

    else: # Sin IMDb o sin póster, usar caption de texto
        final_caption = f"Resultados para: <b>{search}</b>\n({total_results} encontrados en {search_time_seconds}s)\n"
        final_caption += f"Solicitado por: {message.from_user.mention if message.from_user else 'N/A'}\n"
        if message.chat.title: final_caption += f"Grupo: {message.chat.title}\n"
        final_caption += "\n"

        # Añadir lista de archivos si no se usan botones
        if not show_buttons:
            final_caption += "<b>Archivos disponibles:</b>\n"
            is_premium_user = await db.has_premium_access(user_id)
            use_shortlink = SHORTLINK_ENABLED and not is_premium_user
            for file in files[:max_buttons_per_page]:
                start_link_payload = f"{file_cb_prefix}_{file['file_id']}"
                if use_shortlink and SHORTLINK_URL and SHORTLINK_API:
                    final_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f"https://t.me/{temp.U_NAME}?start={start_link_payload}")
                else:
                    final_link = f"https://t.me/{temp.U_NAME}?start={start_link_payload}"
                file_name_display = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.get('file_name', 'archivo').split()))
                final_caption += f"📁 <a href='{final_link}'>[{get_size(file['file_size'])}] {file_name_display}</a>\n"

    # Añadir nota de auto-borrado si está activada
    auto_delete_enabled = settings.get('auto_delete', False)
    if auto_delete_enabled:
         final_caption += f"\n\n<i>ℹ️ Este mensaje se eliminará automáticamente en {AUTO_DELETE_SECONDS // 60} minutos.</i>"

    # --- Enviar la respuesta final ---
    reply_markup = InlineKeyboardMarkup(btn) if btn else None
    sent_message = None

    try:
        if photo_to_send:
             sent_message = await message.reply_photo(
                 photo=photo_to_send,
                 caption=final_caption,
                 reply_markup=reply_markup,
                 parse_mode=enums.ParseMode.HTML
            )
        else:
             sent_message = await reply_msg.edit_text( # Editar el mensaje "Buscando..."
                 text=final_caption,
                 reply_markup=reply_markup,
                 disable_web_page_preview=(not show_buttons), # Deshabilitar preview si hay enlaces en texto
                 parse_mode=enums.ParseMode.HTML
            )
        # Borrar "Buscando..." si se envió foto como nueva respuesta
        if photo_to_send:
            try: await reply_msg.delete()
            except: pass

    except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty) as img_err:
        logger.warning(f"Error de imagen al enviar resultado ({imdb_data.get('poster', 'N/A')}): {img_err}. Enviando como texto.")
        photo_to_send = imdb_data.get('poster', '').replace('.jpg', "._V1_UX360.jpg") # Intentar con tamaño menor
        try: # Reintentar con URL modificada o fallback a texto
            sent_message = await message.reply_photo(
                photo=photo_to_send, caption=final_caption, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML
            )
            if photo_to_send: await reply_msg.delete() # Borrar "Buscando..." si funcionó la foto
        except Exception: # Si falla de nuevo, enviar como texto
             sent_message = await reply_msg.edit_text(
                 text=final_caption, reply_markup=reply_markup, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML
            )
    except MessageNotModified:
        # Puede ocurrir si la búsqueda fue muy rápida y el texto es idéntico
        sent_message = reply_msg # El mensaje ya existe
    except Exception as e:
        logger.exception(f"Error grave al enviar resultado para '{search}': {e}")
        try: # Último intento de informar error
             await reply_msg.edit_text(f"❌ Ocurrió un error inesperado al mostrar los resultados para '{search}'.")
        except: pass # Si todo falla...

    # Programar auto-borrado si está activado y el mensaje se envió
    if auto_delete_enabled and sent_message:
        await asyncio.sleep(AUTO_DELETE_SECONDS) # Usar valor de config
        try:
             await sent_message.delete()
             # Opcional: borrar también el mensaje original del usuario
             if DELETE_USER_MESSAGE: await message.delete()
        except Exception as delete_err:
             logger.warning(f"No se pudo auto-borrar mensaje {sent_message.id} en chat {chat_id}: {delete_err}")


async def advantage_spell_chok(client, name, msg, reply_msg, vj_search):
    """Maneja la corrección ortográfica si la búsqueda inicial falla."""

    # `msg` puede ser `message` o `query` dependiendo de dónde se llame
    message = msg if isinstance(msg, pyrogram.types.Message) else msg.message
    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    # Usar ID del reply_msg (el que tiene los botones de sugerencia) para guardar/recuperar
    spell_check_msg_id = reply_msg.id

    # Intentar obtener sugerencias de IMDb
    try:
        # `name` es la búsqueda original que falló
        movies_data = await get_poster(name, bulk=True)
        if not movies_data:
            raise ValueError("IMDb no devolvió sugerencias")
    except Exception as e:
        logger.warning(f"Corrector ortográfico: No se obtuvieron sugerencias de IMDb para '{name}': {e}")
        req_url = f"https://www.google.com/search?q={quote_plus(name)}"
        google_btn = [[InlineKeyboardButton("🔎 Buscar en Google", url=req_url)]]
        await reply_msg.edit_text(
            text=f"❌ No encontré resultados para '<b>{name}</b>' y no pude obtener sugerencias.\n\nPuedes intentar buscar en Google:",
            reply_markup=InlineKeyboardMarkup(google_btn),
            parse_mode=enums.ParseMode.HTML
        )
        return # No hay más que hacer

    # Crear lista de sugerencias (título y título + año)
    suggestions = []
    suggestions += [movie.get('title') for movie in movies_data if movie.get('title')]
    suggestions += [f"{movie.get('title')} ({movie.get('year')})" for movie in movies_data if movie.get('title') and movie.get('year')]
    # Eliminar duplicados manteniendo el orden (aproximado)
    suggestions = list(dict.fromkeys(suggestions))
    # Limitar número de sugerencias
    suggestions = suggestions[:MAX_SPELL_SUGGESTIONS] # Usar valor de config

    if not suggestions:
        # Si IMDb devolvió datos pero sin títulos válidos
        await reply_msg.edit_text(f"❌ No encontré resultados para '<b>{name}</b>' y las sugerencias no fueron claras.", parse_mode=enums.ParseMode.HTML)
        return

    # Guardar sugerencias para el callback 'spol'
    SPELL_CHECK[spell_check_msg_id] = suggestions

    # Crear botones para las sugerencias
    btn = []
    for i, movie_name in enumerate(suggestions):
        btn.append([
            InlineKeyboardButton(text=movie_name.strip(), callback_data=f"spol#{user_id}#{i}")
        ])
    # Botón para cerrar
    btn.append([InlineKeyboardButton(text="✖️ Cerrar Sugerencias", callback_data=f'spol#{user_id}#close_spellcheck')])

    # Editar el mensaje "Buscando..." para mostrar las sugerencias
    settings = await get_settings(chat_id) # Necesario para auto-borrado
    spell_check_del = await reply_msg.edit_text(
        text=f"🤔 No encontré '<b>{name}</b>'.\n\n¿Quizás quisiste decir alguna de estas?",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

    # Programar auto-borrado del mensaje de sugerencias si está activado
    if settings.get('auto_delete', False): # Usar el mismo setting que los resultados
        await asyncio.sleep(AUTO_DELETE_SECONDS) # Mismo tiempo que resultados
        try:
            await spell_check_del.delete()
            # Limpiar del diccionario si se borra
            if spell_check_msg_id in SPELL_CHECK: del SPELL_CHECK[spell_check_msg_id]
        except Exception as delete_err:
            logger.warning(f"No se pudo auto-borrar mensaje de sugerencias {spell_check_msg_id}: {delete_err}")

# --- Filtros Manuales y Globales (Simplificado) ---
# (Requieren funciones find_filter, get_filters, find_gfilter, get_gfilters desde DB)

async def manual_filters(client, message, text=False):
    """Busca coincidencias con filtros manuales definidos para el grupo."""
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    query_text = text or message.text # Usar texto proporcionado o el del mensaje
    # ID del mensaje al que responder (el del usuario o el que se está respondiendo)
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id

    try:
        keywords = await get_filters(group_id) # Obtener filtros de la DB para este grupo
    except Exception as e:
        logger.error(f"Error obteniendo filtros manuales para grupo {group_id}: {e}")
        return False # No continuar si fallan los filtros

    if not keywords:
        return False # No hay filtros definidos para este grupo

    # Buscar coincidencias (sensible a mayúsculas/minúsculas según cómo se guardó el filtro)
    # Iterar en orden inverso de longitud para priorizar filtros más específicos
    for keyword in reversed(sorted(keywords, key=len)):
        # Usar word boundaries para evitar coincidencias parciales (ej: 'war' en 'award')
        pattern = r"(?i)\b" + re.escape(keyword) + r"\b" # (?i) para case-insensitive
        if re.search(pattern, query_text):
            # Coincidencia encontrada, obtener datos del filtro
            reply_text, btn_str, alert_str, fileid = await find_filter(group_id, keyword)

            # Limpiar texto de respuesta
            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            buttons = None
            if btn_str and btn_str != "[]":
                 try: buttons = InlineKeyboardMarkup(eval(btn_str))
                 except Exception as e: logger.error(f"Error evaluando botones para filtro '{keyword}' en {group_id}: {e}")

            # Enviar la respuesta del filtro
            sent_filter_msg = None
            try:
                if fileid and fileid != "None": # Si hay archivo adjunto
                     sent_filter_msg = await client.send_cached_media(
                         chat_id=group_id,
                         file_id=fileid,
                         caption=reply_text or "",
                         reply_markup=buttons,
                         protect_content=settings.get("file_secure", False),
                         reply_to_message_id=reply_id
                    )
                elif reply_text: # Si solo hay texto (y quizás botones)
                     sent_filter_msg = await client.send_message(
                         chat_id=group_id,
                         text=reply_text,
                         reply_markup=buttons,
                         disable_web_page_preview=True,
                         protect_content=settings.get("file_secure", False), # Proteger texto también?
                         reply_to_message_id=reply_id
                    )
                else:
                     # Filtro inválido (sin texto ni archivo)? Loggear?
                     logger.warning(f"Filtro manual '{keyword}' en {group_id} no tiene contenido para enviar.")
                     continue # Probar siguiente filtro

                # Programar auto-borrado si aplica
                if settings.get('auto_delete', False) and sent_filter_msg:
                     await asyncio.sleep(AUTO_DELETE_SECONDS)
                     try: await sent_filter_msg.delete()
                     except Exception: pass

                return True # Filtro manual aplicado, detener búsqueda

            except Exception as e:
                logger.exception(f"Error enviando respuesta de filtro manual '{keyword}' en {group_id}: {e}")
                # Podría intentar el siguiente filtro o detenerse
                return False # Detener si falla el envío

    return False # No se encontró ninguna coincidencia de filtro manual


# async def global_filters(client, message, text=False):
#     """Busca coincidencias con filtros globales (si está implementado y activado)."""
#     # Similar a manual_filters pero usando get_gfilters y find_gfilter
#     # ... (código similar, adaptando llamadas a DB)
#     # Decidir si los filtros globales se aplican antes o después de los manuales
#     # Decidir si un filtro global detiene la búsqueda automática
#     pass # Implementar si es necesario
