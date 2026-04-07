# ChatApplication

This project is a real-time chat application built with FastAPI, featuring JWT-based authentication, role-based access control (RBAC), and WebSocket support for secure messaging. It includes PostgreSQL-backed persistence for users, chat rooms, and messages, with admin analytics for monitoring user activity and room engagement.

## API Documentation

- `/admin` for SQLAdmin UI

- REST API → [**Documentation**](https://www.postman.com/sumans-team-8696/workspace/suman-s-team/collection/33813618-5fda7e34-0f7d-4726-a7f6-50ddb0bbc069?action=share&source=copy-link&creator=33813618)
- Websocket → [**Documentation**](https://www.postman.com/sumans-team-8696/workspace/suman-s-team/collection/69d42469a8d45117c97afacb?action=share&source=copy-link&creator=33813618)

## Features

### Authentication

- JWT-based user authentication
- User signup and login
- Password validation and confirmation

### Authorization

- Role-Based Access Control (RBAC)
- User roles: `user`, `admin`
- Admin-level permissions for managing users and rooms

### Chat Feature

- Join a chat room via WebSocket
  - Authenticate user
  - Add to room participants
  - Notify others of user join
  - Send recent messages to the user
- Send and receive messages
  - Store messages in DB
  - Broadcast to all participants
- User and room management
  - Check room and user existence
  - Remove disconnected users
- Error handling
  - Handle disconnects and WebSocket errors

### User Management

- Retrieve authenticated user profile
- Update user profile
- Admin endpoints for:
  - Listing all users
  - Creating users
  - Retrieving a single user
  - Updating users
  - Deleting users

### Chat Rooms

- List rooms a participant belongs to
- Create a new chat room (user becomes admin)
- Retrieve details of a specific chat room
- Update chat room info
- Delete a chat room
- Admin endpoints for:
  - Listing all rooms
  - Creating rooms
  - Retrieving a room by ID
  - Updating rooms
  - Deleting rooms

### Messaging

- Retrieve recent messages in a room
- Supports pagination with `limit` and `cursor`
- WebSocket support for real-time messaging

### Admin Dashboards

- Room message counts within a date range
- User participation analytics:
  - Messages count per user
  - Rooms count per user

### Persistence

- PostgreSQL-backed storage
  - Users
  - Chat rooms
  - Messages

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
