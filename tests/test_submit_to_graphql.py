from unittest.mock import MagicMock, patch

from test_new.submit_to_graphql import submit_to_graphql


@patch("test_new.submit_to_graphql.Client")
def test_submit_to_graphql(mock_client: MagicMock):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.execute.return_value = {
        "submitWorkflowTemplate": {"name": "workflow123"}
    }
    submit_to_graphql()
    mock_instance.execute.assert_called_once()
