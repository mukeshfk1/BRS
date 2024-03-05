from main import app


from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200

def test_get_review():
    response = client.get("/reviews/?book_id=1")
    assert response.status_code == 200

def test_add_book():
    response = client.post("/books/", 
                           json={"title": "Test Book", "author": "Test Author", "publication_year": 2024},
                           )

    assert response.status_code == 201
    assert response.json() == {"detail":"new book has been added"}

def test_update_book():
    response = client.put("/books/?book_id=1", 
                           json={"title": "Update Test Book", "author": "Update Test Author"},
                           )
    assert response.status_code == 200
    assert response.json() == {"detail":"book has been updated"}