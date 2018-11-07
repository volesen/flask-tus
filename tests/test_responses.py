import pytest


@pytest.mark.usefixtures('class_client')
class TestResponses(object):
    def test_option_request(self):
        response = self.client.options('/files/')
        # A successful response indicated by the 204 No Content
        # or 200 OK status MUST contain the Tus-Version header.
        assert response.status_code in (204, 200)
        assert response.headers.get('Tus-Version') == '1.0.0'

    def test_post_request(self):
        response = self.client.post('/files/', headers={'Upload-Length': '1000'})
        assert response.status_code == 204
        assert response.headers.get('Location') is not None
        assert response.headers.get('Upload-Defer-Length') is None
        assert response.headers.get('Upload-Length') == '1000'

    def test_defer_post(self):
        # If Upload-Length is unknown, server should
        # respond with Upload-Defer-Length = 1.
        response = self.client.post('/files/')
        assert response.status_code == 204
        assert response.headers.get('Upload-Defer-Length') == '1'
        assert response.headers.get('Upload-Length') is None

    def test_nonexistent_resource(self):
        head_response = self.client.head('/files/VeryUnlikelyUUID')
        patch_response = self.client.patch('/files/EvenMoreUnlikelyUUID')
        assert head_response.status_code == 404
        assert patch_response.status_code == 404

    def test_content_type_patch(self):
        resource_url = self.client.post('/files/', headers={'Upload-Length': '1000'}).headers['Location']
        response = self.client.patch(resource_url)
        assert response.status_code == 415
