# 🧠 AIVOA Customer Complaint Copilot

### AI-Powered Pharmaceutical Customer Complaint Management System

An AI-powered customer complaint management platform designed for pharmaceutical manufacturing workflows.

The application helps users **capture, extract, assess, manage, and update customer complaints** using AI. Users can provide complaint information through text or documents, after which the system extracts structured complaint data, generates an AI-based risk assessment, and allows users to interact with complaints through an AI Copilot.

<p align="center">
  <a href="https://aivoa-copilot.vercel.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-AIVOA%20Copilot-black?style=for-the-badge" />
  </a>
</p>

---

## ✨ Features

### 🤖 AI Complaint Extraction

Convert unstructured customer complaints into structured complaint records.

The AI extracts information such as:

* Product Name
* Product Strength / Grade
* Batch / Lot Number
* Manufacturing Date
* Expiry Date
* Reporter / Customer Information
* Affected Quantity
* Problem Description

---

### ⚠️ AI Risk Assessment

The system automatically analyzes the complaint and provides:

* **Severity Level**

  * 🔴 Critical
  * 🟠 Major
  * 🟢 Minor
* Suggested Action
* AI-generated Reasoning

---

### 💬 AI Copilot

Users can interact with an existing complaint using natural-language instructions.

For example:

```text
Change the affected quantity to 50.
```

The AI processes the instruction and updates the relevant complaint information while preserving the remaining complaint data.

---

### 📄 Complaint Document Processing

Users can provide complaint information through uploaded documents.

The workflow is:

```text
Customer Complaint / Document
            ↓
       Text Extraction
            ↓
       AI Processing
            ↓
   Structured Complaint
            ↓
    AI Risk Assessment
            ↓
     Complaint Form
```

---

### 📋 Complaint Management

Users can:

* Create complaints
* View complaints
* Update complaints
* Delete complaints
* View complaint details
* Track complaint status
* Review AI risk assessments

---

### 🔐 Authentication

The application includes authentication and protected backend APIs.

Users can register, log in, and access their complaint management workspace.

---

### 📝 Audit Logging

Important complaint-related operations are recorded through audit logs to maintain traceability of changes.

---

# 🖥️ Application Screenshots

## 📊 Dashboard

<p align="center">
  <img src="screenshot/dashboard.png" width="90%" alt="AIVOA Customer Complaint Copilot Dashboard"/>
</p>

---

## 🔐 Login

<p align="center">
  <img src="screenshot/login.png" width="90%" alt="AIVOA Customer Complaint Copilot Login"/>
</p>

---

## 📋 Complaint Management

<p align="center">
  <img src="screenshot/complaint.png" width="90%" alt="AIVOA Customer Complaint Copilot Complaint Page"/>
</p>

---

# 🧪 Sample Customer Complaint

The following sample complaint can be used to test the **AI complaint extraction and risk assessment workflow**.

Users can copy the complete text below and paste it into the application or save it as a document and upload it.

## Sample Input

```text
CUSTOMER COMPLAINT — TEST DOCUMENT

Complaint source: Customer Email

Complaint date: September 14, 2026

Customer name: Green Valley Health Supplies Ltd.

# Product Information

Product name: AIVOA Sterile Saline Solution

Product strength/grade: 0.9% Sodium Chloride, USP

Batch/Lot number: SV-26-0815-B17

Manufacturing date: August 15, 2026

Expiry date: August 14, 2028

Quantity affected: 240 kg

# Complaint Details

Complaint type: Product quality / packaging

The customer reported that several units from the above
batch arrived with loose outer seals and visible leakage inside the shipping
carton. The customer received the shipment on September 12, 2026 and identified
the issue during incoming inspection. Approximately 18 units appeared affected.
The customer has placed the affected material on hold and requested
investigation and replacement.

# Initial Assessment

Initial severity: Major — the complaint involves potential
package integrity failure and possible product contamination.

Suggested priority: High — customer has quarantined affected
material and requested prompt investigation.

# Additional Information

Photos of the damaged packaging are available from the
customer. No adverse event or patient injury has been reported. The customer
states that the remaining units from the shipment are being inspected.

TEST PURPOSE: This document is intentionally structured so an AI complaint extraction system can identify customer, product, batch, dates, quantity, complaint type, description, severity, and priority.
```

## Expected Extraction

When this complaint is processed, the system is designed to identify information such as:

| Field                    | Sample Value                          |
| ------------------------ | ------------------------------------- |
| Product Name             | AIVOA Sterile Saline Solution         |
| Product Strength / Grade | 0.9% Sodium Chloride, USP             |
| Batch / Lot Number       | SV-26-0815-B17                        |
| Manufacturing Date       | August 15, 2026                       |
| Expiry Date              | August 14, 2028                       |
| Reporter / Customer      | Green Valley Health Supplies Ltd.     |
| Affected Quantity        | 240 kg                                |
| Complaint Type           | Product quality / packaging           |
| Problem                  | Loose outer seals and visible leakage |
| Initial Severity         | Major                                 |
| Suggested Priority       | High                                  |

The application then generates a structured complaint record and an AI-based risk assessment that the user can review.

> **Note:** The AI output may vary slightly depending on the model response. The sample values above represent the information explicitly provided in the test complaint.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────────┐
                         │       React Frontend      │
                         │                          │
                         │  Dashboard               │
                         │  Complaint Form          │
                         │  AI Copilot              │
                         │  Document Upload         │
                         │  Authentication          │
                         └────────────┬─────────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌──────────────────────────┐
                         │       FastAPI Backend    │
                         │                          │
                         │  Authentication          │
                         │  Complaint APIs          │
                         │  Chat APIs               │
                         │  Document APIs           │
                         │  Audit APIs               │
                         └────────────┬─────────────┘
                                      │
                     ┌────────────────┼────────────────┐
                     │                │                │
                     ▼                ▼                ▼
              ┌────────────┐   ┌────────────┐   ┌────────────┐
              │ AI Service │   │ PostgreSQL │   │   Storage  │
              │            │   │            │   │            │
              │ Extraction │   │ Users      │   │ Documents  │
              │ Assessment │   │ Complaints │   │ Uploads    │
              │ AI Editing │   │ Risk Data  │   │            │
              └────────────┘   │ Audit Logs │   └────────────┘
                               └────────────┘
```

---

# 🔄 Application Workflow

```text
┌──────────────────┐
│      User        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ React Frontend   │
│                  │
│ Text / Document  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ FastAPI Backend  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   AI Service     │
│                  │
│ Extract + Assess │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Pydantic         │
│ Validation       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ PostgreSQL       │
│                  │
│ Persist Data     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Complaint Form   │
│ + Risk Analysis  │
└──────────────────┘
```

---

# 🛠️ Tech Stack

## Frontend

<p>
  <img src="https://skillicons.dev/icons?i=react,js,vite,css,html" />
</p>

* React
* JavaScript
* Vite
* CSS
* REST API Integration

## Backend

<p>
  <img src="https://skillicons.dev/icons?i=python,fastapi" />
</p>

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* JWT Authentication

## Database

<p>
  <img src="https://skillicons.dev/icons?i=postgres" />
</p>

* PostgreSQL
* SQLAlchemy ORM
* Database migrations

## AI

<p>
  <img src="https://skillicons.dev/icons?i=python" />
</p>

* Google Gemini API
* Structured AI responses
* Pydantic response validation
* AI-based complaint extraction
* AI-based risk assessment
* Natural-language complaint editing

## Development Tools

<p>
  <img src="https://skillicons.dev/icons?i=git,github,vscode" />
</p>

* Git
* GitHub
* Visual Studio Code
* REST APIs

---

# 📁 Project Structure

```text
AIVOA-Customer-Complaint-Copilot/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── complaints.py
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   └── audit.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── complaint.py
│   │   │   ├── document.py
│   │   │   └── audit.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── complaint.py
│   │   │   ├── chat.py
│   │   │   ├── document.py
│   │   │   └── audit.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── complaint_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── document_service.py
│   │   │   └── audit_service.py
│   │   │
│   │   └── utils/
│   │       └── text_extractor.py
│   │
│   ├── uploads/
│   ├── migrations/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   ├── complaint/
│   │   │   ├── copilot/
│   │   │   ├── dashboard/
│   │   │   └── audit/
│   │   │
│   │   ├── pages/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── api/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── screenshots/
│   ├── dashboard.png
│   ├── login.png
│   └── complaint.png
│
├── README.md
└── .gitignore
```

---

# 🔌 API Overview

## Authentication

```http
POST /api/auth/register
POST /api/auth/login
```

## Complaints

```http
GET    /api/complaints
POST   /api/complaints
GET    /api/complaints/{complaint_id}
PUT    /api/complaints/{complaint_id}
DELETE /api/complaints/{complaint_id}
```

## AI Copilot

```http
POST /api/chat/log
POST /api/chat/edit
```

## Documents

```http
POST /api/documents/upload
```

## Audit

```http
GET /api/audit/...
```

---

# 🚀 Running Locally

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AIVOA-Customer-Complaint-Copilot
```

## 2. Backend Setup

```bash
cd backend

python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=your_google_model
FRONTEND_URL=http://127.0.0.1:5173/
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://127.0.0.1:5173
```

---

# 🔐 Environment Variables

Never commit API keys or database credentials to GitHub.

Example:

```env
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secure-secret-key
GOOGLE_API_KEY=your-google-api-key
GOOGLE_MODEL=your-google-model
FRONTEND_URL=http://127.0.0.1:5173/
```

A `.env.example` file is provided for reference.

---

# 🎯 Use Case

This project demonstrates how AI can assist pharmaceutical complaint-management workflows by reducing manual data entry and helping users organize and assess unstructured customer complaints.

The architecture is modular and can be extended for larger Quality Management System (QMS) workflows.

---

# 🔒 Security

The application includes several security-oriented practices:

* JWT-based authentication
* Protected API endpoints
* Environment-based secret management
* Pydantic input validation
* Structured AI response validation
* User-specific complaint access
* Audit logging
* Customer content treated as untrusted input

---

# 🚧 Future Improvements

The current architecture can be extended with additional AI-powered QMS capabilities:

* 🔄 LangGraph-based multi-step AI workflows
* ⚡ Alternative LLM providers such as Groq
* ✅ Complaint completeness checker
* 🔍 Duplicate complaint detection
* 🧪 Root-cause recommendation
* 📑 CAPA recommendation
* 📝 Automatic complaint summarization
* 🖼️ Advanced OCR for scanned documents
* 👥 Role-based access control
* 📊 Advanced analytics dashboard
* 🔗 Integration with enterprise QMS systems

---

# 📌 Project Highlights

| Capability                | Implementation |
| ------------------------- | -------------- |
| AI Complaint Extraction   | ✅              |
| Structured Complaint Form | ✅              |
| AI Risk Assessment        | ✅              |
| Natural Language Editing  | ✅              |
| Document Upload           | ✅              |
| Authentication            | ✅              |
| PostgreSQL Persistence    | ✅              |
| Audit Logging             | ✅              |
| REST APIs                 | ✅              |
| React Frontend            | ✅              |
| FastAPI Backend           | ✅              |
| Pydantic Validation       | ✅              |

---

# 🌐 Live Application

<p align="center">

### 🚀 Try the Application

<a href="https://aivoa-copilot.vercel.app/">
  <img src="https://img.shields.io/badge/OPEN%20LIVE%20APP-AIVOA%20COPILOT-000000?style=for-the-badge&logo=vercel&logoColor=white" />
</a>

</p>

**Live Demo:** https://aivoa-copilot.vercel.app/

---

# 👨‍💻 Author

## Omjee Singh

Computer Science & Engineering Student
Machine Learning & AI Developer

<p>
  <a href="https://github.com/Omjee31">
    <img src="https://img.shields.io/badge/GitHub-Omjee31-black?style=for-the-badge&logo=github" />
  </a>
</p>

---

# ⭐ Acknowledgement

This project was developed as an implementation of an AI-powered pharmaceutical customer complaint management workflow, with the goal of demonstrating practical integration of **AI, frontend development, backend APIs, structured data validation, and database persistence**.

---

<p align="center">
  <b>Built with Python • FastAPI • React • PostgreSQL • AI</b>
</p>

<p align="center">
  ⭐ If you find this project interesting, consider giving the repository a star!
</p>
