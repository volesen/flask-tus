import base64
import pytest
import filecmp
import hashlib

CHUNK_SIZE = 1024
TEST_FILE = 'tests/data/flask.png'
SUPPORTED_ALGORITHMS = {'md5', 'sha1'}


@pytest.mark.usefixtures('class_client')
class TestChecksumExtension(object):

    @staticmethod
    def __read_chunks(file, chunk_size):
        return iter(lambda: file.read(chunk_size), b'')

    @staticmethod
    def __create_checksum(algorithm, chunk):
        m = hashlib.new(algorithm)
        m.update(chunk)

        return m.hexdigest()

    def __create_checksum_header(self, algorithm, chunk):
        checksum = self.__create_checksum(algorithm, chunk)
        return '{} {}'.format(algorithm, base64.b64encode(checksum.encode('ascii')).decode('ascii'))

    def test_checksum_upload(self):
        for algorithm in SUPPORTED_ALGORITHMS:
            with open(TEST_FILE, 'rb') as file:
                file_length = len(file.read())

                # Set file pos to 0 after reading
                file.seek(0)

                # Create initial upload (first upload)
                post_response = self.client.post('/files/', headers={
                    'Tus-Version': '1.0.0',
                    'Upload-Length': file_length
                })
                resource_url = post_response.headers['Location']

                # Upload chunks
                offset = 0
                for chunk in self.__read_chunks(file, CHUNK_SIZE):
                    patch_response = self.client.patch(resource_url, data=chunk, headers={
                        'Tus-Version': '1.0.0',
                        'Content-Type': 'application/offset+octet-stream',
                        'Content-Length': len(chunk),
                        'Upload-Offset': offset,
                        'Upload-Checksum': self.__create_checksum_header(algorithm, chunk)
                    })

                    offset += len(chunk)

                    # assert for 204 and offsets match
                    assert patch_response.status_code == 204
                    assert offset == int(patch_response.headers.get('Upload-Offset'))

                #  Get filename for upload and compare test file and uploaded file
                resource_id = resource_url.split('/')[-1]
                uploaded_file = self.flask_tus.repo.find_by_id(resource_id).file.path

                assert filecmp.cmp(TEST_FILE, uploaded_file)

    def test_invalid_checksum(self):
        with open(TEST_FILE, 'rb') as file:
            file_content = file.read()
            file_length = len(file_content)

            # Create initial upload (first upload)
            post_response = self.client.post('/files/', headers={
                'Tus-Version': '1.0.0',
                'Upload-Length': file_length
            })
            resource_url = post_response.headers['Location']

            # Upload chunks
            patch_response = self.client.patch(resource_url, data=file_content, headers={
                'Tus-Version': '1.0.0',
                'Content-Type': 'application/offset+octet-stream',
                'Content-Length': len(file_content),
                'Upload-Offset': 0,
                'Upload-Checksum': 'md5 ZTgwODg0MWMwMzczOTYwMTg5YTA5YzJlNjA3NDdlN2E='  # Random hash
            })

            # assert for 460 Checksum mismatch
            assert patch_response.status_code == 460

    def test_invalid_algorithm(self):
        with open(TEST_FILE, 'rb') as file:
            file_content = file.read()
            file_length = len(file_content)

            # Create initial upload (first upload)
            post_response = self.client.post('/files/', headers={
                'Tus-Version': '1.0.0',
                'Upload-Length': file_length
            })
            resource_url = post_response.headers['Location']

            # Upload file
            patch_response = self.client.patch(resource_url, data=file_content, headers={
                'Tus-Version': '1.0.0',
                'Content-Type': 'application/offset+octet-stream',
                'Content-Length': len(file_content),
                'Upload-Offset': 0,
                'Upload-Checksum': 'invalid_algorithm ZTgwODg0MWMwMzczOTYwMTg5YTA5YzJlNjA3NDdlN2E='
            })

            assert patch_response.status_code == 400
