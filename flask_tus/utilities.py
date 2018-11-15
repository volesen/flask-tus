import base64


def get_extension(filename, depth=1):
    return '.'.join(filename.split('.')[1:])


def extract_metadata(upload_metadata):
    metadata = {}
    for kv in upload_metadata.split(','):
        key, value = kv.split(' ')
        metadata[key] = base64.b64decode(value).decode('ascii')

    return metadata
