import filecmp
import os

import pytest

CHUNK_SIZE = 1024


def read_chunks(file, chunk_size):
    return iter(lambda: file.read(chunk_size), b'')


@pytest.mark.usefixtures('class_client')
class TestUpload(object):
    def test_chunked_upload(self):
        with open('data/flask.png', 'rb') as file:
            file_length = len(file.read())
            file.seek(0)  # Set file pos to 0 after reading

            # Get upload endpoint
            post_response = self.client.post('/files/', headers={
                'Tus-Version': '1.0.0',
                'Upload-Length': file_length
            })
            resource_url = post_response.headers['Location']

            offset = 0
            for chunk in read_chunks(file, CHUNK_SIZE):
                # Upload chunk
                patch_response = self.client.patch(resource_url, data=chunk, headers={
                    'Tus-Version': '1.0.0',
                    'Content-Type': 'application/offset+octet-stream',
                    'Content-Length': len(chunk),
                    'Upload-Offset': offset,
                })
                offset += len(chunk)
                assert patch_response.status_code == 204  # Successful upload
                assert offset == int(patch_response.headers.get('Upload-Offset'))  # Does offsets match

            # Compare test file and uploaded file
            resource_id = resource_url.split('/')[-1]
            uploaded_file = os.path.join(self.app.config['TUS_UPLOAD_DIR'], resource_id)  # Get path of uploaded file

            assert filecmp.cmp('data/flask.png', uploaded_file)
