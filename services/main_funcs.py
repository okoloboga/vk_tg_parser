from json import load
import logging
from os import remove

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient

from services.parsing import check_wall_tg, file_writer_tg, check_wall_vk, file_writer_vk


def main_parsing(api_id, api_hash, phone):

    # Инициализация логгера
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Main parsing START')

    with open('database/database.json', encoding='utf-8') as database_json:
        database = load(database_json)

    """TELEGRAM"""
    api_id = api_id
    api_hash = api_hash
    phone = phone

    client = TelegramClient(phone, api_id, api_hash)
    client.start()

    logging.info('TG client START')

    chats = []
    last_date = None
    size_chats = 200
    groups = []
    total_groups = {}

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=size_chats,
        hash = 0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.username in database['tg_channels']:
                groups.append(chat)
        except:
            continue

    for group in groups:
        total_groups[group.title] = check_wall_tg(group, client)
    logging.info('TG channels added')
    try:
        remove('tg_channels.csv')
        logging.info('CSV TG removed')
    except FileNotFoundError:
        logging.info('No TG files')
    file_writer_tg(total_groups, database['keywords'], database['antiwords'])

    groups.clear()
    total_groups.clear()
    chats.clear()
    client.disconnect()

    logging.info('TG complete')


    """VK"""

    total_data = {}

    for public_domain in database['vk_publics']:
        total_data[public_domain] = check_wall_vk(public_domain)
    logging.info('VK publicks added')
    try:
        remove('vk_publics.csv')
        logging.info('CSV VK removed')
    except FileNotFoundError:
        logging.info('No VK files')
    file_writer_vk(total_data, database['keywords'], database['antiwords'])

    database.clear()
    total_data.clear()

    logging.info('VK complete')
    logging.info('Main parsing COMPLETE')
