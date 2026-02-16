from fastapi import Request
from fastapi.templating import Jinja2Templates
from datetime import datetime, date

templates = Jinja2Templates(directory="templates")


def _deadline_badge(deadline):
    if not deadline:
        return ""
    days = (deadline - date.today()).days
    if days < 0:
        return '<span class="badge badge-closed">마감</span>'
    if days <= 7:
        return f'<span class="badge badge-urgent">D-{days}</span>'
    if days <= 30:
        return f'<span class="badge badge-soon">D-{days}</span>'
    return f'<span class="badge badge-normal">D-{days}</span>'


templates.env.globals["deadline_badge"] = _deadline_badge


def common_context(request: Request) -> dict:
    return {
        "request": request,
        "year": datetime.now().year,
    }
