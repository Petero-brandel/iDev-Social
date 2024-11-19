
iDev-Social is a Django-based social media platform. Below are the steps to set up and run the project locally.


HOW TO RUN THE PROJECT

## Requirements
- Python 3.x
- pip (Python package manager)
- Virtualenv (optional but recommended)
- SQLite (default database)
- Git

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Petero-brandel/iDev-Social.git
   cd iDev-Social
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate   # For Linux/Mac
   env\Scripts\activate      # For Windows
   ```

3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Migration
1. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Running the Server
1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure
- `main/`: Contains the core Django application files.
- `media/`: Stores uploaded files.
- `idevpro/`: Contains project-level settings and configurations.

## Additional Notes
- Ensure you have the required environment variables (if any).
- To deploy to production, refer to the Django deployment guide.
