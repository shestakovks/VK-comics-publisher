import json
import os
import random

import requests
from dotenv import load_dotenv


def get_filename_from_url(url):
    return url.split('/')[-1]


def load_posted(filename=None):
    if filename is None:
        filename = 'posted.json'
    if not os.path.isfile(filename):
        return {}
    with open(filename) as f:
        return json.load(f)


def save_posted(posted, filename=None):
    if filename is None:
        filename = 'posted.json'
    with open(filename, 'w') as f:
        json.dump(posted, f, indent=2)


def download_photo(url, path_to_file):
    response = requests.get(url)
    response.raise_for_status()
    with open(path_to_file, 'wb') as f:
        f.write(response.content)


def get_max_comics_num():
    url = 'https://xkcd.com/info.0.json'
    last_comics = requests.get(url)
    last_comics.raise_for_status()
    return last_comics.json()['num']


def get_comics(comics_number):
    comics_url = f'https://xkcd.com/{comics_number}/info.0.json'
    comics = requests.get(comics_url)
    comics.raise_for_status()

    comics_pic_url = comics.json()['img']
    filename = get_filename_from_url(comics_pic_url)
    download_photo(comics_pic_url, filename)

    comics_comment = comics.json()['alt']
    return filename, comics_comment


def get_random_comics():
    """Generates random comics number and downloads it to working dir

    Returns:
        (filename, comment) -- filename of downloaded comics picture
        and witty author's comment about it

    Raises:
        requests.exceptions.HTTPError if anything went wrong
    """
    max_comics_number = get_max_comics_num()
    is_posted = True
    while is_posted:
        comics_number = random.randint(1, max_comics_number)
        is_posted = str(comics_number) in posted
    posted[comics_number] = True
    return get_comics(comics_number)


def get_wall_upload_url(url, params):
    response = requests.get(url.format('photos.getWallUploadServer'),
                            params=params).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response['response']['upload_url']


def upload_pic_to_server(url, filename):
    with open(filename, 'rb') as pic:
        files = {
            'photo': pic,
        }
        response = requests.post(url, files=files).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response


def save_wall_photo(url, params):
    response = requests.post(url.format('photos.saveWallPhoto'),
                             data=params).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response


def post_to_wall(url, base_params, post_params, comment):
    media_owner_id = post_params['response'][0]['owner_id']
    media_id = post_params['response'][0]['id']
    params = {
        'access_token': base_params['access_token'],
        'v': base_params['v'],
        'owner_id': f'-{base_params["group_id"]}',
        'from_group': 1,
        'attachments': f'photo{media_owner_id}_{media_id}',
        'message': comment,
    }
    response = requests.post(url.format('wall.post'), data=params).json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])


def post_comics_to_vk_group(filename, comment, vk_token,
                            vk_api_version, vk_group_id):
    """Post given picture and comment to given VK group wall

    Arguments:
        filename {str} -- path to file with picture
        comment {str} -- message to add to posted picture
        vk_token {str} -- your VK token
        vk_api_version {str} -- VK API version you'd like to use
        vk_group_id {str} -- your VK group id

    Raises:
        requests.exceptions.HTTPError if anything went wrong
    """
    vk_url = 'https://api.vk.com/method/{}'
    base_params = {
        'access_token': vk_token,
        'v': vk_api_version,
        'group_id': vk_group_id,
    }
    upload_url = get_wall_upload_url(vk_url, base_params)
    upload_params = upload_pic_to_server(upload_url, filename)
    save_params = {**base_params, **upload_params}
    post_params = save_wall_photo(vk_url, save_params)
    post_to_wall(vk_url, base_params, post_params, comment)


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_api_version = os.getenv('VK_API_VERSION')
    vk_group_id = os.getenv('VK_GROUP_ID')
    posted = load_posted()

    try:
        filename, comment = get_random_comics()
        post_comics_to_vk_group(filename, comment, vk_token,
                                vk_api_version, vk_group_id)
        save_posted(posted)
        os.remove(filename)
        print(f'Comics: "{filename}" was successfully posted.')
    except requests.exceptions.HTTPError as e:
        print(f'Something went wrong :(\nHere is your error: "{e}"')
