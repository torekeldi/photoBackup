import requests
import json


def get_photo_count():
    count_input = input('Введите количество фотографий, которые нужно сохранить на Яндекс Диске')
    if not count_input:
        count_input = '5'
    else:
        while not count_input.isdigit():
            count_input = input('Введите только числовое значение и ничего кроме')
    return int(count_input)


def get_photo_owner():
    owner_input = input('Введите id владельца фотографий, из социальной сети ВК')
    while not owner_input.isdigit():
        owner_input = input('Обязательно нужно ввести данные и только числовое значение')
    return int(owner_input)


def get_photo_info(photo_owner, photo_count, vk_access_token):
    req_url = 'https://api.vk.com/method/photos.get?'
    get_params = {
        'owner_id': photo_owner,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
        'count': photo_count,
        'access_token': vk_access_token,
        'v': 5.199
    }
    vk_response = requests.get(url=req_url, params=get_params)
    load_data = vk_response.json()
    photo_info_dict = {}
    for idx, i in enumerate(load_data['response']['items']):
        photo_id = str(i['id'])
        photo_likes = str(i['likes']['count'])
        max_photo = max(i['sizes'], key=lambda x: x['height'] * x['width'])
        if idx == 0:
            photo_info_dict[photo_likes] = {'size': max_photo['type'], 'url': max_photo['url']}
        else:
            if photo_info_dict.get(photo_likes):
                photo_info_dict[photo_likes+'_'+photo_id] = {'size': max_photo['type'], 'url': max_photo['url']}
            else:
                photo_info_dict[photo_likes] = {'size': max_photo['type'], 'url': max_photo['url']}
    return photo_info_dict


def write_json(some_data):
    data_list = []
    for k, v in some_data.items():
        data_list.append({'file_name': k+'.jpg', 'size': v['size']})
    with open('photo_info.json', 'w') as f:
        json.dump(data_list, f)


def yd_disk_folder_create(yd_access_token):
    yd_disk_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=/vk_profile_photo'
    yd_disk_headers = {'content-type': 'application/json', 'Authorization': yd_access_token}
    requests.put(url=yd_disk_url, headers=yd_disk_headers)


def yd_disk_upload_photo(yd_access_token, photo_info):
    photo_count = len(photo_info)
    yd_disk_headers = {'content-type': 'application/json', 'Authorization': yd_access_token}
    for idx, (k, v) in enumerate(photo_info.items()):
        yd_disk_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        yd_disk_params = {
            'path': f'vk_profile_photo/{k}.jpg',
            'url': v['url']
        }
        if f'{k}.jpg' in exist_photo_list(yd_access_token):
            print(f'Фото с названием {k}.jpg уже есть в папке vk_profile_photo на Яндекс Диске, '
                  f'обработано {idx+1} фото из {photo_count}')
        else:
            r = requests.post(yd_disk_url, params=yd_disk_params, headers=yd_disk_headers)
            if str(r.status_code)[0] == '2':
                print(f'Фото с названием {k}.jpg загрузился в папку vk_profile_photo на Яндекс Диске, '
                      f'обработано {idx+1} фото из {photo_count}')
            else:
                print(f'Что-то пошло не так, статус ответа {r.status_code}')


def exist_photo_list(yd_access_token):
    photo_list = []
    yd_disk_headers = {'content-type': 'application/json', 'Authorization': yd_access_token}
    yd_disk_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    yd_disk_params = {'path': 'vk_profile_photo'}
    r = requests.get(url=yd_disk_url, params=yd_disk_params, headers=yd_disk_headers)
    data = r.json()
    for i in data['_embedded']['items']:
        photo_list.append(i['name'])
    return photo_list
