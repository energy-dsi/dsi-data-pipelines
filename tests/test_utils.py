# Script to test the utilities for the adaptor

import base64
import unittest

import kubernetes.client.exceptions

from unittest.mock import patch, MagicMock

from templates.adaptor.utils import get_k8_secret
from templates.adaptor.utils import get_blob_object

from azure.core.exceptions import ResourceNotFoundError

class TestAdaptorUtils(unittest.TestCase):

    @patch('templates.adaptor.utils.client.CoreV1Api')
    @patch('templates.adaptor.utils.config.load_kube_config')
    def test_get_k8_secret(self, mock_load_kube_config, mock_core_v1_api):
        """
        Description: test the normal functioning of the get_k8_secret function.
        """

        mock_load_kube_config.return_value = None
        mock_secret_data = {'my-secret-key': base64.b64encode(b'my-secret-value').decode('utf-8')}

        mock_secret = MagicMock()
        mock_secret.data = mock_secret_data
        mock_core_v1_api.return_value.read_namespaced_secret.return_value = mock_secret

        actual = get_k8_secret('my-secret', 'default')
        expected = 'my-secret-value'

        self.assertEqual(actual, expected)

    @patch('templates.adaptor.utils.client.CoreV1Api')
    @patch('templates.adaptor.utils.config.load_kube_config')
    def test_secret_not_found(self, mock_load_kube_config, mock_core_v1_api):
        """
        Description: test the function when the secret is not found.
        """

        mock_load_kube_config.return_value = None
        mock_core_v1_api.return_value.read_namespaced_secret.side_effect = kubernetes.client.exceptions.ApiException(status=404)

        with self.assertRaises(kubernetes.client.exceptions.ApiException) as context:
            get_k8_secret('non-existent-secret', 'default')

        actual = context.exception.status
        expected = 404

        self.assertEqual(actual, expected)

    @patch('templates.adaptor.utils.client.CoreV1Api')
    @patch('templates.adaptor.utils.config.load_kube_config')
    def test_kube_config_load_failure(self, mock_load_kube_config, mock_core_v1_api):
        """
        Description: test the function when the kube config load fails.
        """

        mock_load_kube_config.side_effect = Exception("Kube config load failed")

        with self.assertRaises(Exception) as context:
            get_k8_secret('my-secret', 'default')

        actual = str(context.exception)
        expected = "Kube config load failed"

        self.assertEqual(actual, expected)

    @patch("templates.adaptor.utils.BlobServiceClient")
    def test_get_blob_object(self, mock_blob_service_client):
        """
        Description: test the normal functioning of the get_blob_object function.
        """

        account_url = "https://example.blob.core.windows.net"
        container_name = "test-container"
        blob_name = "test-blob"
        credential = "test-credential"
        blob_content = "Hello, Blob!"

        mock_blob_client = MagicMock()
        mock_blob_client.download_blob().readall.return_value = blob_content.encode("utf-8")
        mock_blob_service_client_instance = MagicMock()
        mock_blob_service_client_instance.get_blob_client.return_value = mock_blob_client
        mock_blob_service_client.return_value = mock_blob_service_client_instance

        actual = get_blob_object(account_url, container_name, blob_name, credential)
        expected = blob_content

        mock_blob_service_client.assert_called_once_with(account_url=account_url, credential=credential)
        mock_blob_service_client_instance.get_blob_client.assert_called_once_with(
            container=container_name, blob=blob_name
        )
        mock_blob_client.download_blob().readall.assert_called_once()

        self.assertEqual(actual, expected)

    @patch('templates.adaptor.utils.BlobServiceClient')
    def test_get_blob_object_not_found(self, mock_blob_service_client):
        """
        Description: test the function when the file is not found.
        """

        account_url = "https://example.blob.core.windows.net"
        container_name = "test-container"
        blob_name = "nonexistent-blob"
        credential = "test-credential"

        mock_blob_client = MagicMock()
        mock_blob_client.download_blob.side_effect = ResourceNotFoundError("Blob not found")
        mock_blob_service_client_instance = MagicMock()
        mock_blob_service_client_instance.get_blob_client.return_value = mock_blob_client
        mock_blob_service_client.return_value = mock_blob_service_client_instance

        with self.assertRaises(ResourceNotFoundError) as context:
            get_blob_object(account_url, container_name, blob_name, credential)

        mock_blob_service_client.assert_called_once_with(account_url=account_url, credential=credential)
        mock_blob_service_client_instance.get_blob_client.assert_called_once_with(
            container=container_name, blob=blob_name
        )
        mock_blob_client.download_blob.assert_called_once()
