def test_create_card(auth_client):
    response = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"})
    assert response.status_code == 201
    data = response.json()
    assert data["word"] == "안녕"
    assert data["translation"] == "привет"
    assert "id" in data


def test_get_cards(auth_client):
    auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"})
    response = auth_client.get("/cards/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_card(auth_client):
    card_id = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"}).json()["id"]
    response = auth_client.get(f"/cards/{card_id}")
    assert response.status_code == 200
    assert response.json()["word"] == "안녕"


def test_get_card_not_found(auth_client):
    response = auth_client.get("/cards/999")
    assert response.status_code == 404


def test_update_only_changed_field(auth_client):
    card_id = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"}).json()["id"]
    response = auth_client.patch(f"/cards/{card_id}", json={"translation": "хай"})
    assert response.status_code == 200
    assert response.json()["translation"] == "хай"
    assert response.json()["word"] == "안녕"  


def test_delete_card(auth_client):
    card_id = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"}).json()["id"]
    assert auth_client.delete(f"/cards/{card_id}").status_code == 204
    assert auth_client.get(f"/cards/{card_id}").status_code == 404


def test_review_card(auth_client):
    card_id = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"}).json()["id"]
    response = auth_client.post(f"/cards/{card_id}/review", json={"quality": 5})
    assert response.status_code == 200
    assert response.json()["repetitions"] == 1
    assert response.json()["interval"] == 1


def test_review_invalid_quality(auth_client):
    card_id = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"}).json()["id"]
    response = auth_client.post(f"/cards/{card_id}/review", json={"quality": 10})
    assert response.status_code == 422 

def test_get_stats(auth_client):
    card_1 = auth_client.post("/cards/", json={"word": "안녕", "translation": "привет"}).json()
    auth_client.post("/cards/", json={"word": "고양이", "translation": "кот"})
    for _ in range(10):
        auth_client.post(f"/cards/{card_1['id']}/review", json={"quality": 5})
    response = auth_client.get("/cards/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_cards"] == 2
    assert data["new_cards"] == 1
    assert data["average_ease_factor"] > 0


def test_cards_are_isolated_between_users(client):
    client.post("/auth/register", json={"email": "user1@test.com", "password": "123456"})
    r = client.post("/auth/login", data={"username": "user1@test.com", "password": "123456"})
    client.headers["Authorization"] = f"Bearer {r.json()['access_token']}"
    client.post("/cards/", json={"word": "안녕", "translation": "привет"})
    
    client.post("/auth/register", json={"email": "user2@test.com", "password": "123456"})
    r = client.post("/auth/login", data={"username": "user2@test.com", "password": "123456"})
    client.headers["Authorization"] = f"Bearer {r.json()['access_token']}"

    response = client.get("/cards/")
    assert len(response.json()) == 0

def test_unauthorized_request(client):
    response = client.get("/cards")
    assert response.status_code == 401