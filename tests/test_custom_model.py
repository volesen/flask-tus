import pytest
import hashlib
from flask_tus.models.mongoengine_upload import MongoengineBaseUpload, MongoengineUpload

CHUNK_SIZE = 1024
TEST_FILE = 'tests/data/flask.png'


@pytest.mark.usefixtures('class_client')
class TestMD5(object):

    md5 = hashlib.md5()

    @staticmethod
    def __read_chunks(file, chunk_size):
        return iter(lambda: file.read(chunk_size), b'')

    def test_checksum_upload(self):
        if not isinstance(self.flask_tus.model(), MongoengineUpload):
            pytest.skip("This only test non-base mongoengine upload")

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
                self.md5.update(chunk)

                patch_response = self.client.patch(resource_url, data=chunk, headers={
                    'Tus-Version': '1.0.0',
                    'Content-Type': 'application/offset+octet-stream',
                    'Content-Length': len(chunk),
                    'Upload-Offset': offset,
                })

                offset += len(chunk)

                # assert for 204 and offsets match
                assert patch_response.status_code == 204
                assert offset == int(
                    patch_response.headers.get('Upload-Offset'))

            #  Get filename for upload and compare test file and uploaded file
            resource_id = resource_url.split('/')[-1]

            with self.app.app_context():
                upload = self.flask_tus.repo.find_by_id(resource_id)
                assert upload.md5 == self.md5.hexdigest()
