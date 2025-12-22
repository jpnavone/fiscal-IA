import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Denuncia(Base):
    __tablename__ = 'denuncias'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    filename = Column(String)
    transcript = Column(Text)
    keywords = Column(String) # Stored as comma-separated string
    summary = Column(Text)
    category = Column(String)
    file_type = Column(String)

    def __repr__(self):
        return f"<Denuncia(id={self.id}, filename='{self.filename}')>"

# Setup database connection
DB_PATH = "sqlite:///judicial_voice.db"
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(engine)

def save_denuncia(filename, transcript, keywords, summary, category, file_type):
    """Save a processed denuncia to the database."""
    session = Session()
    try:
        # Ensure keywords is a string if it's a list
        if isinstance(keywords, list):
            keywords = ", ".join(keywords)
            
        new_denuncia = Denuncia(
            filename=filename,
            transcript=transcript,
            keywords=keywords,
            summary=summary,
            category=category,
            file_type=file_type
        )
        session.add(new_denuncia)
        session.commit()
        return new_denuncia.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def search_denuncias(query):
    """Search denuncias by keyword or transcript content."""
    session = Session()
    try:
        results = session.query(Denuncia).filter(
            (Denuncia.keywords.ilike(f'%{query}%')) | 
            (Denuncia.transcript.ilike(f'%{query}%'))
        ).all()
        return results
    finally:
        session.close()

def get_all_denuncias():
    """Retrieve all denuncias."""
    session = Session()
    try:
        return session.query(Denuncia).order_by(Denuncia.timestamp.desc()).all()
    finally:
        session.close()
