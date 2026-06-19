from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Notes(BaseModel):
    title: str
    content: str

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='P1 DB', user='postgres', password='saad@512', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database was connected sucessfully")
        break

    except Exception as error:
        print("Connecting to Database failed")
        print(f"Error: {error}")
        time.sleep(2)

@app.get("/notes")
def get_notes():
    cursor.execute("""SELECT * FROM notes""")
    notes = cursor.fetchall()

    return {"data": notes}

@app.post("/notes")
def create_note(note: Notes):
    cursor.execute("""INSERT INTO notes (title, content) VALUES(%s, %s) RETURNING *""", (note.title, note.content))
    created_notes = cursor.fetchone()

    return {"data": created_notes}

