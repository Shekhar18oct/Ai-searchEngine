import sys
import os

# Replace 'yourusername' with your PythonAnywhere username
project_home = '/home/yourusername/Ai-searchEngine'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set working directory
os.chdir(project_home)

# Import Flask app
from src.main import app as application
