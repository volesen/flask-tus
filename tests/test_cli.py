import pytest
import datetime
from flask_tus.manage.commands import delete_expired as cmd


@pytest.mark.usefixtures('class_client')
class TestResponses(object):
    def test_expired_upload(self):
        # Create initial upload
        headers = {'Tus-Version': '1.0.0', 'Upload-Length': '1000'}
        post_response = self.client.post('/files/', headers=headers)
        resource_url = post_response.headers['Location']

        self.app.config['TUS_TIMEDELTA'] = datetime.timedelta(days=-1)
        headers = {'Tus-Version': '1.0.0', 'Content-Length': '1000', 'Upload-Offset': '0'}
        patch_response = self.client.patch(resource_url, headers=headers)
        # Assert 410 gone as resource should be expired
        assert patch_response.status_code == 410

    def test_delete_expired_uploads(self):
        # Create initial upload
        post_response = self.client.post('/files/', headers={'Tus-Version': '1.0.0', 'Upload-Length': '1000'})

        resource_url = post_response.headers['Location']
        resource_id = resource_url.split('/')[-1]

        # Create expired upload
        with self.app.app_context():
            self.flask_tus.repo.find_by_id(resource_id).created_on -= self.app.config['TUS_TIMEDELTA']
        
        # Run CLI command
        runner = self.app.test_cli_runner()    
        result = runner.invoke(cmd)

        # Assert output, assuming succesful deletion
        assert result.output == 'Deleting expired uploads\nSuccessfully deleted expired uploads deleted\n'

        headers = {'Tus-Version': '1.0.0', 'Content-Length': '1000', 'Upload-Offset': '0'}
        head_response = self.client.head(resource_url, headers=headers)
        # Assert 404 Not Found, as resource should be deleted
        assert head_response.status_code == 404
