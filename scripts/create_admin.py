from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.session import Session as SessionLocal
from core.security import hash_password

import argparse


def create_admin(db: Session, email: str, username: str, password: str):
    """
    Create an admin user in the database.
    """
    try:
        # Check if a user with the given username or email already exists
        check_query = text(
            """
            SELECT * FROM users
            WHERE username = :username OR email = :email
            LIMIT 1
            """
        )
        result = db.execute(
            check_query, {"username": username, "email": email}
        ).fetchone()

        if result:
            raise Exception("User with given username or email already exists.")

        # Insert a new admin user into the users table
        insert_query = text(
            """
            INSERT INTO users (email, username, password, role)
            VALUES (:email, :username, :password, 'ADMIN')
            """
        )
        db.execute(
            insert_query,
            {
                "email": email,
                "username": username,
                "password": hash_password(password),
            },
        )
        db.commit()

        print("Admin created successfully.")

    except SQLAlchemyError as ex:
        # Rollback in case of any SQLAlchemy errors
        db.rollback()
        print("SQLAlchemyError: ", ex)

    except Exception as ex:
        # Handle other exceptions
        print("Exception: ", ex)


if __name__ == "__main__":
    # Setup command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", type=str, help="Email")
    parser.add_argument("--username", type=str, help="Username")
    parser.add_argument("--password", type=str, help="Password")
    args = parser.parse_args()

    # Create a session and call create_admin
    with SessionLocal() as session:
        create_admin(
            db=session, email=args.email, username=args.username, password=args.password
        )
