from datetime import date
from urllib.parse import quote

from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from .auth import authenticate_user, create_access_token, get_user_from_token, hash_password
from .database import Base, engine, get_db
from .excel import import_gastos_from_file
from .models import Gasto, Usuario

ORCAMENTO_MENSAL = 1_000_000

app = FastAPI(title="Plataforma de Inteligencia Municipal")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def create_demo_users(db: Session) -> None:
    if db.query(Usuario).count():
        return

    users = [
        Usuario(
            nome="Prefeito Demo",
            email="prefeito@demo.com",
            senha=hash_password("123456"),
            cargo="prefeito",
            secretaria="Todas",
        ),
        Usuario(
            nome="Secretaria Saude",
            email="saude@demo.com",
            senha=hash_password("123456"),
            cargo="secretario",
            secretaria="Saude",
        ),
    ]
    db.add_all(users)
    db.commit()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        create_demo_users(db)
    finally:
        db.close()


def current_user(request: Request, db: Session = Depends(get_db)) -> Usuario | None:
    return get_user_from_token(db, request.cookies.get("access_token"))


def require_user(user: Usuario | None) -> Usuario | RedirectResponse:
    if not user:
        return RedirectResponse("/login", status_code=303)
    return user


def visible_gastos_query(db: Session, user: Usuario):
    query = db.query(Gasto)
    if user.cargo != "prefeito":
        query = query.filter(Gasto.secretaria == user.secretaria)
    return query


@app.get("/", include_in_schema=False)
def index() -> RedirectResponse:
    return RedirectResponse("/dashboard", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str | None = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/login")
def login(
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, email, senha)
    if not user:
        return RedirectResponse("/login?error=Email%20ou%20senha%20invalidos", status_code=303)

    token = create_access_token(user)
    redirect = RedirectResponse("/dashboard", status_code=303)
    redirect.set_cookie("access_token", token, httponly=True, samesite="lax")
    return redirect


@app.get("/logout")
def logout():
    redirect = RedirectResponse("/login", status_code=303)
    redirect.delete_cookie("access_token")
    return redirect


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: Usuario | None = Depends(current_user),
    db: Session = Depends(get_db),
    message: str | None = None,
    error: str | None = None,
):
    user_or_redirect = require_user(user)
    if isinstance(user_or_redirect, RedirectResponse):
        return user_or_redirect

    today = date.today()
    query = visible_gastos_query(db, user)
    month_query = query.filter(extract("month", Gasto.data) == today.month, extract("year", Gasto.data) == today.year)

    total_mes = month_query.with_entities(func.coalesce(func.sum(Gasto.valor), 0)).scalar()
    restante = ORCAMENTO_MENSAL - total_mes
    percentual = (total_mes / ORCAMENTO_MENSAL) * 100 if ORCAMENTO_MENSAL else 0

    por_secretaria = query.with_entities(Gasto.secretaria, func.sum(Gasto.valor)).group_by(Gasto.secretaria).all()
    por_categoria = query.with_entities(Gasto.categoria, func.sum(Gasto.valor)).group_by(Gasto.categoria).all()
    ultimos = query.order_by(Gasto.data.desc(), Gasto.id.desc()).limit(8).all()

    maior_secretaria = max(por_secretaria, key=lambda item: item[1], default=("-", 0))[0]
    alerta = "vermelho" if percentual >= 100 else "amarelo" if percentual >= 80 else "ok"

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "message": message,
            "error": error,
            "total_mes": total_mes,
            "restante": restante,
            "percentual": percentual,
            "maior_secretaria": maior_secretaria,
            "alerta": alerta,
            "por_secretaria": dict(por_secretaria),
            "por_categoria": dict(por_categoria),
            "ultimos": ultimos,
        },
    )


@app.post("/upload")
async def upload_file(
    arquivo: UploadFile = File(...),
    user: Usuario | None = Depends(current_user),
    db: Session = Depends(get_db),
):
    user_or_redirect = require_user(user)
    if isinstance(user_or_redirect, RedirectResponse):
        return user_or_redirect

    filename = arquivo.filename or ""
    if not filename.lower().endswith((".xlsx", ".csv")):
        return RedirectResponse("/dashboard?error=Envie%20um%20arquivo%20.xlsx%20ou%20.csv", status_code=303)

    try:
        count = import_gastos_from_file(db, await arquivo.read(), filename)
    except ValueError as exc:
        return RedirectResponse(f"/dashboard?error={quote(str(exc))}", status_code=303)

    return RedirectResponse(f"/dashboard?message={count}%20gastos%20importados", status_code=303)


@app.get("/gastos", response_class=HTMLResponse)
def gastos(
    request: Request,
    secretaria: str | None = None,
    categoria: str | None = None,
    data: str | None = None,
    user: Usuario | None = Depends(current_user),
    db: Session = Depends(get_db),
):
    user_or_redirect = require_user(user)
    if isinstance(user_or_redirect, RedirectResponse):
        return user_or_redirect

    query = visible_gastos_query(db, user)
    if secretaria and user.cargo == "prefeito":
        query = query.filter(Gasto.secretaria == secretaria)
    if categoria:
        query = query.filter(Gasto.categoria == categoria)
    if data:
        try:
            query = query.filter(Gasto.data == date.fromisoformat(data))
        except ValueError:
            pass

    registros = query.order_by(Gasto.data.desc(), Gasto.id.desc()).all()
    all_visible = visible_gastos_query(db, user).all()
    secretarias = sorted({g.secretaria for g in all_visible})
    categorias = sorted({g.categoria for g in all_visible})

    return templates.TemplateResponse(
        "gastos.html",
        {
            "request": request,
            "user": user,
            "registros": registros,
            "secretarias": secretarias,
            "categorias": categorias,
            "filters": {"secretaria": secretaria or "", "categoria": categoria or "", "data": data or ""},
        },
    )
