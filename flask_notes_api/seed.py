from app import app, db
from models import User, Note
from faker import Faker
import random

faker = Faker()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()

    print("Seeding users...")
    
    users = []
    for _ in range(5):
        user = User(username=faker.user_name())
        user.set_password("password123") 
        users.append(user)
        db.session.add(user)
    db.session.commit()
    
    print("Seeding notes...")
    
    for user in users:
        for _ in range(random.randint(3, 7)):
            note = Note(
                title=faker.sentence(nb_words=5),
                content=faker.paragraph(nb_sentences=5),
                user_id=user.id
            )
            db.session.add(note)
    db.session.commit()

    print("Database seeding complete!")