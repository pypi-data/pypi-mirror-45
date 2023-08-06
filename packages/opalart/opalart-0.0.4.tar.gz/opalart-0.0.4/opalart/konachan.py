from opalart.client import GalleryClient


def konachan():
    """
    Returns an GalleryClient instance with Konachan data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'Konachan',
        'client_url': 'https://konachan.com/post.json?limit=1000&tags='
    }
    return GalleryClient(client_data)
