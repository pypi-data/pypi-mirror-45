from opalart.client import GalleryClient


def e621():
    """
    Returns an GalleryClient instance with E621 data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': True,
        'client_name': 'E621',
        'client_url': 'https://e621.net/post/index.json?tags=',
        'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    }
    return GalleryClient(client_data)
