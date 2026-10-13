# Project Commands Guide

## 1. Run Both Models Side-by-Side in CMD (Interactive)

.\backend\.venv\Scripts\python.exe scripts\compare_cli.py


What is electrochemistry?


## 2. Run RAG Model in CMD (Interactive - You type questions)


.\backend\.venv\Scripts\python.exe RAG\chat.py


## 3. Run Fine-Tuning Model in CMD (Interactive)

.\backend\.venv\Scripts\python.exe Fine-Tuning\inference\chat.py


### Backend (Terminal 1)

.\.venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload


### Frontend (Terminal 2)

npm run dev
