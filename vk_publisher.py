from dotenv import load_dotenv
from os import getenv
import requests
import argparse
import load_store as ls
import random
import pathlib


def get_args():
    parser = argparse.ArgumentParser(description='Downloading comics from xkcd.com')
    parser.add_argument('--img_name', default='python',  help='Define image name default=python')
    parser.add_argument('--img_id',   help='Define image id if empty then random')
    parser.add_argument('--api', default='https://xkcd.com/', help=argparse.SUPPRESS)
    parser.add_argument('--headers', default={
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    }, help=argparse.SUPPRESS)
    parser.add_argument('--img_dir', default='images',  help='Define image folder default=images')
    args = parser.parse_args()
    return args


def get_comic():
    """
    Function downloads json files with comic
    :return:
    """
    args = get_args()
    if args.img_id is None:
        url = f'{args.api}info.0.json'
        resp = requests.get(url,  headers=args.headers)
        if not resp.ok:
            raise requests.exceptions.HTTPError(resp['error'])
        comic = resp.json()
        img_id = random.choice(range(comic.get('num')))
    else:
        img_id = args.img_id
    url = f'{args.api}{img_id}/info.0.json'
    resp = requests.get(url, headers=args.headers)
    if not resp.ok:
        raise requests.exceptions.HTTPError(resp['error'])
    comic = resp.json()

    img_links = [comic.get('img')]
    alt = comic.get('alt')
    written_files = ls.load_n_store(img_links, f'{args.img_name}_{img_id}', args.img_dir)[0]
    return {'file': written_files, 'comments': alt, 'dir': args.img_dir}


def vk_request(method, url, params, files):
    if method == 'get':
        resp = requests.get(url, params=params)
    elif method == 'post':
        resp = requests.post(url, files=files)
    resp.raise_for_status()
    json_resp = resp.json()
    if 'error' in json_resp:
        raise requests.exceptions.HTTPError(json_resp['error'])
    return json_resp


def vk_post_pic_onto_wall(comic_file):
    extended = 1
    cur_dir = pathlib.PurePath(__file__).parent
    img_path = cur_dir.joinpath(comic_file['dir'], comic_file['file'])
    version = '5.101'
    method = ['groups.get', 'photos.getWallUploadServer', 'photos.saveWallPhoto', 'wall.post']
    params = {'user_id': vk_user_id, 'extended': extended, 'access_token': vk_access_token, 'v': version}
    url = f'https://api.vk.com/method/{method[0]}'
    vk_reponse = vk_request('get', url, params, None).get('response')

    group_id = vk_reponse.get('items')[0].get('id')
    url = f'https://api.vk.com/method/{method[1]}'
    params.update({'group_id': group_id})
    del params['extended'], params['user_id']
    vk_reponse = vk_request('get', url, params, None).get('response')

    upload_url = vk_reponse.get('upload_url')
    with open(img_path, 'rb') as file:
        files = {'photo': file}
        vk_reponse = vk_request('post', upload_url, None, files)

    params.update({'server': vk_reponse.get('server')})
    params.update({'photo': vk_reponse.get('photo')})
    params.update({'hash': vk_reponse.get('hash')})
    params.update({'user_id': vk_user_id})
    params.update({'caption': 'Random comics'})
    url = f'https://api.vk.com/method/{method[2]}'
    vk_reponse = vk_request('get', url, params, None).get('response')[0]

    vk_media_id = vk_reponse.get('id')
    vk_owner_id = vk_reponse.get('owner_id')
    params.update({'message': comic_file['comments']})
    params.update({'owner_id': f'-{group_id}'})
    params.update({'from_group': '1'})
    params.update({'attachments': f'photo{vk_owner_id}_{vk_media_id}'})
    del params['server'], params['photo'], params['hash'], params['caption'], params['user_id'], params['group_id']
    url = f'https://api.vk.com/method/{method[3]}'
    vk_reponse = vk_request('get', url, params, None)
    del_path = pathlib.Path(img_path)
    del_path.unlink()
    print(vk_reponse)


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = getenv('VK_ACCESS_TOKEN')
    vk_user_id = getenv('VK_ID')
    comic_file = get_comic()
    vk_post_pic_onto_wall(comic_file)
