import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

    LOGIN_DISABLED =  os.getenv('LOGIN_DISABLED') == 'True'