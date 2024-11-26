from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException
from fastapi import status

from datetime import datetime

from unittest.mock import patch, MagicMock
import pytest

from src.utils import errors
from src.api.users_ep import router
from src.service.user_service import login
from src.repository import user_repository


client = TestClient(router)


def test_login_ep_successful():
    with patch("src.api.users_ep.user_service.login", return_value="mocked_token") as mock_login:
        response = client.post("/api/login", json={"username": "test_user", "password": "test_password"})

        assert response.status_code == 200
        assert response.json() == "mocked_token"

        args, kwargs = mock_login.call_args
        assert args[0].username == "test_user"
        assert args[0].password == "test_password"


def test_login_ep_invalid_credentials():
    with patch("src.api.users_ep.user_service.login", side_effect=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")) as mock_login:

        with pytest.raises(HTTPException) as e:
            client.post("/api/login", json={"username": "test_user", "password": "wrong_password"})

        assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert e.value.detail == "Invalid credentials"

        args, kwargs = mock_login.call_args
        assert args[0].username == "test_user"
        assert args[0].password == "wrong_password"


def test_login_service_successful():
    mock_user = MagicMock()
    mock_user.id = "57140f5a-e299-43e6-866d-aa81fe9e6a9d"
    mock_user.username = "test_user"
    mock_user.password = "hashed_password"
    mock_user.user_type = "client"
    mock_user.is_active = True
    mock_token = MagicMock()
    mock_token.token = "mocked_token"
    
    with patch("src.service.user_service.user_repository.UserRepository.get", return_value=mock_user) as mock_user_repo_get, \
        patch("src.service.user_service.verify", return_value=True) as mock_verify, \
        patch("src.service.user_service.user_repository.TokenRepository.get", return_value=None) as mock_token_repo_get, \
        patch("src.service.user_service.user_repository.TokenRepository.create", return_value=mock_token) as mock_token_repo_create, \
        patch("src.service.user_service.auth.create_access_token", return_value="mocked_token") as mock_create_access_token:

        user_credentials =  MagicMock(username="test_user", password="test_password")
        result = login(user_credentials)

        assert result == "mocked_token"
        
        args, kwargs = mock_user_repo_get.call_args
        assert args[0].username == "test_user"

        mock_verify.assert_called_once_with("test_password", "hashed_password")

        args, kwargs = mock_token_repo_get.call_args
        assert str(args[0].user_id) == "57140f5a-e299-43e6-866d-aa81fe9e6a9d"
        assert args[0].exists == True

        mock_create_access_token.assert_called_once_with("57140f5a-e299-43e6-866d-aa81fe9e6a9d", "client")
        mock_token_repo_create.assert_called_once()


def test_login_service_user_not_found():
    with patch("src.service.user_service.user_repository.UserRepository.get", side_effect=errors.UserNotFound) as mock_user_repo_get:
        user_credentials = MagicMock(username="unknown_user", password="test_password")

        with pytest.raises(HTTPException) as e:
            login(user_credentials)
        
        assert e.value.status_code == status.HTTP_404_NOT_FOUND
        assert e.value.detail == "User not found"

        args, kwargs = mock_user_repo_get.call_args
        assert args[0].username == "unknown_user"


def test_repository_get_token_by_user_id_successful():
    mock_token = MagicMock()
    mock_token.token = "mocked_token"
    mock_token.expiration_date = "2024-12-31T23:59:59"
    mock_token.is_active = True
    mock_token.user_id = "57140f5a-e299-43e6-866d-aa81fe9e6a9d"
    mock_token.role = "client"

    params = MagicMock(user_id="57140f5a-e299-43e6-866d-aa81fe9e6a9d")

    with patch("src.repository.user_repository.TokenRepository.get_db") as mock_get_db:
        session = MagicMock()
        mock_get_db.return_value.__enter__.return_value = session
        session.query.return_value.filter.return_value.first.return_value = mock_token

        result = user_repository.TokenRepository.get(params)

        session.query.assert_called()
        session.query.return_value.filter.assert_called()
        
        assert result.token == "mocked_token"
        assert result.expiration_date == datetime(2024, 12, 31, 23, 59, 59)
        assert result.is_active is True
        assert str(result.user_id) == "57140f5a-e299-43e6-866d-aa81fe9e6a9d"
        assert result.role == "client"
