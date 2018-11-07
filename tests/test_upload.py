import pytest


@pytest.mark.usefixtures('class_client')
class TestUpload(object):
    def test_small_upload(self):
        assert 1 == 1
