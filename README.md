Simple Django OAuth app with GitHub authentication:

1. Clone the repository:

```bash
git clone https://github.com/82bits/simple_django_oauth2.git
cd simple_django_oauth2
```

2. Set up the development environment and install the requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.pip
```

3. Set up environment variables:
   Create an `.env` file in the project root, and add the following:

```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
SECRET_KEY=your_django_secret_key
```

4. Run the initial migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Access the app at `http://127.0.0.1:8000/`.
