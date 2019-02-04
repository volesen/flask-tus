import base64


def get_extension(filename, depth=1):
    return '.'.join(filename.split('.')[depth:])


def read_chunks(file, chunk_size=1024):
    return iter(lambda: file.read(chunk_size), b'')


def extract_metadata(upload_metadata):
    metadata = {}
    for kv in upload_metadata.split(','):
        key, value = kv.split(' ')
        metadata[key] = base64.b64decode(value).decode('ascii')

    return metadata


def extract_checksum(upload_checksum):
    # The Upload-Checksum request header consist of the name of the used checksum algorithm and the Base64 encoded
    # checksum separated by a space.
    algorithm, value = upload_checksum.split(' ')
    checksum = base64.b64decode(value).decode('ascii')
    return algorithm, checksum


def format_date(date):
    # The value of the Upload-Expires header MUST be in RFC 7231 datetime format.
    # Link: https://tools.ietf.org/html/rfc7231#section-7.1.1.1
    return date.strftime('%a, %d %b %Y %H:%M:%S GMT')
