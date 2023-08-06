from opalart.client import GalleryClient


def xbooru():
    """
    Returns an GalleryClient instance with Xbooru data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': False,
        'client_name': 'Xbooru',
        'client_url': 'http://xbooru.com/index.php?page=dapi&s=post&q=index&tags='
    }
    return GalleryClient(client_data)
