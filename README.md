# Project Title
Full Auth Flask Backend - Productivity App

## Project Description
This project implements a secure Flask RESTful API backend for a productivity application. It features user authentication using JSON Web Tokens (JWT) and provides full CRUD (Create, Read, Update, Delete) operations for a user-owned resource, specifically 'Notes'. The API ensures that users can only access and manage their own data, with pagination implemented for listing notes.

## Installation Instructions

1.  **Clone the repository (or download the ZIP):**
    ```bash
    git clone <your-repo-url>
    cd flask_notes_api
    ```

2.  **Install dependencies using Pipenv:**
    If you don't have Pipenv installed, install it first:
    ```bash
    pip install pipenv
    ```
    Then, navigate to the project directory and install the dependencies:
    ```bash
    pipenv install
    pipenv shell
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the `productivity_backend` directory with the following content:
    ```
    SECRET_KEY='your_flask_secret_key_here'
    JWT_SECRET_KEY='your_jwt_secret_key_here'
    ```
    Replace the placeholder values with strong, unique keys.

4.  **Initialize and migrate the database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5.  **Seed the database with example data:**
    ```bash
    python seed.py
    ```

## Run Instructions

To run the Flask application, ensure you are in the `productivity_backend` directory and have activated your pipenv shell:

```bash
flask run
```

The API will typically run on `http://127.0.0.1:5000`.

## API Endpoints

### Authentication

*   **`POST /signup`**
    *   **Description:** Registers a new user.
    *   **Request Body:** `{"username": "<username>", "password": "<password>"}`
    *   **Response:** `{"message": "User created successfully", "user": {"id": <id>, "username": "<username>"}, "access_token": "<jwt_token>"}`
    *   **Status Codes:** `201 Created`, `400 Bad Request` (e.g., username exists, validation errors)

*   **`POST /login`**
    *   **Description:** Authenticates a user and returns a JWT access token.
    *   **Request Body:** `{"username": "<username>", "password": "<password>"}`
    *   **Response:** `{"access_token": "<jwt_token>", "user": {"id": <id>, "username": "<username>"}}`
    *   **Status Codes:** `200 OK`, `401 Unauthorized` (invalid credentials)

*   **`POST /logout`**
    *   **Description:** Logs out the current user. (For JWT, this typically means invalidating the token on the client-side).
    *   **Response:** `{"message": "Successfully logged out"}`
    *   **Status Codes:** `200 OK`

*   **`GET /me`**
    *   **Description:** Retrieves information about the currently authenticated user.
    *   **Headers:** `Authorization: Bearer <jwt_token>`
    *   **Response:** `{"id": <id>, "username": "<username>"}`
    *   **Status Codes:** `200 OK`, `401 Unauthorized` (missing/invalid token), `404 Not Found` (user not found)

### Notes Resource

*   **`GET /notes`**
    *   **Description:** Retrieves a paginated list of notes belonging to the authenticated user.
    *   **Headers:** `Authorization: Bearer <jwt_token>`
    *   **Query Parameters:** `page` (int, default 1), `per_page` (int, default 10)
    *   **Response:** `{"notes": [{"id": <id>, "title": "<title>", "content": "<content>", "created_at": "<timestamp>", "updated_at": "<timestamp>", "user_id": <user_id>}], "total": <total_notes>, "pages": <total_pages>, "current_page": <current_page>, "next_page": <next_page_num>, "prev_page": <prev_page_num>}`
    *   **Status Codes:** `200 OK`, `401 Unauthorized`

*   **`POST /notes`**
    *   **Description:** Creates a new note for the authenticated user.
    *   **Headers:** `Authorization: Bearer <jwt_token>`
    *   **Request Body:** `{"title": "<note_title>", "content": "<note_content>"}`
    *   **Response:** `{"id": <id>, "title": "<title>", "content": "<content>", "created_at": "<timestamp>", "updated_at": "<timestamp>", "user_id": <user_id>}`
    *   **Status Codes:** `201 Created`, `400 Bad Request`, `401 Unauthorized`

*   **`GET /notes/<int:note_id>`**
    *   **Description:** Retrieves a specific note by its ID, ensuring it belongs to the authenticated user.
    *   **Headers:** `Authorization: Bearer <jwt_token>`
    *   **Response:** `{"id": <id>, "title": "<title>", "content": "<content>", "created_at": "<timestamp>", "updated_at": "<timestamp>", "user_id": <user_id>}`
    *   **Status Codes:** `200 OK`, `401 Unauthorized`, `404 Not Found`

*   **`PATCH /notes/<int:note_id>`**
    *   **Description:** Updates an existing note by its ID, ensuring it belongs to the authenticated user.
    *   **Headers:** `Authorization: Bearer <jwt_token>`
    *   **Request Body:** `{"title": "<new_title>", "content": "<new_content>"}` (fields are optional)
    *   **Response:** `{"id": <id>, "title": "<updated_title>", "content": "<updated_content>", "created_at": "<timestamp>", "updated_at": "<timestamp>", "user_id": <user_id>}`
    *   **Status Codes:** `200 OK`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`

*   **`DELETE /notes/<int:note_id>`**
    *   **Description:** Deletes a specific note by its ID, ensuring it belongs to the authenticated user.
    *   **Headers:** `Authorization: Bearer <jwt_token>`
    *   **Response:** `{"message": "Note deleted successfully"}`
    *   **Status Codes:** `200 OK`, `401 Unauthorized`, `404 Not Found`
