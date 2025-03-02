import pytest
from typing import List
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    posts_list = list(map(lambda p: schemas.PostOut(**p), response.json()))
    print(response.json())
    print(response.status_code)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    print(res.json())
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get(f"/posts/51")
    print(res.json())
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published",[
    ("Lotus", "Europa", True),
    ("Debian", "vs Fedora", False),
    ("Lola", "T70", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/", json={"title": "check", "content": "if published"})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "check"
    assert created_post.content == "if published"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_create_post_unauthorized_user(client):
    response = client.post("/posts/", json={"title": "check", "content": "if published"})
    print(response.json())
    assert response.status_code == 401


def test_delete_post_unautorized_user(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    print(response.json())
    assert response.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    # print(response.json()) # Fails - No Content
    assert response.status_code == 204


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
        response = authorized_client.delete(f"/posts/51")
        print(response.json())
        assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    print(response.json())
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    print(response.json())
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 202
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_post_other_user(authorized_client, test_user, test_user_extra, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403


def test_update_post_unautorized_user(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=data)
    print(response.json())
    assert response.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
        data = {
            "title": "updated title",
            "content": "updated content",
            "id": test_posts[3].id
        }
        response = authorized_client.put(f"/posts/51", json=data)
        print(response.json())
        assert response.status_code == 404