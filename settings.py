import time, datetime
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, RedirectResponse
from routers import auth, todos
from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    with open('server_time_log.log', 'a') as log:
        log.write(f'server started at {datetime.datetime.now()} \n')
    
    yield

    with open('server_time_log.log', 'a') as log:
        log.write(f'server shutdowned at {datetime.datetime.now()} \n')


app = FastAPI(lifespan=lifespan)
app.include_router(todos.router, tags=['Todos'])
app.include_router(auth.router, tags=['Authentication and Authorization'])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
def main ():
    return RedirectResponse(url="/todos/", status_code=status.HTTP_302_FOUND)

@app.middleware('http')
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response
