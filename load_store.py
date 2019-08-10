import requests
import os
import pathlib


def load_n_store(links, image_name, folder):
    """
    :links should be a list of http links
    Load files that came in the list of :links
    with name's boilerplate :image_name
    into the folder that was passed in the :folder parameter
    """
    if len(links) < 1:
        return None
    list_of_files = []
    for image_enum, link in enumerate(links):
        img_name = f'{image_name}{image_enum}{pathlib.Path(link).suffix}'
        img_content = download_img(link)
        if img_content is None:
            list_of_files.append('None')
        save_img(img_name, img_content, folder)
        list_of_files.append(img_name)
    return list_of_files


def save_img(img_name, img_content, folder):
    cur_dir = os.path.dirname(__file__)
    image_path = os.path.join(cur_dir, folder)
    pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(image_path, img_name), 'wb') as q:
        q.write(img_content)


def download_img(link):
    resp = requests.get(link)
    if not resp.ok:
        return None
    return resp.content


if __name__ == '__main__':
    load_n_store([], '', '')
