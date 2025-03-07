import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    print(response.json())
    assert response.status_code == 201


def test_vote_on_post_other_user(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    print(response.json())
    assert response.status_code == 201


def test_vote_post_twice(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    print(response.json())
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    print(response.json())
    assert response.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert response.status_code == 404


def test_vote_post_not_exist(authorized_client):
    response = authorized_client.post("/vote/", json={"post_id": 51, "dir": 0})
    assert response.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert response.status_code == 401