import requests
import pathlib


def load_n_store(links, image_name, folder):
    """
    :links should be a list of http links
    Load files that came in the list of :links
    with name's boilerplate :image_name
    into the folder that was passed in the :folder parameter
    """
    list_of_files = []
    for image_enum, link in enumerate(links):
        img_name = f'{image_name}{image_enum}{pathlib.Path(link).suffix}'
        img_content = download_img(link)
        save_img(img_name, img_content, folder)
        list_of_files.append(img_name)
    return list_of_files


def save_img(img_name, img_content, folder):
    cur_dir = pathlib.PurePath(__file__).parent
    image_path = cur_dir.joinpath(cur_dir, folder)
    pathlib.Path(image_path).mkdir(parents=True, exist_ok=True)
    with open(image_path.joinpath(image_path, img_name), 'wb') as q:
        q.write(img_content)


def download_img(link):
    resp = requests.get(link)
    resp.raise_for_status()
    return resp.content


if __name__ == '__main__':
    urls = ['https://imgs.xkcd.com/comics/woodpecker.png']
    pic_name = 'comic_pict'
    dir_name = 'pict'
    load_n_store(urls, pic_name, dir_name)
