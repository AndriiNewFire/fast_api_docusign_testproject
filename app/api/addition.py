from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates('./app/addition/templates')


@router.get("/addition")
def addition_page_get(request: Request):
    return templates.TemplateResponse('addition.html', {'request': request},)


@router.post('/addition')
def addition_page_post(request: Request, num: int = Form(...)):
    result = num ** num
    return templates.TemplateResponse('addition.html', context={
                                                                'request': request,
                                                                'result': result,
                                                                })
