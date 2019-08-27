from dotenv import load_dotenv
from os import getenv
import requests
import argparse
import load_store as ls
import random
import pathlib


def get_args():
    parser = argparse.ArgumentParser(description='Downloading comics from xkcd.com')
    parser.add_argument('--img_name', default='comic', help='Define image name default=python')
    parser.add_argument('--img_id', help='Define image id if empty then random')
    parser.add_argument('--img_dir', default='images', help='Define image folder default=images')
    arguments = parser.parse_args()
    return arguments


def get_comic(xkcd_img_name, xkcd_img_id, xkcd_dir):
    """
    Function downloads comic picture given by API of xkcd.com-site
    :return: dictionary with downloaded file.
    comment for comic and folder where picture was stored
    """
    xkcd_api = 'https://xkcd.com/'
    headers = {
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    }
    if xkcd_img_id is None:
        url = f'{xkcd_api}info.0.json'
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        comic = resp.json()
        xkcd_img_id = random.randint(0, comic['num'])
    url = f'{xkcd_api}{xkcd_img_id}/info.0.json'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    comic = resp.json()

    img_links = [comic.get('img')] if comic.get('img') is not None else []
    alt = comic.get('alt')
    written_files = ls.load_n_store(
        img_links,
        f'{xkcd_img_name}_{xkcd_img_id}',
        xkcd_dir
    )[0]
    return {'file': written_files, 'comments': alt, 'dir': xkcd_dir}


def call_vk_api(vk_method, vk_url, vk_params, vk_files):
    if vk_method == 'get':
        vk_resp = requests.get(vk_url, params=vk_params)
    elif vk_method == 'post':
        vk_resp = requests.post(vk_url, files=vk_files)
    vk_resp.raise_for_status()
    json_resp = vk_resp.json()
    if 'error' in json_resp:
        raise requests.exceptions.HTTPError(json_resp['error'])
    return json_resp


def post_pic_onto_vk_wall(comics_file, vk_access_token, vk_user_id):
    cur_dir = pathlib.PurePath(__file__).parent
    img_path = cur_dir.joinpath(comics_file['dir'], comics_file['file'])
    base_params = {'access_token': vk_access_token, 'v': '5.101'}
    params = base_params.copy()
    params.update({'user_id': vk_user_id, 'extended': 1})
    url = 'https://api.vk.com/method/groups.get'
    vk_reponse = call_vk_api('get', url, params, None)['response']

    group_id = vk_reponse['items'][0]['id']
    params = base_params.copy()
    params.update({'group_id': group_id})
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_reponse = call_vk_api('get', url, params, None)['response']

    upload_url = vk_reponse['upload_url']
    with open(img_path, 'rb') as file:
        files = {'photo': file}
        vk_reponse = call_vk_api('post', upload_url, None, files)
    params = base_params.copy()
    params.update({'server': vk_reponse['server'],
                   'photo': vk_reponse['photo'],
                   'hash': vk_reponse['hash'],
                   'user_id': vk_user_id,
                   'caption': 'Random comics',
                   'group_id': group_id
                   })
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    vk_reponse = call_vk_api('get', url, params, None)['response'][0]

    vk_media_id = vk_reponse['id']
    vk_owner_id = vk_reponse['owner_id']
    params = base_params.copy()
    params.update({'message': comic_file['comments'],
                   'owner_id': f'-{group_id}',
                   'from_group': '1',
                   'attachments': f'photo{vk_owner_id}_{vk_media_id}'
                   })
    url = 'https://api.vk.com/method/wall.post'
    vk_reponse = call_vk_api('get', url, params, None)
    del_path = pathlib.Path(img_path)
    del_path.unlink()
    return vk_reponse


if __name__ == '__main__':
    load_dotenv()
    access_token = getenv('VK_ACCESS_TOKEN')
    user_id = getenv('VK_ID')
    args = get_args()
    img_id = args.img_id
    img_folder = args.img_dir
    img_name = args.img_name
    comic_file = get_comic(img_name, img_id, img_folder)
    vk_post = post_pic_onto_vk_wall(
        comic_file,
        access_token,
        user_id
    )
    print(vk_post)
