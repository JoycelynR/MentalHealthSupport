
from database import engine
from models import Base

Base.metadata.drop_all(bind=engine)
print("All tables dropped.")

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
