from fastapi import Request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.templating import Jinja2Templates


router = InferringRouter()
templates = Jinja2Templates('templates/user_management')


@cbv(router)
class UserAndDocumentsManagement:

    @router.get("/")
    def homepage_endpoint(self, request: Request):
        return templates.TemplateResponse('home.html', {'request': request},)

    @router.get("/register")
    def register_new_user_account_endpoint(self, request: Request):
        return templates.TemplateResponse('register.html', {'request': request}, )

    @router.get("/login")
    def login_user_to_the_system_endpoint(self, request: Request):
        return templates.TemplateResponse('login.html', {'request': request}, )
