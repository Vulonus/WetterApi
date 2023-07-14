from unittest import mock

from hamcrest import equal_to, assert_that

from app.common.secrets_manager import SecretsManager


@mock.patch("boto3.session.Session")
def test_secret_manager_get_value(mock_session_class):
    # GIVEN
    mock_session_object = mock.Mock()
    mock_client = mock.Mock()

    mock_client.get_secret_value.return_value = {
        "SecretString": '{"clientId":"foo","clientSecret":"bar"}'
    }

    mock_session_object.client.return_value = mock_client
    mock_session_class.return_value = mock_session_object

    # WHEN
    secrets_manager = SecretsManager("/secret")

    # THEN
    assert_that(secrets_manager.get_value("clientId"), equal_to("foo"))
    assert_that(secrets_manager.get_value("clientSecret"), equal_to("bar"))
