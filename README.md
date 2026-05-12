# Vendify

Vendify is an API first platform that brings resources to manage sales.

## Instalation

### Requirements

* Docker/Podman
* Git 2.3+
* Python 3.11+ 

### 1. Clone repository

```bash
git clone https://github.com/mobml/Vendify
cd vendify
```

### 2. Create a virtual environment & activate it(optional)

```bash
python -m venv venv
source venv/bin/activate

```
### 3. Install depencencies

```bash
pip install -r requirements.txt
```

### 4. Config .env 

Create an .env file in the root directory.
```env
MYSQL_ROOT_PASSWORD=your-root-password
MYSQL_PASSWORD=your-db-user-password
MYSQL_DATABASE=db-name
MYSQL_USER=user-db-name
MYSQL_PORT=3306
DB_HOST=localhost
```

### 5. Run

#### Database container

```bash
docker compose up --build
# or
podman compose up -d
```

#### App server (develop mode)

```bash
python manage.py migrations
python manage.py createsuperuser
python manage.py runserver
```

### 6. Access

```
http://127.0.0.1:8000
```

## API

Base URL:

```
/api/v1
```

Endpoints:

| Method | Endpoint          | Description        |
|--------|-------------------|--------------------|
|GET     |`/products`        |Get a list od products|
|POST    |`/sales`           |Make a sale         |
|POST    |`/sales/:id`       |Cancel a sale       |
|GET     |`/sales/:id/ticket`|Get a ticket      |
