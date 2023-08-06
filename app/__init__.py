from flask import Flask 

app=Flask(__name__)

#place import statements for modules within this packege to avoid circular import
from app import views