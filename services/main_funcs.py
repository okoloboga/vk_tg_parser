import pandas as pd
import os
import json

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient

from services.parsing import check_wall_tg, file_writer_tg, check_wall_vk, file_writer_vk


def main_parsing(phone):
    with open('database/database.json', encoding='utf-8') as database_json:
        database = json.load(database_json)

    """TELEGRAM"""
    api_id = 23264414
    api_hash = 'da3808010cb0370a88e770adb5338c9e'
    phone = phone
    print('TG PHONE:', phone)

    client = TelegramClient(phone, api_id, api_hash)
    client.start()
    print('TG CLIENT START')

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
            if chat.title in database['tg_channels']:
                groups.append(chat)
        except:
            print('NO CHAT IN DATABASE')
            continue

    for group in groups:
        total_groups[group.title] = check_wall_tg(group, client)
    print('TG CHANNELS ADDED')
    try:
        os.remove('tg_channels.csv')
        os.remove('tg_channels.xlsx')
    except FileNotFoundError:
        print('NO VK/TG FILES')
    file_writer_tg(total_groups, database['keywords'])

    print('TG COMPLETE')

    """VK"""
    total_data = {}

    for public_domain in database['vk_publics']:
        total_data[public_domain] = check_wall_vk(public_domain)
    print('VK PUBLICS ADDED')
    try:
        os.remove('vk_publics.csv')
        os.remove('vk_publics.xlsx')
    except FileNotFoundError:
        print('NO VK/TG FILES')
    file_writer_vk(total_data, database['keywords'])

    print('VK COMPLETE')

    vk_result = pd.read_csv("vk_publics.csv", encoding='utf8')
    tg_result = pd.read_csv("tg_channels.csv", encoding='utf8')
    vk_result.to_excel('vk_publics.xlsx', index=False, header=True)
    tg_result.to_excel('tg_channels.xlsx', index=False, header=True)

    print('WRITE COMPLETE')