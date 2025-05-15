    # ExpertMatch
    ExpertMatch is a Django-based backend application designed to match candidates with experts based on their resumes. It leverages AI-powered resume parsing and scoring to evaluate the relevance of a candidate's profile compared to an expert's profile.

    ## Features

    - **User Authentication**: Secure user registration and login using JWT-based authentication.
    - **AI-Powered Resume Parsing**: Utilizes Google Generative AI (Gemini) for extracting and structuring resume data.
    - **Scoring System**: Evaluates candidates against experts based on key parameters such as education, skills, experience, and projects.
    - **RESTful APIs**: Provides endpoints for managing users, profiles, and scores.
    - **Admin Interface**: Built-in Django admin panel for managing application data.

    ---

    ## File Structure

    The project is organized as follows:

    ```
    ExpertMatch/
    ├── account/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── signals.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   ├── views.py
    ├── ExpertMatch/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    ├── db.sqlite3
    ├── Dockerfile
    ├── manage.py
    ├── requirements.txt
    ├── README.md
    ```

    ---

    ## API Endpoints

    Here are the available API endpoints:

    ### Authentication
    - **POST** `/register/` - Register a new user.
    - **POST** `/login/` - Login and obtain JWT tokens.
    - **POST** `/token/refresh/` - Refresh the access token.
    - **POST** `/token/verify/` - Verify the validity of a token.

    ### User Management
    - **GET** `/candidates/` - Retrieve a list of all candidates.
    - **GET** `/experts/` - Retrieve a list of all experts.
    - **GET** `/profile/<int:id>` - Retrieve the profile of a user by ID.
    - **POST** `/adduser/` - Add a new user along with their resume.

    ### Resume and Scoring
    - **GET** `/userinfo/<int:id>` - Retrieve structured resume information for a user.
    - **GET** `/score/<int:id>` - Generate and retrieve score matches for a user.

    ---

    ## Prerequisites

    Before setting up the project, ensure you have the following installed:

    - **Python**: Version 3.10 or higher.
    - **pip**: Python package manager.
    - **Docker**: (Optional) For containerized deployment.

    ---

    ## Setup Instructions

    Follow these steps to set up and run the project:

    ### 1. Clone the Repository

    Clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    cd ExpertMatch
    ```

    ### 2. Create and Activate a Virtual Environment

    Set up a virtual environment to isolate dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    ### 3. Install Dependencies

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

    ### 4. Configure Environment Variables

    Create a `.env` file in the project root and add the following variables:

    ```env
    DEBUG=True
    API_KEY=<Your-Google-Generative-AI-API-Key>
    ```

    Replace `<Your-Google-Generative-AI-API-Key>` with your actual API key.

    ### 5. Apply Database Migrations

    Set up the database by applying migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    ### 6. Create a Superuser

    Create an admin account for accessing the Django admin panel:

    ```bash
    python manage.py createsuperuser
    ```

    ### 7. Build a Docker Image (Optional)

    If you prefer to run the application in a Docker container, build the Docker image:

    ```bash
    docker build -t expertmatch .
    ```

    ### 8. Run the Development Server

    Start the Django development server:

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

    ---

    ## Additional Notes

    - **Admin Panel**: Access the admin panel at `/admin` using the superuser credentials.
    - **API Documentation**: Use tools like Postman or Swagger to explore the available API endpoints.
    - **Docker Deployment**: If using Docker, ensure the required ports are exposed and mapped correctly.

    For further assistance, refer to the official Django documentation or the project's source code.
