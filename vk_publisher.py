from dotenv import load_dotenv
import os
import requests
import argparse
import load_store as ls



def get_args():
    parser = argparse.ArgumentParser(description='Downloading comics from xkcd.com')
    parser.add_argument('--img_name', default='python',  help='Define image name default=python')
    parser.add_argument('--img_id', default='353',  help='Define image id default=353')
    parser.add_argument('--api', default='https://xkcd.com/', help=argparse.SUPPRESS)
    parser.add_argument('--headers', default={
        'User-Agent': 'curl',
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'Keep-Alive'
    }, help=argparse.SUPPRESS)
    parser.add_argument('--img_dir', default='images',  help='Define image folder default=images')
    args = parser.parse_args()
    args.api = f'{args.api}{args.img_id}/info.0.json'
    return args

def get_comic():
    """
    Function downloads json files with comic
    :return:
    """
    args = get_args()
    resp = requests.get(args.api, headers=args.headers)
    if not resp.ok:
        raise requests.exceptions.HTTPError(resp['error'])
    comic = resp.json()
    img_links = [comic.get('img')]
    alt = comic.get('alt')
    written_files = ls.load_n_store(img_links, args.img_name, args.img_dir)
    print(alt)


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


def vk_post_pic_onto_wall ():
    extended = 1
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, 'images') # из аргументов
    pics = os.listdir(image_path)
    if len(pics) == 0:
        quit()
    pic_full_path = os.path.join(image_path, pics[0])
    version = '5.101'
    method = ['groups.get', 'photos.getWallUploadServer', 'photos.saveWallPhoto', 'wall.post']
    params = {'user_id': vk_user_id, 'extended': extended, 'access_token': vk_access_token, 'v': version}
    url = f'https://api.vk.com/method/{method[0]}'
    vk_reponse = vk_request('get', url, params, None).get('response')

    group_id = vk_reponse.get('items')[0].get('id')
    url = f'https://api.vk.com/method/{method[1]}'
    params.update({'group_id':group_id})
    del params['extended'], params['user_id']
    vk_reponse = vk_request('get', url, params, None).get('response')

    upload_url = vk_reponse.get('upload_url')
    with open(pic_full_path, 'rb') as file:
        files = {'photo': file}
        vk_reponse = vk_request('post', upload_url, None, files)

    params.update({'server': vk_reponse.get('server')})
    params.update({'photo': vk_reponse.get('photo')})
    params.update({'hash': vk_reponse.get('hash')})
    params.update({'user_id': vk_user_id})
    params.update({'caption': 'Python comics'})
    url = f'https://api.vk.com/method/{method[2]}' # SaveWallPhoto
    vk_reponse = vk_request('get', url, params, None).get('response')[0]

    vk_media_id = vk_reponse.get('id')
    vk_owner_id = vk_reponse.get('owner_id')
    params.update({'message': 'Look at this Python comics!!!2222'})
    params.update({'owner_id': f'-{group_id}'})
    params.update({'from_group': '1'})
    params.update({'attachments': f'photo{vk_owner_id}_{vk_media_id}'})
    del params['server'], params['photo'], params['hash'], params['caption'], params['user_id'], params['group_id']
    url = f'https://api.vk.com/method/{method[3]}'
    vk_reponse = vk_request('get', url, params, None)
    print(vk_reponse)


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_user_id = os.getenv('VK_ID')
    # vk_app_id = os.getenv('VK_APP_ID')
    # get_comic()
    vk_post_pic_onto_wall()
