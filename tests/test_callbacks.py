import pytest

CHUNK_SIZE = 1024
TEST_FILE = 'tests/data/flask.png'


@pytest.mark.usefixtures('class_client')
class TestCallbacks(object):
    # Side effects for callbacks
    pre_saves = 0
    post_saves = 0
    created = False
    completed = False
    pre_delete = False
    post_delete = False

    @staticmethod
    def __read_chunks(file, chunk_size):
        return iter(lambda: file.read(chunk_size), b'')

    def _on_create(self):
        self.created = True

    def _pre_save(self):
        self.pre_saves += 1

    def _post_save(self):
        self.post_saves += 1

    def _on_complete(self):
        self.completed = True

    def _pre_delete(self):
        self.pre_delete = True

    def _post_delete(self):
        self.post_delete = True

    def test_callbacks(self):
        # Inject callbacks and mock upload
        self.app.flask_tus.pre_save = self._pre_save
        self.app.flask_tus.post_save = self._post_save
        self.app.flask_tus.on_create = self._on_create
        self.app.flask_tus.on_complete = self._on_complete
        self.app.flask_tus.pre_delete = self._pre_delete
        self.app.flask_tus.post_delete = self._post_delete

        with open(TEST_FILE, 'rb') as file:
            file_length = len(file.read())

            # Set file pos to 0 after reading
            file.seek(0)

            # Create initial upload (first upload)
            post_response = self.client.post('/files/', headers={
                'Tus-Version': '1.0.0',
                'Upload-Length': file_length
            })

            assert self.created
            resource_url = post_response.headers['Location']
            resource_id = resource_url.split('/')[-1]

            offset = 0
            chunks = 0
            # Upload chunks
            for chunk in self.__read_chunks(file, CHUNK_SIZE):
                response = self.client.patch(resource_url, data=chunk, headers={
                    'Tus-Version': '1.0.0',
                    'Content-Type': 'application/offset+octet-stream',
                    'Content-Length': len(chunk),
                    'Upload-Offset': offset
                })
                offset += len(chunk)
                chunks += 1

            # Assert callback side-effects, assuming successful upload
            assert self.pre_saves == chunks
            assert self.post_saves == chunks
            assert self.completed
        
        # Assert callback side-effects, assuming successful deletion
        with self.app.app_context():
            self.flask_tus.model.get(resource_id).delete()

        assert self.pre_delete
        assert self.post_delete