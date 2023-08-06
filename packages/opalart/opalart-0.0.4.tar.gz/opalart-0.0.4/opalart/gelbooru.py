from opalart.client import GalleryClient


def gelbooru():
    """
    Returns an GalleryClient instance with Gelbooru data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': False,
        'client_name': 'Gelbooru',
        'client_url': 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='
    }
    return GalleryClient(client_data)
