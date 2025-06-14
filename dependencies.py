from models.user import User

def get_current_user() -> User:
    # TEMP: Return a mock user object for development/testing
    return User(id=100, name="Admin",email="admin@gmail.com",role="admin",username="admin",password="admin@123")  # Make sure this ID exists in DB
