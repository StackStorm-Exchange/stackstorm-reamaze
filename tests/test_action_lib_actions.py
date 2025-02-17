import unittest
from unittest.mock import patch, MagicMock
from lib.actions import BaseAction


class TestBaseAction(unittest.TestCase):

    def setUp(self):
        self.config = {
            'email': 'test@example.com',
            'api_token': 'test_token',
            'brand': 'test_brand'
        }
        self.action = BaseAction(self.config)

    def test_init(self):
        self.assertEqual(self.action._email, 'test@example.com')
        self.assertEqual(self.action._token, 'test_token')
        self.assertEqual(self.action._brand, 'test_brand')
        self.assertEqual(self.action._api_root, 'https://test_brand.reamaze.com/api/v1')

    def test_missing_email(self):
        self.config.pop('email')
        with self.assertRaises(ValueError) as context:
            BaseAction(self.config)
        self.assertEqual(str(context.exception), 'Missing "email" config option')

    def test_missing_brand(self):
        self.config.pop('brand')
        with self.assertRaises(ValueError) as context:
            BaseAction(self.config)
        self.assertEqual(str(context.exception), 'Missing "brand" config option')

    def test_missing_token(self):
        self.config.pop('api_token')
        with self.assertRaises(ValueError) as context:
            BaseAction(self.config)
        self.assertEqual(str(context.exception), 'Missing "api_token" config option')

    @patch('lib.actions.requests.get')
    def test_api_get(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        mock_get.return_value = mock_response

        response = self.action._api_get('/test_endpoint')

        self.assertEqual(response, {'key': 'value'})
        mock_get.assert_called_once_with(
            url='https://test_brand.reamaze.com/api/v1/test_endpoint',
            auth=('test@example.com', 'test_token'),
            params=None,
            headers={'Accept': 'application/json'}
        )

    @patch('lib.actions.requests.get')
    def test_api_get_logs_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"error": "not found"}'
        mock_get.return_value = mock_response

        self.action.logger = MagicMock()
        self.action._api_get('/test_endpoint')

        self.action.logger.error.assert_called_once_with(
            'GET failed. HTTP status: %s, Body: %s.',
            404, '{"error": "not found"}'
        )

    @patch('lib.actions.requests.post')
    def test_api_post(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'key': 'value'}
        mock_post.return_value = mock_response

        response = self.action._api_post('/test_endpoint', json={'data': 'value'})

        self.assertEqual(response, {'key': 'value'})
        mock_post.assert_called_once_with(
            url='https://test_brand.reamaze.com/api/v1/test_endpoint',
            auth=('test@example.com', 'test_token'),
            data=None,
            headers={'Accept': 'application/json'},
            json={'data': 'value'}
        )

    @patch('lib.actions.requests.post')
    def test_api_post_logs_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"error": "bad request"}'
        mock_post.return_value = mock_response

        self.action.logger = MagicMock()
        self.action._api_post('/test_endpoint', json={'data': 'value'})

        self.action.logger.error.assert_called_once_with(
            'POST failed. HTTP status: %s, Body: %s.',
            400, '{"error": "bad request"}'
        )

    @patch('lib.actions.requests.put')
    def test_api_put(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.json.return_value = {'key': 'value'}
        mock_put.return_value = mock_response

        response = self.action._api_put('/test_endpoint', json={'data': 'value'})

        self.assertEqual(response, {'key': 'value'})
        mock_put.assert_called_once_with(
            url='https://test_brand.reamaze.com/api/v1/test_endpoint',
            auth=('test@example.com', 'test_token'),
            data=None,
            headers={'Accept': 'application/json'},
            json={'data': 'value'}
        )

    @patch('lib.actions.requests.put')
    def test_api_put_logs_error(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"error": "bad request"}'
        mock_put.return_value = mock_response

        self.action.logger = MagicMock()
        self.action._api_put('/test_endpoint', json={'data': 'value'})

        self.action.logger.error.assert_called_once_with(
            'PUT failed. HTTP status: %s, Body: %s.',
            400, '{"error": "bad request"}'
        )

    def test_convert_slug(self):
        self.assertEqual(self.action._convert_slug('Test Slug'), 'test-slug')
        self.assertEqual(self.action._convert_slug('Another Test'), 'another-test')
        self.assertIsNone(self.action._convert_slug(None))

    def test_run(self):
        with self.assertRaises(RuntimeError):
            self.action.run()


if __name__ == '__main__':
    unittest.main()
