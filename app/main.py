from fastapi import FastAPI, Depends, Path, HTTPException
from app.validations.TodoRequest import TodoRequest
from .models.Todo import Base, Todos
from .db.connection import engine, SessionLocal
from starlette import status # type: ignore
from sqlalchemy.orm import Session #type: ignore
from typing import Annotated


app = FastAPI()

Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/todos')
async def get_todos(db: db_dependency): # type: ignore 
    todos = db.query(Todos).all()
    return todos

@app.get('/todos/{id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(db:db_dependency, id: int = Path(gt=0)): # type: ignore
    todo = db.query(Todos).filter(Todos.id == id).first()
    
    if todo is not None:
        return todo

    raise HTTPException(status_code=404, detail="Todo not found")

@app.post('/todos', status_code=status.HTTP_201_CREATED)
async def save_todo(db: db_dependency, todo_request: TodoRequest): # type: ignore
   todo = todo_request.model_dump()
   todo_model = Todos(**todo)
   db.add(todo_model)
   db.commit()
   return todo

@app.put('/todos/{id}')
async def upate_todo( db: db_dependency, todo_request: TodoRequest, id: int = Path(gt=0)): # type: ignore 
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, delail="Todo not found")
    
    todo = todo_request.model_dump()
    
    todo_model.title = todo.get('title')
    todo_model.description = todo.get('description')
    todo_model.is_active = todo.get('is_active')
    todo_model.rating = todo.get('rating')
    
    db.add(todo_model)
    db.commit()
    
    return todo_model

@app.delete('/todos/{id}')
async def delete_todo(db: db_dependency, id: int = Path(gt=0)): # type: ignore
    todo = db.query(Todos).filter(Todos.id == id).first()
    
    if todo is None: 
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()
    
    return {}