from sqlalchemy import create_engine        # Create a connection setup for the database.
from sqlalchemy.orm import sessionmaker     # A Session is like a temporary workspace for database operations.

DATABASE_URL = "mysql+mysqldb://root:@localhost:3306/dummy_shop"   # database address.

engine = create_engine(DATABASE_URL)   # SQLAlchemy creates an Engine object

SessionLocal = sessionmaker(
    autocommit = False,         # Without committing, MySQL doesn't save it permanently.
    autoflush = False,          # Send changes to the database temporarily. false means not tremp saves
    bind = engine               # Attach this Session Factory to this Engine
)

