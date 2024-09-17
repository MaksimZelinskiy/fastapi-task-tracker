# FASTAPI Таск трекер
### Tech stack

- **PL**: Python
- **Framework**: FastAPI
- **DB**: PostgreSQL
- **Documentation  API**: Built-in FastAPI documentation is available at `/docs`.
- **Tests**: pytest 

## Project structure:
```
project/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── user.py
│   │   ├── activity_log.py
│   │   ├── comment.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   ├── auth.py
│   │   ├── activity_log.py
│   │   ├── comments.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── user.py
│   │   ├── activity_log.py
│   │   ├── comment.py
│   ├── config/
│   │   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── email_sender.py
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup and installation

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MaksimZelinskiy/fastapi-task-tracker.git
   cd fastapi-task-tracker/
   ```
2. Build and run Docker containers:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000`.

#### Documentation API
- Documentation API: `http://localhost:8000/docs`.

## Functionality

### Task management:

**1. Create a task (`POST /tasks`)**:
- Allows users to create new tasks.
- Each task has the following fields:
   - **title**: The task's title.
   - **description**: The task's description.
   - **status**: The task's status (e.g., `TODO`, `In progress`, `Done`).
   - **priority**: The task's priority (e.g., `Low`, `Medium`, `High`).
   - **task_assignees**: A list of users assigned to the task (assignees).
   - **owner_user_id**: The ID of the user who created the task (task owner).
- After creating the task, assignees are automatically added to the `task_assignees` table, which links tasks to assignees.
- Returns a JSON response with details of the created task.

**2. Get tasks (`GET /tasks`)**:
- Allows users to retrieve a list of tasks with optional filtering by status and priority.
- Supports pagination through the `skip` (to skip N records) and `limit` (to limit the number of records) parameters.
- Tasks can be filtered by status (`TODO`, `In progress`, `Done`) and priority (`Low`, `Medium`, `High`).
- For each task, it returns details about the assignees, owner, status, priority, and creation date.

**3. Update a task (`PUT /tasks/{task_id}`)**:
- Allows users to update an existing task.
- Checks if the task status has been changed. If the status is updated, it sends an email notification to the task owner.
- Activity log tracking: Whenever the task status or assignees are updated, an event is recorded in the `activity_logs` table. This log helps to track the history of changes.
- When updating assignees, existing assignees are removed, and the new ones are added.
- Returns a JSON response with the updated task information.

**4. Delete a task (`DELETE /tasks/{task_id}`)**:
- Allows users to delete a task after verifying that the current user is the owner.
- Removes all assignee records related to the task before deleting the task itself.
- Returns a response confirming successful deletion or an error if the task is not found or the user does not have permission to delete it.

**5. Create a task comment (`POST /tasks/{task_id}/comments`)**:
- Each comment is linked to a specific task and includes:
   - **content**: The comment text.
   - **task_id**: The task.
   - **user_id**: The user who posted the comment.

**6. Get omments on tasks (`GET /tasks/{task_id}/comments`)**:
- Comments have been left for users on this task.

**7. Activity log (`GET /tasks/{task_id}/activity_log`)**:
- Tracks changes and updates to tasks, such as status_update, assignment_update.
- Returns a the activity log for a task.

### Authentication:

**Register a new user (`POST /register`)**:
- Allows users to create a new account with a **unique username**, **unique email**, and **password**.
- Returns a **JWT token** for authentication upon successful registration.

**User login (`POST /token`)**:
- Allows users to log in with their **username** and **password**.
- Returns a **JWT token** if the credentials are correct, otherwise returns a **401 Unauthorized** error.

**Security**:
- Passwords are hashed before storage.
- JWT tokens are created for authenticated access, with an expiration time controlled by `ACCESS_TOKEN_EXPIRE_MINUTES`.

**Role-based access control**:
- Users have different roles (`Admin`, `Manager`, `User`), which determine their permissions to create, edit, or delete tasks.



