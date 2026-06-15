# Monthly Expense Manager

A full-stack expense tracking application built using:

* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Groq LLM API

---

## Features

### Categories

* Create categories
* List categories

### Expenses

* Add expenses
* Update expenses
* Delete expenses
* Filter expenses by month
* Filter expenses by year
* Filter expenses by category

### Summaries

* Monthly spending summary
* Category-wise spending summary

### Budgets

* Set category budgets
* Budget alerts when spending exceeds limits

### AI Insights

* Analyze spending patterns
* Detect overspending
* Generate savings recommendations
* Personalized financial advice using Groq

---

## Project Structure

expense-manager/

app/

* main.py
* models.py
* database.py
* db_models.py
* crud.py
* llm.py
* prompts.py
* budget.py

docker-compose.yml

Dockerfile

requirements.txt

README.md

.env

---

## Setup

### Clone Repository

```bash
git clone <repo-url>

cd expense-manager
```

### Create Environment File

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key

DATABASE_URL=postgresql://postgres:password@db:5432/expensedb

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=expensedb
```

---

## Run Application

Build and start containers:

```bash
docker-compose up --build
```

Open Swagger Docs:

```text
http://localhost:8000/docs
```

---

## Stop Containers

```bash
docker-compose down
```

---

## Remove Containers and Database

```bash
docker-compose down -v
```

---

## API Endpoints

### Health

```http
GET /health
```

### Categories

```http
POST /categories
GET /categories
```

### Expenses

```http
POST /expenses
GET /expenses
GET /expenses/{id}
PUT /expenses/{id}
DELETE /expenses/{id}
```

### Summaries

```http
GET /summary/monthly
GET /summary/categories
```

### Budget

```http
POST /budget
GET /budget/alerts
```

### AI Insights

```http
POST /insights
```

---

## Team Ownership

### Intern 1

* main.py
* models.py

### Intern 2

* database.py
* db_models.py
* crud.py

### Intern 3

* llm.py
* prompts.py
* budget.py

---

## Run Verification

After startup verify:

```http
GET /health
```

Expected:

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

---

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Groq LLM
* Pydantic
