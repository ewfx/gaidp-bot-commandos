# Transaction Compliance Checker

This project provides a **Transaction Compliance Checker** using **Streamlit** for the frontend and **FastAPI** for the backend. The system validates transactions against compliance rules for two sections: **H1** and **H2**.

## Features
- User-friendly **Streamlit UI** for manual transaction input.
- **FastAPI backend** to process compliance checks.
- Supports two compliance sections: **H1** and **H2**.
- Real-time validation and risk assessment.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip

### Clone the Repository
```sh
git clone https://github.com/ewfx/gaidp-bot-commandos.git
cd gaidp-bot-commandos
```


### Install Dependencies
```sh
pip install -r requirements.txt
```
## Short Notes on each python package
uvicorn is needed to run the FastAPI server.

langchain-community provides PyPDFLoader, so it's included.

pypdf is required because PyPDFLoader internally depends on it.

re and os are built-in Python modules, so they don’t need to be installed.

## Running the Application

### 1. Start the Backend (FastAPI)
```sh
uvicorn main:app --reload
```
This will start the API at `http://127.0.0.1:8000`.

### 2. Start the Frontend (Streamlit UI)
In another terminal, run:
```sh
streamlit run app.py
```
This will launch the UI in your browser.

## Usage
1. Open the Streamlit UI.
2. Select **H1 Compliance** or **H2 Compliance**.
3. Enter transaction details.
4. Click **Check Compliance**.
5. View validation results, risk score, and suggested remedies.

## API Reference
### Check Compliance Endpoint
```
POST http://127.0.0.1:8000/check_compliance/{section}
```
**Path Parameter:**
- `section`: `H1` or `H2`

**Request Body:**
- JSON object containing transaction details.

**Response:**
```json
{
  "compliant": "Yes" or "No",
  "risk_score": 85,
  "violated_rules": ["Rule 1", "Rule 2"],
  "remedies": ["Suggestion 1", "Suggestion 2"]
}
```


