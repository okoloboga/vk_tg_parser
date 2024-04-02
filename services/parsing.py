import time
import csv
import requests
from telethon.tl.functions.messages import GetHistoryRequest

"""TELEGRAM"""


def check_wall_tg(group, client_tg):
    limit = 100
    total_count_limit = 100
    all_messages = []
    offset_id = 0
    total_messages = 0
    try:
        all_messages.append(group.username)
        while True:
            history = client_tg(GetHistoryRequest(
                peer=group,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
                total_messages += 1
            offset_id = messages[len(messages) - 1].id
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        return all_messages
    except AttributeError:
        print('NO USERNAME: ', group)


def file_writer_tg(data, keywords, antiwords):
    with (open('tg_channels.csv', 'w', encoding='UTF-8') as file):
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        writer.writerow(('Соцсеть', 'Паблик', 'username Канала', 'ID канала', 'ID сообщения',
                         'ID пользователя', 'Текст поста', 'Дата публикации'))
        for group, posts in data.items():
            try:
                for post in posts:
                    if post is not None and 'message' in post:
                        if any(word in post['message'] for word in keywords) and (int(time.time())-5300000 < post['date'].timestamp()):
                            if any(antiword in post['message'] for antiword in antiwords):
                                continue
                            else:
                                writer.writerow(('TG ', group,
                                                 posts[0] if posts[0] is not None else 'нет username',
                                                 post['peer_id']['channel_id'],
                                                 post['id'],
                                                 post['from_id']['user_id'] if ('from_id' in post and 'user_id' in post['from_id']) else 'нет ID отправителя',
                                                 post['message'], post['date']))
            except TypeError:
                print('POST IS NONE TYPE')


"""VK"""


def check_wall_vk(domain):
    count = 100
    offset = 0
    all_posts = []
    token = '735bf6a6735bf6a6735bf6a6be704c6dc47735b735bf6a616ad7155515806ec7853c8b1'
    version = 5.199

    group_info = requests.get('https://api.vk.com/method/groups.getById',
                              params={
                                  'access_token': token,
                                  'v': version,
                                  'group_id': domain
                              })

    name = group_info.json()['response']['groups'][0]['name']
    all_posts.append(str(name))
    while offset < 100:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                }
                                )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
        time.sleep(.5)
    return all_posts


def file_writer_vk(data, keywords, antiwords):
    with (open('vk_publics.csv', 'w', encoding="utf-8") as file):
        a_pen = csv.writer(file)
        a_pen.writerow(
            ('Соцсеть', 'ID Паблика', 'Название паблика', 'Ссылка', 'ID Автора', 'Текст поста', 'Дата публикации'))
        for domain, posts in data.items():
            for post in posts:
                if type(post) != str:
                    if any(word in post['text'] for word in keywords) and (int(time.time())-5300000 < post['date']):
                        if any(antiword in post['text'] for antiword in antiwords):
                            continue
                        else:
                            a_pen.writerow(('VK', domain, posts[0],
                                            f"https://vk.com/{domain}?w=wall{post['owner_id']}_{post['id']}",
                                            post['from_id'], post['text'],
                                            time.ctime(post['date'])))


