from sqlmodel import Session, SQLModel, create_engine

# Database URL
DATABASE_URL = 'sqlite:///./db/main.sqlite'

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the tables
SQLModel.metadata.create_all(engine)


# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session
