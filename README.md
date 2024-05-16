<h1 align="center">FastAPI Full-Stack Application (ToDo App)</h1>
<h3 align="center">🌟 Simple example of using FastAPI in a Full-Stack project with Poetry and Docker 🌟</h3>
<br>

## 📜 Features
- Authentication & Authorization
  - JWT
  - Login/Register
- CRUD operation on ToDos
- Dockerized
- Using Alembic as migration tool
- Using Poetry

## 🛠 Installation
1. **Clone the repository**
   
   `git clone https://github.com/Aron-S-G-H/fastapi-fullstack-todo.git`

   then...

   `cd fastapi-fullstack-todo`
2. **Create and activate a virtual environment**

   `python3 -m venv venv` or `virtualenv venv`

   then...

   `source venv/bin/activate`
3. **Install dependencies**
   
   `pip install -r requirements.txt` or `poetry install`
4. **Start the app**

   `python3 main.py` or `uvicorn settings:main --host 0.0.0.0 --port 8000` or `poetry run python3 main.py`

## 🚀 Run with Docker
---
<h4 align="center">⚠️ Ensure that you have Docker installed before you proceed</h4>

---

1. **Clone the repository**
   
   `git clone https://github.com/Aron-S-G-H/fastapi-fullstack-todo.git`

   then...

   `cd fastapi-fullstack-todo`
2. **Create an image**
   
   `docker build -t todoapp:latest --no-cache .`
3. **Run a container**

   `docker run --name todoApp -p 8000:8000 -d todoapp:latest`
> **Note** : If you encounter the error 'ERROR: Exception TimeoutError: timed out' while creating the image, go to the Dockerfile and either remove or comment out line 27. Then, try building the image again.
