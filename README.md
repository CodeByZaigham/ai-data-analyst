<p align="center"> <h1 align="center">🧠 AI Data Analyst — NL2SQL Intelligence Engine</h1> <p align="center"> Turning natural language into data-driven decisions — instantly </p> </p>

<p align="center"> <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi"> <img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql"> <img src="https://img.shields.io/badge/LLM-NL2SQL-orange?style=for-the-badge"> <img src="https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit"> <img src="https://img.shields.io/badge/Architecture-Production--Inspired-black?style=for-the-badge"> </p>



---

## 🚀 The Idea

Modern businesses sit on massive amounts of data — but extracting insights still requires **SQL expertise**.

> What if anyone could query a database like they talk to a human analyst?

This project answers that.

**AI Data Analyst** is an **end-to-end NL2SQL system** that converts plain English questions into executable SQL queries and returns real insights — instantly.

---

## 🎯 Impact & Value

- ✔️ **Eliminates SQL barrier** for non-technical users
- ✔️ **Reduces query time** from minutes → seconds
- ✔️ **Simulates real-world** AI-powered BI systems
- ✔️ **Demonstrates production-level** backend + AI integration

### 📊 What This Project Proves

- 🧠 You can design **LLM-powered data systems**
- ⚡ You understand **backend + AI orchestration**
- 🏗️ You can build **scalable, modular architectures**
- 📈 You can translate **business questions → technical queries**

---

## 🧠 How It Works

```text
User Question (Natural Language)
        ↓
Prompt Engineering + Schema Context
        ↓
LLM → SQL Query Generation
        ↓
SQL Execution (PostgreSQL)
        ↓
Structured JSON Response
        ↓
Frontend Visualization (Streamlit)
        ↓
Description and Analysis of that Data
        ↓
Download Data CSV
        ↓
Cached Query History

```
---

## 👨‍💻 Tech Stack

- Streamlit (Frontend)
- fastapi (backend)
- groq Llama 3.* (LLM)
- postgreSQL (database)

---

## ✨ Core Features

### 🧠 Intelligent NL2SQL Engine

- Converts plain English → optimized SQL
- Schema-aware prompt design (tables, columns, relationships)
- Handles joins, aggregations, filtering, sub-queries
- Returns both:
  - Generated SQL
  - Query results
        +
  - Visual Graph Representation
  - Downloadable CSV
  - Analysis of Data

### ⚡ Backend (FastAPI)

- High-performance REST API
- Clean modular architecture:
  - **AI Layer -> GROQ AI** (SQL generation + Data Analysis)
  - **Service Layer** (query execution + Graph visualization)
  - **Schema Layer** (validation)
- Pydantic v2 for strict data validation
- Structured responses:

```json
{
  "sqlquery": "...",
  "data": [...],
  "description":"..."
}
```

### 🗄️ Database (PostgreSQL)

- Relational schema with realistic datasets + Any Company Database can be used
- Supports:
  - Aggregations
  - Joins
  - Sorting & grouping
  - Sub-queries
  - Filtering
- Integrated via SQLAlchemy

### 📊 Frontend (Streamlit)

- Chat-like query interface
- Instant result visualization
- Table + analytics display
- Data in CSV foemat
- Analysis description
- Real-time interaction with backend API

---

## 🏗️ Architecture (Production Mindset)

```text
Frontend (Streamlit)
        ↓
FastAPI API Layer
        ↓
LLM (NL2SQL Engine)
        ↓
Query Execution Service
        ↓
PostgreSQL Database
        ↓
Data Analysis
        ↓
Data Visualization
```

---

## 📁 Project Structure

```text
ai-data-analyst/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── config.py
│   │   ├── schemas.py
│   │   ├── ai/
│   │   │   └── sql_generator.py
│   │   ├── services/
│   │   │   └── query_runner.py
│   └── .env
├── frontend/
│   └── streamlit.py
│
├── database/
│   └── schema.sql
│
├── LISENCE
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### 1️⃣ Clone Repo

```bash
git clone <your-repo-url>
cd ai-data-analyst
```

### 2️⃣ Setup Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

```env
DB_PATH=your_postgres_url
OPENAI_API_KEY=your_api_key
```

---

## ▶️ Run Project

### 🖥️ Backend

```bash
cd backend/app
uvicorn main:app --reload
```

- **API** → http://127.0.0.1:8000
- **Docs** → http://127.0.0.1:8000/docs

### 🎛️ Frontend

```bash
cd frontend
streamlit run streamlit.py
```

- **UI** → http://localhost:8501

---

## 📦 Example

**Input**

```json
{
  "question": "Top 5 customers by total spending"
}
```

**Output**

```json
{
  "sqlquery": "SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id ORDER BY total DESC LIMIT 5;",
  "data": [...]
}
```

---

## 📊 Demo Screenshots

###  SaaS Product

![Product Ready](/screenshots/SaaS%20product%20Poster.png)

###  Backend response

![fastapi docs](/screenshots/fastapi%20backend%20response.PNG)

###  Analyze Data

![Data Analysis](/screenshots/demo-1.PNG)

###  Data Table

![Database](/screenshots/demo-2.PNG)

###  Data Visualization

![Graph Plotting](/screenshots/demo-3.PNG)

###  SQL Query

![Raw SQL](/screenshots/demo-4.PNG)

### 🗑️ Safety-Checl

![Safety](/screenshots/query-safe-check.PNG)
---

## 🧠 Engineering Highlights

- 🔥 Designed a **schema-aware prompting system**
- ⚡ Built a complete **NL → SQL → Execution pipeline**
- 🧩 Clean **separation of concerns** (AI / DB / API / UI)
- 🧠 Integrated an **LLM into a real backend workflow**
- 📊 Built a **full-stack system** (API + UI + DB)
- ❗ Solved real issues:
  - Response serialization bugs
  - SQL execution handling
  - API schema validation
  - Query History Caching
  - JSON to Object Mapping

---

## ⚠️ Limitations

- LLM may generate imperfect SQL
- No authentication tokens

---

## 🚀 Future Improvements

- 🔐 Authentication (JWT)
- 📊 Advanced dashboards (charts, BI-style UI)
- 🐳 Dockerization
- ☁️ Deployment (AWS / Render / Railway)
- 🔗 LangChain / RAG integration

---

## 🧑‍💻 About the Developer

**CodeByZaigham**

Aspiring **AI/ML Engineer / Data Systems Builder** focused on:

- LLM-powered applications
- Backend engineering (FastAPI)
- Data-driven systems
- Automating Workflows
- solving Real World problems by integrating AI

---

## 🌟 Why This Project Stands Out

This is not just another CRUD app.

It demonstrates:

- ✔️ **AI + Backend integration**
- ✔️ **Real-world system design thinking**
- ✔️ **Understanding of data pipelines**
- ✔️ Ability to build **intelligent developer tools**
- ✔️ **Reducing the Need of manual SQL**
- ✔️ **Automating Data Analytics Tasks**
- ✔️ **Can be used on any company's Database**

---

## 📄 License

Built for **learning, experimentation, and portfolio showcase**.