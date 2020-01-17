"""SQLAlchemy-MutableSoup examples"""

"""Setup"""
# 1. Import from SQLAlchemy-MutableSoup
from sqlalchemy_mutablesoup import MutableSoupType

# 2. Standard session creation
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# 3. Create a model class with a `MutableSoupType` Column
class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    soup = Column(MutableSoupType)

# 4. Create the database
Base.metadata.create_all(engine)

# 5. Additional setup
from bs4 import BeautifulSoup

model = Model()
session.add(model)

"""Examples"""
print('\nExample 1: Setting the `soup` from a string')
model.soup = '<p>Hello World.</p>'
print(model.soup)
print(
    '`soup` is a BeautifulSoup object?', 
    isinstance(model.soup, BeautifulSoup)
)

print('\nExample 2: Setting the `soup` from a `BeautifulSoup` object')
model.soup = BeautifulSoup('<p>Hello World.</p>', 'html.parser')
print(model.soup)

print('\nExample 3: Setting an element')
model.soup.set_element(parent_selector='p', val='Hello Moon.')
session.commit()
print(model.soup)

print('\nExample 4: Setting an element (advaced)')
def gen_span_tag(*args, **kwargs):
    print('My args are:', args)
    print('My kwargs are:', kwargs)
    return BeautifulSoup('<span></span>', 'html.parser')

model.soup.set_element(
    parent_selector='p',
    val='Span text',
    target_selector='span',
    gen_target=gen_span_tag,
    args=['hello world'],
    kwargs={'hello': 'moon'}
)
session.commit()
print(model.soup)

print('\nExample 5: Using the `changed` method')
model.soup.select_one('p')['style'] = 'color:red;'
session.commit()
print(model.soup)

model.soup.select_one('p')['style'] = 'color:red;'
model.soup.changed()
session.commit()
print(model.soup)