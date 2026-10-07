# AI Expense Tracker

A full-stack expense tracking application that uses AI to convert natural-language messages into structured expense records.

Users can enter a transaction such as:

> Paid $14.50 at Panera for lunch

The application extracts the amount, merchant, category, and description before saving the transaction to the user’s account.

## Features

- User registration and login
- JWT-based authentication
- User-specific expense records
- AI-powered transaction extraction
- Add expenses using natural language
- Display merchant, category, description, and amount
- Delete expense records
- Total transaction and spending summaries
- Input validation with a 300-character limit
- Expired-session handling
- Logout functionality
- Responsive dashboard interface

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- React Router
- CSS

### Backend

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-JWT-Extended
- OpenAI API
- Pydantic

## How It Works

1. The user registers or logs in.
2. The backend returns a JWT access token.
3. The user enters one transaction in natural language.
4. The React frontend sends the text to the Flask API.
5. AI converts the text into structured expense data.
6. The backend validates and saves the expense for the current user.
7. The dashboard refreshes and displays the updated transactions and totals.

## Project Structure

```text
expense-tracker-pro/
├── backend/
│   ├── ai_service.py
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── .gitignore
└── README.md
```

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Log in and receive an access token |
| GET | `/expenses` | Retrieve the current user’s expenses |
| POST | `/ai/parse-expense` | Parse and save a natural-language expense |
| DELETE | `/expenses/:id` | Delete an expense |
| PATCH | `/expenses/:id` | Update an expense |

Protected endpoints require a JWT access token.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL
- An OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/iyai55/expense-tracker-pro.git
cd expense-tracker-pro
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost/database_name
JWT_SECRET_KEY=replace_with_a_secure_secret
OPENAI_API_KEY=replace_with_your_openai_api_key
```

Do not commit the `.env` file.

### 3. Start the backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies and start Flask:

```bash
pip install -r requirements.txt
python app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

### 4. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

## Example Transaction

```text
Paid $7.60 at Starbucks for coffee
```

The AI service converts the message into structured data similar to:

```json
{
  "amount": 7.6,
  "merchant": "Starbucks",
  "category": "Food and Drink",
  "description": "Coffee"
}
```

## Future Improvements

- Store and display transaction dates
- Daily and monthly expense summaries
- Filter expenses by date or category
- Expense editing interface
- Spending charts
- Application deployment

## What I Learned

This project helped me practice:

- Building a REST API with Flask
- Connecting React to a Python backend
- Managing authentication with JWT
- Creating user-specific database queries
- Managing React state and API requests
- Using structured AI output in an application
- Validating input on both the frontend and backend
- Handling API, authentication, and CORS errors

## Author

Created by [iyai55](https://github.com/iyai55)