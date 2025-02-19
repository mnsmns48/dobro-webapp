from datetime import datetime
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from config import dobro_engine
from crud import main_menu, walking_menu

dobrotsen_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@dobrotsen_router.get("/", response_model=None)
async def get_main(
        request: Request,
        session: AsyncSession = Depends(dobro_engine.session_dependency)
):
    data = await main_menu(session=session, parent=0)
    context = {'request': request, 'data': data.get('data'), 'date': datetime.now().strftime("%d.%m.%Y")}
    return templates.TemplateResponse(
        name="menu.html",
        context=context
    )


@dobrotsen_router.get("/{parent}")
async def get_page_parent(
        parent: int,
        request: Request,
        session: AsyncSession = Depends(dobro_engine.session_dependency),

):
    data = await walking_menu(session=session, parent=parent)
    if data.get('end'):
        context = {"request": request,
                   "data": data.get('data'),
                   "parent": data.get('parent'),
                   'date': datetime.now().strftime("%d.%m.%Y")}
        return templates.TemplateResponse(name="products.html", context=context)
    else:
        if data.get('data'):
            context = {"request": request,
                       "data": data.get('data'),
                       "parent": data.get('parent'),
                       'date': datetime.now().strftime("%d.%m.%Y")}
            return templates.TemplateResponse(name="menu.html", context=context)
        else:
            context = {"request": request}
            return templates.TemplateResponse(name="none.html", context=context)
