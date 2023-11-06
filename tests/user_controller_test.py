import pytest
from unittest.mock import patch, MagicMock
from src.internal.users.controllers import UserController
from src.internal.users.schemas import Users as UserEntity
from src.internal.users.models import Users as UserModel
from src.internal.databases import DBConnectionHandler

# Mock the DBConnectionHandler to isolate the function under test
@patch.object(DBConnectionHandler, "__enter__", return_value=MagicMock())
@patch.object(DBConnectionHandler, "__exit__")
# Parametrize the test to cover various cases
@pytest.mark.parametrize(
    "user, expected_result, raises_exception, test_id",
    [
        # Happy path tests with various realistic test values
        (UserEntity(id=1, name="John Doe", email="john@example.com", pseudo="johndoe"), UserEntity(id=1, name="John Doe", email="john@example.com", pseudo="johndoe"), False, "happy_path_1"),
        (UserEntity(id=2, name="Jane Doe", email="jane@example.com", pseudo="janedoe"), UserEntity(id=2, name="Jane Doe", email="jane@example.com", pseudo="janedoe"), False, "happy_path_2"),
        # Edge cases
        (UserEntity(id=3, name="", email="emptyname@example.com", pseudo="emptyname"), UserEntity(id=3, name="", email="emptyname@example.com", pseudo="emptyname"), False, "edge_case_empty_name"),
        (UserEntity(id=4, name="Null Name", email=None, pseudo="nullname"), UserEntity(id=4, name="Null Name", email=None, pseudo="nullname"), False, "edge_case_null_email"),
        # Error cases
        (UserEntity(id=5, name="Exception", email="exception@example.com", pseudo="exception"), None, True, "error_case_exception"),
    ],
    ids=lambda param: param[-1]  # Use the test_id as the pytest id
)

def test_create_user(mock_exit, mock_enter, user, expected_result, raises_exception, test_id):
    # Arrange
    mock_save = MagicMock()
    mock_save.side_effect = Exception("Test Exception") if raises_exception else None
    mock_save.return_value = UserModel(
        id=user.id,
        name=user.name,
        email=user.email,
        pseudo=user.pseudo,
        create_at=None,
        update_at=None,
        badges=None
    )
    with patch("src.internal.users.controllers.save", new=mock_save):

        # Act
        if raises_exception:
            with pytest.raises(Exception, match="Test Exception"):
                result = UserController.create_user(user)
        else:
            result = UserController.create_user(user)

        # Assert
        if not raises_exception:
            assert result == expected_result
