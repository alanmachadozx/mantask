# Mantask

Mantask is a RESTful API project developed to deepen Python skills, understand integration with relational databases, and implement authenticated routes for a task management system back-end.

# Technologies Used:

* Web Framework: FastAPI
* ASGI Server: Uvicorn
* Database: SQLite
* ORM: SQLModel / SQLAlchemy
* Authentication & Security: PyJWT (JSON Web Tokens) & Passlib (PBKDF2 for password hashing)
* Automatic Documentation: Swagger UI / OpenAPI

Features

* User Management: New user registration and authentication via login.
* Security: Password encryption and JWT token generation for protected routes.
* Task Management: Creation of tasks directly linked to the authenticated user's ID.

# Getting Started

Run the following commands in your terminal to clone the repository, set up the environment, install dependencies, and start the server:

```bash
# Clone the repository and navigate into the project directory
git clone https://github.com/alanmachadozx/mantask.git
cd mantask

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies and launch the development server
pip install -r requirements.txt
uvicorn src.main:app --reload
