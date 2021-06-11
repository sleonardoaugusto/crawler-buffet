# Crawler Buffett

A stocks crawler application.

## How develop?

1. Clone this repo.
2. Create a virtualenv with Python >= 3.7.
3. Activate virtualenv.
4. Install dependencies.
5. Setup instance with .env.
6. Run tests.
7. Run server.

```console
git clone git@github.com:sleonardoaugusto/crawler-buffet.git
cd crawler-buffet
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
flask run
```

### Resources

```http://localhost:5000/stocks/Argentina/```
