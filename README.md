# ChatApplication

This project is a real-time chat application built with FastAPI, featuring JWT-based authentication, role-based access control (RBAC), and WebSocket support for secure messaging. It includes PostgreSQL-backed persistence for users, chat rooms, and messages, with admin analytics for monitoring user activity and room engagement.

## API Documentation

- `/admin` for SQLAdmin UI

- REST API → [**Documentation**](https://www.postman.com/sumans-team-8696/workspace/suman-s-team/collection/33813618-5fda7e34-0f7d-4726-a7f6-50ddb0bbc069?action=share&source=copy-link&creator=33813618)
- Websocket → [**Documentation**](https://www.postman.com/sumans-team-8696/workspace/suman-s-team/collection/69d42469a8d45117c97afacb?action=share&source=copy-link&creator=33813618)

## Technology Stack

- FastAPI
- Uvicorn
- SQLAlchemy (or SQLModel),
- psycopg2 (for PostgreSQL),
- passlib (for password hashing),
- python-jose
- SQLAdmin

## Setup

1. Git clone the repo
2. Install Python dependenices
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI development server

   ```
   cd app
   python -m fastapi dev
   ```

---

THE END
