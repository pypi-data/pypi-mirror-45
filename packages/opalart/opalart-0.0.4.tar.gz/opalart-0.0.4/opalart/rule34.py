from opalart.client import GalleryClient


def rule34():
    """
    Returns an GalleryClient instance with Rule 34 data.
    :return:
    :rtype: opalart.GalleryClient
    """
    client_data = {
        'as_json': False,
        'client_name': 'Rule 34',
        'client_url': 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags='
    }
    return GalleryClient(client_data)
