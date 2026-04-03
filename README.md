# Job Tracker API

A **containerized REST API** for tracking jobs, built with **Flask** and **Docker**.  
This project was **designed and guided using AI-assisted coding 70/30** to rapidly create a functional backend.

---

## Features

- Add, update, delete, and list jobs  
- Filter jobs by **status** (`pending`, `applied`, `rejected`)  
- Search jobs by **title**  
- Health check endpoint (`/health`)  
- Fully Dockerized for easy deployment

---

## Tech Stack

- Python 3.10  
- Flask  
- Flask SQLAlchemy  
- SQLite (embedded DB)  
- Docker

---

## Usage

### Run locally
```bash
git clone git@github.com:Husseinuahmedc/job-tracker.git
cd job-tracker
docker build -t job-tracker .
docker run -p 5000:5000 job-tracker
