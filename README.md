# NayePankh Saathi 🪽

### 🔗 Live Demo

🌐 **Live Application:** `https://nayepankh-saathi-ccflnlehmiukybvuj2quew.streamlit.app/`

---

## 📌 Project Overview

**NayePankh Saathi** (Saathi means *companion* in Hindi) is an AI-powered volunteer and awareness hub built for **NayePankh Foundation**.

The goal of this project is to help the foundation automate volunteer coordination, answer frequently asked questions, generate awareness campaign content, and visualize volunteer engagement data through an interactive dashboard.

Unlike a traditional static website, this project provides a **live multi-page application** that reviewers can actively explore.

---

## 🚀 Why This Project Stands Out

### ✅ Live Deployment

Instead of submitting screenshots or a ZIP file, this project is deployed online so reviewers can interact with every feature.

### 🤖 Three Separate AI Features

The application contains three distinct AI-powered modules:

* AI Volunteer Role Matching
* Multilingual FAQ Assistant
* AI Campaign Generator

### ❤️ Solves Real NGO Problems

The project directly addresses common NGO challenges:

* Volunteer coordination
* Awareness campaign creation
* Information accessibility
* Data-driven decision making

---

## 🏗️ Features

### 📝 Volunteer Registration + AI Match

Volunteers can register their details and receive AI-generated role recommendations based on:

* Skills
* Interests
* Availability
* Preferred programs

The information is stored in SQLite for future use.

---

### 💬 Multilingual FAQ Chatbot

An AI assistant that answers common NGO-related questions in:

* English
* Hindi

Examples:

* How can I volunteer?
* What programs does NayePankh offer?
* Mujhe volunteer kaise banna hai?

---

### 📣 Campaign Generator

Generate awareness content with one click.

Outputs include:

* Instagram posts
* X (Twitter) threads
* Email drafts
* Relevant hashtags

---

### 📊 Impact Dashboard

Visualize volunteer data using Plotly charts.

Includes:

* Volunteer registrations over time
* Program distribution
* Skills distribution
* Search and filter functionality

---

## 🖥️ Application Architecture

```text
Browser
   ↓
Streamlit Application
   ↓
SQLite Database
   ↓
Gemini Flash API
```

---

## 🛠️ Tech Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Core programming language |
| Streamlit        | User interface            |
| Gemini Flash 1.5 | AI capabilities           |
| SQLite           | Volunteer database        |
| Plotly           | Interactive dashboards    |
| Pandas           | Data processing           |
| python-dotenv    | Environment management    |

---

## 📂 Project Structure

```text
nayepankh_saathi/

├── app.py

├── pages/
│   ├── 1_Home.py
│   ├── 2_Register.py
│   ├── 3_Chatbot.py
│   ├── 4_Campaign.py
│   └── 5_Dashboard.py

├── utils/
│   ├── ai.py
│   └── db.py

├── .streamlit/
│   └── config.toml

├── requirements.txt

└── .env
```

---

## 🎯 Internship Category

**Primary Category:**

🤖 Artificial Intelligence (AI) Internship – Option 2

**Additional Areas Covered:**

* 🤖 AI Web Development
* 📊 Data Analytics
* 🐍 Python Development
* 🗄️ Backend Development

---

## 📈 Future Improvements

Potential enhancements:

* Volunteer authentication system
* Admin login
* Email notifications
* Export dashboard reports
* Advanced analytics
* Event management system

---

## 👨‍💻 Author

**Sahil Katkamwar**

Built as an internship submission project for **NayePankh Foundation**.

