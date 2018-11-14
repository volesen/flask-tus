import base64


def handle_metadata(upload_metadata):
    metadata = {}
    for kv in upload_metadata.split(','):
        key, value = kv.split(' ')
        metadata[key] = base64.b64decode(value).encode('ascii')
    return metadata
