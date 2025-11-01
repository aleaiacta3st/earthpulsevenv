import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Float, String, Boolean, DateTime, Integer
import datetime 
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from .config import current_config



load_dotenv()
password=os.environ.get("DB_PASSWORD")



DATABASE_URL = current_config["DATABASE_URL"]

#create the async engine 
#echo=true will print all SQL statements to console, useful for debugging 
#Remember - May need to turn it off in production to decrease processing overhead
engine = create_async_engine(DATABASE_URL, echo=True)

#create base class. Our models will inherit from this base.
Base = declarative_base() 

#create session factory 
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#create a class which inherits from Base. Each attribute of this class is a column. 
class Earthquake(Base):
    __tablename__ = "earthquakes"
    id = Column(String, primary_key=True)
    place=Column(String)
    magnitude=Column(Float)
    depth=Column(Float)
    latitude=Column(Float)
    longitude=Column(Float)
    tsunami=Column(Boolean)
    occurred_at=Column(DateTime) 

#converts python dicts to earthquake objects, handles dbsession ops
async def save_earthquakes(earthquakes_imp):
    earthquake_objects=[]
    for earthquake in earthquakes_imp:
        eq_object = Earthquake(
            id=earthquake["id"],
            place=earthquake["place"],
            magnitude=earthquake["magnitude"],
            depth=earthquake["depth"],
            latitude=earthquake["latitude"],
            longitude=earthquake["longitude"],
            tsunami=earthquake["tsunami"],
            occurred_at=earthquake["occurred_at"]  # Already a datetime object from your parser
        )
        earthquake_objects.append(eq_object) 
    
    try:
        async with async_session() as session:
            # Use SQLAlchemy's built-in merge function to handle upserts
            for eq_object in earthquake_objects:
                await session.merge(eq_object)
            await session.commit()
            return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

async def init_db():
    """Create all tables in the database if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_earthquakes(limit=10, offset=0, min_magnitude=0):
    try:
        async with async_session() as session:
            from sqlalchemy import select
            query = select(Earthquake).where(Earthquake.magnitude >= min_magnitude)\
                .order_by(Earthquake.occurred_at.desc())\
                .offset(offset)\
                .limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
    except Exception as e:
        print(f"Database error: {e}")
        return []




















# """ 
# Engine -
# connection to the database
# a bridge between python code and postgresql 
# manages the com channel to the database server 
# In this code we use async engine 
# asyncsession - async version of database session class, allows to perform db ops w/o blocking the program while waiting for db responses 

# what is a session?
# similar to convo between this program and the database
# 1. you want to talk to someone on the phone
# 2. dial number and they answer(opening a session)
# 3. have convo(doing db ops)
# 4. say goodbye and hangup(close the session)

# Factory
# A function or class that creates objects for us 
# def make_car():
#     return Car()

# what is factory generator?
# It is something which creates factories.
# def make_factory():
#     def make_thing():
#         return Thing()
#     return make_thing 
# when i call make_factory I get make_thing(a function) which is a factory because it returns objects 
# How You Would Use This Code
# # Create the factory
# my_factory = make_factory()  

# # Now use the factory to create things
# thing1 = my_factory()  # Creates a Thing
# thing2 = my_factory()  # Creates another Thing 

# How This Relates to SQLAlchemy's sessionmaker
# In SQLAlchemy:

# sessionmaker is like your make_factory()
# The session factory it returns is like your make_thing
# The actual sessions it creates are like your Thing() objects 

# Factory Pattern in SQLAlchemy: Complete Summary
# SQLAlchemy uses the factory pattern (sessionmaker) instead of direct object creation because: 
# Avoids repetition: Creating a session directly would require repeating all configuration parameters every time: 
# # Without factory - repeat this verbose configuration every time:
# session1 = AsyncSession(bind=engine, expire_on_commit=False, autoflush=True)
# session2 = AsyncSession(bind=engine, expire_on_commit=False, autoflush=True) 

# DRY principle: The factory approach follows "Don't Repeat Yourself" by configuring settings once: 
# # Configure once:
# async_session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=True)

# # Create many sessions with minimal code:
# session1 = async_session()
# session2 = async_session()  

# Consistency: Every session has identical settings, preventing subtle configuration bugs

# Maintainability: If database connection details change, you update one factory instead of hunting through code 

# The factory approach reduces repetitive boilerplate code, especially important when creating complex objects with multiple configuration options like database sessions.



# SessionObject


# Base - 
# A template class from which models inherit 

# Data Model
# A description of what info I want to be stored and how it's organised. In this project, data model decsribes what details I am saving about each earthquake.(location, mag, time etc)

# SQLAlchemy:
# Makes working with databases easier. 
# Instead of writing complex db commands, it can convert the python code into db operations automatically. It is like a translator b/n Python and PostgreSQL database.

# Inherit:
# When Earthquake class "inherits" from Base, it's like saying "I want all the basic database functionality that Base provides, plus I'll add my own specific earthquake-related fields."


# Environment variables
# A name-value pair sroted on my os
# Name: An identifier(like DB_pwd)
# Value: The dat that needs to be stored(secret123)

# How do these env variables work?
# OS maintains a list of n-v pairs and any prog can request the value by name
# example: Most PCs have an env variable called PATH that tells them where to look for progs 

# DATABASE_URL = f"postgresql+asyncpg://postgres:{password}@localhost:5432/Earthquakes" 

# postgresql    # Database type
# +asyncpg      # Python driver for PostgreSQL
# ://           # Protocol separator
# postgres      # Username
# :             # Username/password separator
# {password}    # Password variable (will be filled with actual value)
# @             # Authentication/server separator  
# localhost     # Server address (your computer)
# :             # Server/port separator
# 5432          # Port number
# /             # Port/database separator
# Earthquakes   # Database name


# What Is a Database Driver?
# Think of a database driver like a translator between two people who speak different languages:

# Your Python program speaks "Python language"
# Your PostgreSQL database speaks "PostgreSQL language"
# The driver (like asyncpg) is the translator in the middle

# Without this translator (driver), your Python code and PostgreSQL database couldn't communicate at all.

#  expire on commit=False
# # after commit. there is a copy of data in the db and also a copy as python objects in program memory. we want python code to remember it even after committing it. Keep using the Python objects you already have in memory, don't try to refresh them from the database. 
# # This is particularly important in async code because:

# # If SQLAlchemy tried to refresh the data automatically
# # It would need to make a database query
# # That query would require an await statement
# # If your code isn't expecting that, it would crash

# # By keeping the Python objects "alive" after commit, your code can continue working with them without unexpected database queries happening behind the scenes. 
# # surprise data queries with sqlalchemy in async will fail because it will not use the await keyword


# primary_key=True - This critical flag tells SQLAlchemy:

# This column uniquely identifies each row (no duplicates allowed)
# This column cannot be null (must have a value)
# This column will be indexed automatically for fast lookups
# This is the main identifier used when relating to other tables


# ORM Objects:
#object relational mapping - a programming tech that converts data b/nincompatible type systems, sepcifically between this python code and relational database 

#database thinks in terms of tables, rows and rels. Pyth thinks in terms of objects, attributes, emthods. ORM objects bridge this gap. 
# ORM objects auto convert db records(rows) into pyth objects you can work with directly. and also in the opposite direction 

# Here's how it works:

# SQLAlchemy (the ORM framework) provides the foundation through declarative_base()
# Your Earthquake class inherits from Base, making it an ORM class
# When you create instances of Earthquake, those instances are ORM objects

# It's like this:

# SQLAlchemy → Provides ORM functionality
# Base = declarative_base() → Creates a base class with ORM capabilities
# class Earthquake(Base) → Creates your specific ORM class
# earthquake_obj = Earthquake(...) → Creates an ORM object

# Pagination support
# w/o it reults will load in a single page. and users will have to scroll thru. As the list in the database grows, this is not practical.

# The backslash (\) at the end of a line is a line continuation character in Python. It tells the interpreter that the current logical line continues on the next physical line. This allows you to break up long lines of code for better readability.
               
# When you query your database, you're absolutely retrieving only earthquake data - there are no "other objects" in your table.
# The .scalars().all() method is just SQLAlchemy's way of processing query results:

# When SQLAlchemy executes a query, it returns a "Result" object (essentially a wrapper around your database results)
# The .scalars() method extracts your actual Earthquake objects from this wrapper
# The .all() method collects these objects into a Python list 

# Why queries return Python objects, not "database objects"
# The database itself doesn't return "Python objects" - it returns rows of data. SQLAlchemy does the conversion:

# You call get_earthquakes()
# SQLAlchemy generates and sends an SQL query to PostgreSQL
# The database returns rows of data
# SQLAlchemy converts these rows into Python objects matching your defined Earthquake class
# Your code then works with these familiar Python objects

# This conversion is exactly what makes ORMs like SQLAlchemy valuable - they handle the translation between database rows and Python objects automatically.

# In db.py, we defined an Earthquake class that inherits from Base - this is the mapping that tells SQLAlchemy how to convert between database records and Python objects.

# The operation where SQLAlchemy converts Python objects into database rows is called "persisting" data to the database. In your code, this happens in the save_earthquakes() function in db.py 

# All SQLAlchemy objects are Python objects
# Not all Python objects are SQLAlchemy objects 

# class Earthquake(Base):
#     __tablename__ = "earthquakes"
#     id = Column(String, primary_key=True)
#     # other fields...


# This creates a special Python class that:

# Is a regular Python class (can be instantiated, has attributes, etc.)
# Has extra SQLAlchemy features that map it to your database table

# When you query the database with get_earthquakes(), SQLAlchemy returns instances of this class - they're Python objects that have a direct mapping to rows in your database.