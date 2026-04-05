from db.session import Session


def get_db():

    session = Session()

    try:
        yield session
    finally:
        session.close()
