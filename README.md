    Developed by Nay Oo Kyaw
    nayookyaw.nok@gmail.com

# how to activate env
if window, <br>
venv\Scripts\activate <br>

if linux <br>
source venv/bin/activate <br>

# install dependencies
pip install poetry <br>
poetry --version <br>
poetry install <br>

# how to run app
uvicorn main:app --reload <br>

# migration db (alembic)
alembic revision --autogenerate -m "xxx your comments" <br>

alembic upgrade head <br>
alembic downgrade -1 <br>

# Response bodies
1. Validation failed
{
    "status" : 422,
    "content" : {
        "errors": exc.errors(),
        "message": "Validation failed"
    }
}