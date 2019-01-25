import pytest
import filecmp

CHUNK_SIZE = 1024
TEST_FILE = 'tests/data/flask.png'


@pytest.mark.usefixtures('class_client')
class TestUpload(object):

    @staticmethod
    def __read_chunks(file, chunk_size):
        return iter(lambda: file.read(chunk_size), b'')

    def test_chunked_upload(self):
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
                    'Upload-Offset': offset
                })
                offset += len(chunk)

                # assert for 204 and offsets match
                assert patch_response.status_code == 204
                assert offset == int(patch_response.headers.get('Upload-Offset'))

            #  Get filename for upload and compare test file and uploaded file
            resource_id = resource_url.split('/')[-1]
            uploaded_file = self.flask_tus.repo.find_by_id(resource_id).file.name

            assert filecmp.cmp(TEST_FILE, uploaded_file)
