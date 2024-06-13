from project.users.models import User
from project.users import users_router
from unittest import mock
import requests

def test_pytest_setup(client, db_session):
    response = client.get(users_router.url_path_for("form_example_get"))
    assert response.status_code == 200
    
    user = User(username="test", email="test@example.com")
    with db_session.begin():
        db_session.add(user)
    assert user.id
    
    
# test solution 1
    
def test_view_with_eager_mode(client, db_session, settings, monkeypatch):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)
    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)
    
    user_name = "michaelyin"
    user_email = f"{user_name}@example.com"
    response = client.post(
        users_router.url_path_for("user_subscribe"),
        json={"email": user_email, "username": user_name},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "send task to Celery successfully",
    }
    
    mock_requests_post.assert_called_with(
        "https://httpbin.org/delay/5",
        data={"email": user_email}
    )
    
# Test solution 2 
from project.users.factories import UserFactory
from project.users import tasks

def test_user_subscribe_view(client, db_session, settings, monkeypatch):
    user = UserFactory.build()
    
    task_add_subscribe = mock.MagicMock(name="task_add_subscribe")
    task_add_subscribe.return_value = mock.MagicMock(task_id="task_id")
    monkeypatch.setattr(tasks.task_add_subscribe, "delay", task_add_subscribe)
    
    response = client.post(
        users_router.url_path_for("user_subscribe"),
        json={"email": user.email, "username": user.username}
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "send task to Celery successfully",
    }
    
    user = db_session.query(User).filter_by(username=user.username).first()
    task_add_subscribe.assert_called_with(user.id)
    
    
# pytest-factoryboy from tests/users/test_views.py
def test_user_subscribe_view(client, db_session, settings, monkeypatch, user_factory):
    user = user_factory.build()

    task_add_subscribe = mock.MagicMock(name="task_add_subscribe")
    task_add_subscribe.return_value = mock.MagicMock(task_id="task_id")
    monkeypatch.setattr(tasks.task_add_subscribe, "delay", task_add_subscribe)

    response = client.post(
        users_router.url_path_for('user_subscribe'),
        json={"email": user.email, "username": user.username}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "send task to Celery successfully",
    }

    # query from the db again
    user = db_session.query(User).filter_by(username=user.username).first()
    task_add_subscribe.assert_called_with(
        user.id
    )

