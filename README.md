\# Document Layout Understanding with LayoutLMv3



!\[Document Parsing Demo](demo.gif) <!-- Add a demo GIF later -->



This project provides an end-to-end solution for document layout understanding using LayoutLMv3. It extracts structured information (headers, questions, answers, etc.) from documents through a FastAPI backend and React frontend.



\## Features



\- 🧠 Fine-tuned LayoutLMv3 model for document understanding

\- 📄 Supports images and PDF documents

\- 🌐 REST API with FastAPI backend

\- ⚛️ React-based frontend interface

\- 📊 Entity extraction with bounding box visualization

\- 🚀 Easy deployment with Docker



\## Installation



\### Backend Setup



1\. Install Python dependencies:

'''bash

cd backend

pip install -r requirements.txt



2\. Set environment variables:

cp .env.example .env



\### Frontend Setup

'''bash

cd frontend

npm install



\## Running the Application



\###Backend

'''bash

uvicorn api\_service:app --reload --port 8000



\###Frontend

'''bash

npm start

