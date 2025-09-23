
# Professional Psychological Assessment System (MCMI-III)

This project is a professional-grade psychological assessment system for the Millon Clinical Multiaxial Inventory (MCMI-III). It includes complete clinical scoring, T-score conversions, and professional results visualization.

## Features

- **Complete MCMI-III Test**: All 175 questions are included.
- **Clinical Scoring**: Implements the full, complex scoring and adjustment algorithms.
- **Results Visualization**: Displays scores in a professional, clinical format with bar charts and color-coding.
- **Flask Backend**: Built with Python and the Flask web framework.
- **SQLite Database**: Uses SQLite for storing assessment data.
- **RESTful API**: Provides endpoints for submitting assessments and retrieving results.

## File Structure

```
assessment-system/
├── app.py
├── scoring.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── results.html
└── static/
    ├── css/style.css
    └── js/
        ├── assessment.js
        └── results.js
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  Open your web browser and navigate to `http://127.0.0.1:5000/` to begin an assessment.

## How It Works

1.  The user visits the main page and answers all 175 questions.
2.  Upon submission, the frontend sends the responses to the `/api/submit` endpoint.
3.  The Flask backend uses the `scoring.py` module to calculate the raw scores, Base Rate (BR) scores, and all clinical adjustments.
4.  The scores are stored in the `assessments.db` SQLite database.
5.  The user is redirected to a results page, where the scores are fetched from the `/api/results/<session_id>` endpoint and displayed visually.
