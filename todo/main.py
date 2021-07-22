from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/all_todos')
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    # print(db)
    # lst =[]
    # for i in db:
    #     lst.append(i)
    return todos

@app.post('/')
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = crud.create_todo(db, todo)
    return db_todo

@app.put('/{id}')
def update_todo(id: int, done: bool = True, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=id, done=done)
    return db_todo

@app.get('/done')
def completed_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    lst = []
    for i in todos:
        print("done", i.done)
        if i.done:
            print("inside if loop")
            lst.append(i)
    print("lst", lst)
    return lst

@app.get('/incomplete')
def incompleted_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    lst = []
    for i in todos:
        print("done", i.done)
        if not i.done:
            print("inside if loop")
            lst.append(i)
    print("lst", lst)
    return lst



