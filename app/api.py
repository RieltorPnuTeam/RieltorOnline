# app/api.py

from flask import Blueprint, jsonify, request, abort
from app.models import User, Apartment
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')