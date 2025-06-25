from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def set_name(self, key, name):
        if not name:
            raise ValueError('Author must have a name')
        
        existing = Author.query.filter(Author.name.ilike(name)).first()
        if existing and existing.id != self.id:
            raise ValueError("An author with this name already exists.")
        return name
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError("Phone number is required.")
        if not (phone_number.isdigit() and len(phone_number) == 10):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary cannot exceed 250 characters.")
        return summary
    @validates('category')
    def validate_category(self, key, category):
        if category.lower() not in ['fiction', 'non-fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category.lower()
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["won't believe", "secret", "top", "guess"]
        if not any(phrase in title.lower() for phrase in clickbait_phrases):
            raise ValueError(
                "Title must contain one of: 'Won't Believe', 'Secret', 'Top', 'Guess'"
            )
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'