# Quiz Backend Management API

A production-grade, modular RESTful backend service built using **FastAPI**, **SQLAlchemy ORM**, **Pydantic**, and **SQLite**. 

This system manages quiz questions and multiple-choice options while enforcing relational database logic, cascading deletions, runtime schema constraints, and specific application business rules. The seeded question bank is tailored to the **Celebal Technologies Python & AI/ML Internship** learning curriculum.

---

## Features

- **REST CRUD API**: Clean, paginated endpoints for Questions and Choices with strict input sanitization (using Pydantic v2 `StringConstraints` to trim inputs and prevent whitespace-only values).
- **Business Constraint Enforcement**: Cascades deletions, prevents duplicate choice text (case-insensitive & trimmed), restricts questions to at most one correct choice, and enforces strict logical checks for True/False structures.
- **Shuffled Quiz Engine**: Starts unique quiz attempts on-the-fly, locks randomly selected questions dynamically, supports scoring with negative marking (-0.25 pt penalty per wrong answer), and returns question reviews showing choices, user selections, and correctness.
- **Analytics & Leaderboard**: Provides aggregated summary metrics, lists leaderboard attempts with deterministic tie-breakers (scores, correct counts, elapsed duration), and logs hardest questions by tracking incorrect submissions.
- **Interactive UI & Documentation**: Features a beautiful, dark-themed Single Page Application (SPA) frontend at `/ui` and auto-generated interactive documentation at `/docs`.

---

## Project Preview

### Interactive Quiz Interface

A responsive, self-contained quiz interface for selecting quiz parameters, taking quizzes, viewing scores, and reviewing answers.

![Interactive Quiz Interface](assets/quiz-ui.png)

### FastAPI Swagger Documentation

Interactive Swagger documentation for testing and exploring the complete REST API endpoints.

![FastAPI Swagger Documentation](assets/api-docs.png)

---

## Directory Structure

```text
quiz_api/
│
├── assets/
│   ├── quiz-ui.png       # Interactive Quiz UI screenshot
│   └── api-docs.png      # Swagger API docs screenshot
├── config.py             # App Configuration (database URL, app metadata)
├── database.py           # SQLAlchemy engine local session setup, SQLite connection listener
├── models.py             # SQLAlchemy ORM models (Question, Choice, QuizAttempt, QuizAttemptQuestion, AttemptAnswer)
├── schemas.py            # Pydantic v2 validation models, pagination response, and Quiz views
├── crud.py               # Database interaction and business-rule service layer
├── main.py               # Application entry point, router inclusion, log middleware, health checks
├── seed.py               # Seeding script populating 29 Celebal curriculum questions
├── requirements.txt      # Python dependencies manifest
├── test_main.py          # Pytest automation suite
├── static/
│   └── index.html        # Interactive Single Page Application Frontend
└── README.md             # Project documentation (this file)
```

---

## Tech Stack

| Technology | Purpose |
|:---|:---|
| **FastAPI** | High-performance, modern Python web framework for REST APIs. |
| **SQLAlchemy** | SQL Toolkit and Object-Relational Mapper (ORM) to handle DB operations. |
| **Pydantic v2** | Runtime data validation and serialization checking. |
| **SQLite** | Lightweight disk-based relational database. |
| **Uvicorn** | Fast ASGI server to run the FastAPI app. |
| **Pytest** | Automated unit testing framework. |

---

## Database Architecture

A relational structure is mapped between `questions`, `choices`, `quiz_attempts`, `quiz_attempt_questions`, and `attempt_answers` tables. SQLite connection parameters enforce referential safety constraints.

```text
   ┌─────────────────────────────────┐
   │           questions             │
   ├─────────────────────────────────┤
   │ [PK] id            : Integer    │
   │      question_text : String     │
   │      category      : String(opt)│
   │      difficulty    : String(opt)│
   │      question_type : String     │
   └─────────────┬─────────────┬─────┘
                 │             │
                 │             │ (Locks question list)
                 ▼             ▼ 
   ┌─────────────┴───┐   ┌─────┴──────────────────────────┐
   │     choices     │   │     quiz_attempt_questions     │
   ├─────────────────┤   ├────────────────────────────────┤
   │ [PK] id         │   │ [PK] id                        │
   │      choice_text│   │ [FK] attempt_id  : QuizAttempt │
   │      is_correct │   │ [FK] question_id : Question    │
   │ [FK] question_id│   └─────────────▲──────────────────┘
   └─────────────────┘                 │
                                       │ (1 Attempt owns Many Questions)
                                       │
   ┌───────────────────────────────────┴─┐
   │            quiz_attempts            │
   ├─────────────────────────────────────┤
   │ [PK] id                : Integer    │
   │      started_at        : String     │
   │      completed_at      : String(opt)│
   │      score             : Float(opt) │
   │      total_questions   : Integer    │
   │      correct_count     : Integer    │
   │      incorrect_count   : Integer    │
   │      skipped_count     : Integer    │
   │      category_filter   : String(opt)│
   │      difficulty_filter : String(opt)│
   │      is_completed      : Boolean    │
   └───────────────────┬─────────────────┘
                       │
                       │ (1 Attempt has Many Answers)
                       ▼ (Cascade Delete)
   ┌─────────────────────────────────────┐
   │           attempt_answers           │
   ├─────────────────────────────────────┤
   │ [PK] id                : Integer    │
   │ [FK] attempt_id        : Integer    │
   │ [FK] question_id       : Integer    │
   │ [FK] choice_id         : Integer    │
   │      is_correct        : Boolean    │
   │      marks_awarded     : Float      │
   └─────────────────────────────────────┘
```

---

## Quick Start & Installation (Step-by-Step)

Follow these steps to set up and run the project locally on Windows:

### 1. Open Terminal and Navigate to Project Folder
Open PowerShell or Command Prompt and run:
```powershell
cd e:\celebal-internship-project
```

### 2. Create the Virtual Environment
Create a clean virtual environment using the built-in python module:
```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment
Activate the environment to sandbox dependencies.
* **PowerShell**:
  ```powershell
  venv\Scripts\Activate.ps1
  ```
* **Command Prompt**:
  ```cmd
  venv\Scripts\activate.bat
  ```

*(Note: If Windows Script Execution Policy restricts activation, you can skip activation and prefix python/pip commands with `venv\Scripts\` e.g. `venv\Scripts\python -m ...`)*

### 4. Install Dependencies
Always use `python -m pip` to target the active virtual environment python interpreter reliably:
```powershell
python -m pip install -r requirements.txt
```

### 5. Seed the Database
Run the seeding script. It checks your existing database, performs lightweight column migrations if you have an older schema, and inserts the 29 curated question structures:
```powershell
python seed.py
```

### 6. Launch the API Server
Start the Uvicorn ASGI dev server as a python executable module. This bypasses PATH lookup lookup errors:
```powershell
python -m uvicorn main:app --reload
```
The console logs will confirm:
`Uvicorn running on http://127.0.0.1:8000`

---

## Running the Application

1. **API Interactive Documentation**: Visit **`http://127.0.0.1:8000/docs`** to view and test all REST routes. The Quiz UI link is also located inside the header description.
2. **Interactive Quiz Interface**: Visit **`http://127.0.0.1:8000/ui`** in your browser. This displays the single-page application where you can customize categories, select difficulties, answer questions, submit results, and view a detailed review.

---

## Verification & Testing

To run the automated test suite (isolated database tests covering system health, question limits, negative scores, and analytics):
```powershell
python -m pytest test_main.py -v
```

---

## API Reference

### System Endpoints
- **`GET /`**: Redirects to interactive documentation (`/docs`).
- **`GET /health`**: Returns system health status.
- **`GET /ui`**: Redirects to interactive HTML frontend.

### Question Management (`/questions`)

| Method | Endpoint | Description | Success Code | Errors |
|:---|:---|:---|:---|:---|
| **POST** | `/questions` | Create a new question. | `201 Created` | `422 Unprocessable` |
| **GET** | `/questions` | List questions (paginated and filtered). | `200 OK` | - |
| **GET** | `/questions/random`| Retrieve random set of questions. | `200 OK` | - |
| **GET** | `/questions/{id}` | Get a question and its choices by ID. | `200 OK` | `404 Not Found` |
| **PUT** | `/questions/{id}` | Update question text or category. | `200 OK` | `404`, `422` |
| **DELETE**| `/questions/{id}` | Delete a question (cascades choices). | `204 No Content`| `404` |
| **GET** | `/questions/{id}/quiz` | Get shuffled question with hidden correct answers. | `200 OK` | `404` |

### Choice Management (`/choices`)

| Method | Endpoint | Description | Success Code | Errors |
|:---|:---|:---|:---|:---|
| **POST** | `/choices` | Add a choice to a question. | `201 Created` | `400 Bad Request`, `404`, `422` |
| **GET** | `/choices` | List choices (optional filter: `?question_id=x`). | `200 OK` | - |
| **PUT** | `/choices/{id}` | Update choice text or correctness flag. | `200 OK` | `400`, `404`, `422` |
| **DELETE**| `/choices/{id}` | Delete a single choice. | `204 No Content`| `404` |

### Quiz Session

| Method | Endpoint | Description | Success Code | Errors |
|:---|:---|:---|:---|:---|
| **POST** | `/quiz/start` | Creates a new attempt with questions locked. | `201 Created` | `404 Not Found` |
| **POST** | `/quiz/{id}/submit`| Submit answers and score the attempt. | `200 OK` | `400`, `404` |
| **GET** | `/quiz/{id}/review`| Fetch detailed question by question feedback. | `200 OK` | `400`, `404` |

### Analytics

| Method | Endpoint | Description | Success Code | Errors |
|:---|:---|:---|:---|:---|
| **GET** | `/analytics/summary` | Get aggregated metadata on current question bank. | `200 OK` | - |
| **GET** | `/analytics/leaderboard` | View deterministically sorted top scores. | `200 OK` | - |
| **GET** | `/analytics/hardest-questions` | Group incorrect responses by question. | `200 OK` | - |

---

## Future Enhancements

- **User Authentication & Role-Based Access Control (RBAC)**: Integrate JWT token-based authentication to distinguish admin users (authorized to modify questions/choices) from standard students (authorized only to take quizzes).
- **AI-Powered Question Generation**: Leverage LLMs (like Google Gemini) to dynamically generate fresh questions, choices, and detailed explanations based on selected categories and difficulty parameters.
- **Real-Time Multiplayer Duels**: Utilize WebSockets to support real-time shared quiz rooms where multiple users answer the same set of questions under a synchronized countdown timer.
- **Detailed Analytics per Question**: Track response latency for each individual question to report where users are spending the most time and highlight target learning paths.
- **Rich Media & Code Highlighting**: Expand choice rendering to support code syntax highlighting (Prism.js) and embedded diagram files (Mermaid.js) within question cards.
