from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('comments.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()

# Define a model for creating comments
class CommentCreate(BaseModel):
    text: str

# API endpoint to get all comments
@app.get("/api/comments")
def get_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()
    conn.close()
    return comments

# API endpoint to create a new comment
@app.post("/api/comments")
def create_comment(comment: CommentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (text) VALUES (?)", (comment.text,))
    conn.commit()
    comment_id = cursor.lastrowid
    conn.close()
    return {"id": comment_id, "text": comment.text}
