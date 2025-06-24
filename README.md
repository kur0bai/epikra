
# 🐍 Epikra CMS
Epikra is a lightweight, powerful, and extensible Headless CMS built with **FastAPI**,  designed to be simple to deploy and scale for people who wants the power of python for building blogs or content quickly. Ideal for developers who need flexibility and performance, with modern features such as automatic slug generation, authentication, **AI-enhanced content** endpoints using Huggingface, dynamic table creation, and full Docker + PostgreSQL support.

## ✨ Features

- ⚡ **FastAPI** as the main async backend (blazing fast)
- 🧠 **AI-powered endpoint** to improve post content automatically
- 🔒 **Authentication system** using JWT
- 📝 **Automatic slug generation** (SEO-friendly)
- 🧩 **Dynamic table creation** without manual migrations
- 🐳 **Dockerized** with production-ready setup using **PostgreSQL**
- 🧬 **Lightweight and modular**, great for scaling
- 💻 **Fully-documented RESTful API** (Swagger UI)
- 💚 **Open Source**

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [JWT](https://jwt.io/)
- [Hugging Face](https://huggingface.co/) (Using Mixtral model, you can use whatever you want to)

## 🚀 Quick Start

### Clone the repository

```bash
git clone https://github.com/kur0bai/epikra.git
cd epikra
```

### Set your Environment variables

```bash
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""
POSTGRES_PORT=5432
POSTGRES_HOST=""
HUGGINGFACE_API_KEY=""
```
### Run with docker (Recommended)
```bash
docker-compose up --build
```
### Run manually
```bash
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload
``` 
## 📚 API Documentation

This time I'm using swagger so to get the full API documentation, you need to get to 
`http://localhost:8000/docs`

## 🤝 Contributing

Contributions are welcome! To suggest improvements, fix bugs, or collaborate.

## 📄 License
This project is licensed under the **MIT License**. See the LICENSE file for details.