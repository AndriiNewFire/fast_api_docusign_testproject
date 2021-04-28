from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

addition_router = APIRouter()
templates = Jinja2Templates('templates')


@addition_router.get("/addition")
def addition_page_get(request: Request):
    return templates.TemplateResponse('addition.html', {'request': request},)


@addition_router.post('/addition')
def addition_page_post(request: Request, num: int = Form(...)):
    result = num ** num
    return templates.TemplateResponse('addition.html', context={
                                                                'request': request,
                                                                'result': result,
                                                                })
