import pytest


@pytest.mark.usefixtures('class_client')
class TestResponses(object):
    def test_options_request(self):
        response = self.client.options('/files/', headers={'Tus-Version': '1.0.0'})
        # A successful response indicated by the 204 No Content
        # or 200 OK status MUST contain the Tus-Version header.
        assert response.status_code in (204, 200)
        assert response.headers.get('Tus-Version') == '1.0.0'

    def test_post_request(self):
        response = self.client.post('/files/', headers={'Tus-Version': '1.0.0', 'Upload-Length': '1000'})
        assert response.status_code == 201
        assert response.headers.get('Location') is not None
        assert response.headers.get('Upload-Defer-Length') is None
        assert response.headers.get('Upload-Length') == '1000'

    def test_defer_post(self):
        # If Upload-Length is unknown, server should
        # respond with Upload-Defer-Length = 1.
        response = self.client.post('/files/', headers={'Tus-Version': '1.0.0'})
        assert response.status_code == 201
        assert response.headers.get('Upload-Defer-Length') == '1'
        assert response.headers.get('Upload-Length') is None

    def test_nonexistent_resource(self):
        head_response = self.client.head('/files/VeryUnlikelyUUID', headers={'Tus-Version': '1.0.0'})
        patch_response = self.client.patch('/files/EvenMoreUnlikelyUUID', headers={'Tus-Version': '1.0.0'})
        assert head_response.status_code == 404
        assert patch_response.status_code == 404

    def test_content_type_patch(self):
        post_response = self.client.post('/files/', headers={'Tus-Version': '1.0.0', 'Upload-Length': '1000'})
        resource_url = post_response.headers['Location']
        response = self.client.patch(resource_url,
                                     headers={'Tus-Version': '1.0.0', 'Content-Length': '1000', 'Upload-Offset': '0'})
        assert response.status_code == 415
