# Task Master System API

## Description

REST API developed with Django and Django REST Framework for managing tasks and tracking their status. The application allows users to create, update, delete, and retrieve tasks, as well as manage their statuses efficiently. Authentication is handled via JWT tokens.

## Technologies Used

- **Django** and **Django REST Framework**
- **PostgreSQL** (via Docker)
- **Docker** and **Docker Compose**
- **JWT Authentication**

## Features

- **Task Management**: Create, retrieve, update, and delete tasks with attributes like title, description, status, and due date.
- **Status Tracking**: Update task statuses to "Pending," "In Progress," or "Completed."
- **JWT Authentication**: Ensure secure access, allowing users to manage only their own tasks.

---

## Setup Instructions

1. Clone the Repository:

   ```bash
   https://github.com/Yghor-Castello/TaskMaster.git
   ```

2. Configure and Start with Docker:

   ```bash
   docker-compose up --build
   ```

3. Apply Migrations and Create a Superuser:

   ```bash
   docker-compose exec backend python manage.py migrate
   ```

   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. Load Fixtures to Populate the Database:

   ```bash
   docker-compose exec backend python manage.py loaddata tasks_fixture.json
   ```

5. Access the API:

   - The API will be available at `http://localhost:8000/`.

6. Run Tests:

   ```bash
   docker-compose exec backend pytest
   ```

7. Test with Insomnia:

   - Navigate to the `insomnia_collection` folder and import the JSON file into your Insomnia workspace.

---

## Example Endpoints

- `http://localhost:8000/api/tasks/` - Retrieve all tasks.
- `http://localhost:8000/api/tasks/{id}/` - Retrieve, update, or delete a specific task by ID.
- `http://localhost:8000/api/tasks/?status=completed` - Filter tasks by status.

---