from starlette.responses import RedirectResponse
from fastapi import APIRouter, Request, status, Path, Form
from fastapi.responses import HTMLResponse
from models import Todo
from .auth import get_current_user
from dependencies import templates, db_dependency
from typing import Annotated, Optional


router = APIRouter(
    prefix="/todos",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)


@router.get("/", response_class=HTMLResponse)
async def read_all_users_todo(request: Request, db: db_dependency):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todos = db.query(Todo).filter(Todo.owner_id == user.get("id")).all()
        return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(
        request: Request,
        db: db_dependency,
        title: Annotated[str, Form(...)],
        description: Optional[str] = Form(None)
    ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo_model = Todo()
        todo_model.title = title
        todo_model.description = description
        todo_model.owner_id = user.get("id")
        db.add(todo_model)
        db.commit()
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, db: db_dependency, todo_id: int = Path(gt=0)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(
        request: Request,
        db: db_dependency,
        title: Annotated[str, Form(...)],
        description: Optional[str] = Form(None),
        todo_id: int = Path(gt=0)
    ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
        todo_model.title = title
        todo_model.description = description
        db.add(todo_model)
        db.commit()
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, db: db_dependency, todo_id: int = Path(gt=0)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo_model = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == user.get("id")).first()
        if todo_model is None:
            return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        db.query(Todo).filter(Todo.id == todo_id).delete()
        db.commit()
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, db: db_dependency, todo_id: int = Path(gt=0)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        todo.status = not todo.status
        db.add(todo)
        db.commit()
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
