# 🧾 Document Layout Understanding with LayoutLMv3

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/) 
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://react.dev/)

![Demo](/screenshots/doclayout_demo.gif)

An end-to-end system for understanding the layout and structure of documents using the power of **LayoutLMv3**. This project enables structured extraction of elements like headers, questions, and answers from scanned documents and PDFs through an interactive user-friendly interface.

---

## ✨ Key Features

- **Fine-tuned LayoutLMv3 model for document layout understanding**
- **Supports both image and PDF inputs**
- **RESTful API powered by FastAPI**
- **Intuitive React-based frontend interface**
- **Bounding box visualization for extracted entities**

---

## ⚙️ Installation

### Backend Setup

1. Navigate to the backend folder and install Python dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Copy and configure environment variables:

   ```bash
   cp .env.example .env
   ```

---

### Frontend Setup

1. Navigate to the frontend folder and install dependencies:

   ```bash
   cd frontend
   npm install
   ```

---

## 🚀 Running the Application

### Start Backend (FastAPI)

From the `backend/` directory:

```bash
uvicorn api_service:app --reload --port 8000
```

### Start Frontend (React)

From the `frontend/` directory:

```bash
npm start
```

---