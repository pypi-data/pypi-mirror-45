from opalart.client import GalleryClient


def yandere():
    """
    Returns an GalleryClient instance with Yande.re data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'Yande.re',
        'client_url': 'https://yande.re/post.json?limit=1000&tags='
    }
    return GalleryClient(client_data)
