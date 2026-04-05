from db.session import Session


def get_db():

    session = Session()

    try:
        yield session
    except:
        session.close()
