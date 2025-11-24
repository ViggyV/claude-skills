---
name: "Flask Optimizer"
description: "You are an expert at building and optimizing Flask applications."
---

# Flask Optimizer

You are an expert at building and optimizing Flask applications.

## Activation

This skill activates when the user needs help with:
- Flask application setup
- Flask blueprints
- Flask extensions
- Performance optimization
- Flask best practices

## Process

### 1. Application Factory Pattern

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # Register error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal server error'}, 500
```

### 2. Blueprints Organization

```python
# app/api/__init__.py
from flask import Blueprint
api_bp = Blueprint('api', __name__)

from app.api import users, orders

# app/api/users.py
from flask import request, jsonify
from app.api import api_bp
from app.models import User
from app.schemas import UserSchema

@api_bp.route('/users', methods=['GET'])
def list_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return jsonify(UserSchema(many=True).dump(users.items))

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(UserSchema().dump(user))

@api_bp.route('/users', methods=['POST'])
def create_user():
    schema = UserSchema()
    data = schema.load(request.json)
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(schema.dump(user)), 201
```

### 3. Configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
```

### 4. Request Validation with Marshmallow

```python
# schemas.py
from marshmallow import Schema, fields, validate, post_load

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

# Validation decorator
from functools import wraps

def validate_json(schema_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            try:
                data = schema.load(request.json)
            except ValidationError as err:
                return {'errors': err.messages}, 400
            return f(data, *args, **kwargs)
        return wrapper
    return decorator

@api_bp.route('/users', methods=['POST'])
@validate_json(UserSchema)
def create_user(data):
    # data is validated and loaded
    pass
```

### 5. Performance Optimization

```python
# Caching
from flask_caching import Cache
cache = Cache()

@api_bp.route('/products')
@cache.cached(timeout=300, key_prefix='products')
def list_products():
    return jsonify(Product.query.all())

# Eager loading
users = User.query.options(
    joinedload(User.orders)
).all()

# Pagination
from flask_sqlalchemy import pagination

@api_bp.route('/orders')
def list_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.paginate(page=page, per_page=20, error_out=False)
    return jsonify({
        'items': [o.to_dict() for o in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'page': orders.page,
    })

# Background tasks with Celery
from celery import Celery

celery = Celery()

@celery.task
def send_email_async(user_id, subject, body):
    user = User.query.get(user_id)
    send_email(user.email, subject, body)
```

### 6. Authentication

```python
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

jwt = JWTManager()

@api_bp.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if user and user.check_password(request.json['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)
    return jsonify(error='Invalid credentials'), 401

@api_bp.route('/me')
@jwt_required()
def get_me():
    user = User.query.get(get_jwt_identity())
    return jsonify(UserSchema().dump(user))
```

## Output Format

Provide:
1. Application structure
2. Blueprint organization
3. Schema validation
4. Caching strategy
5. Authentication setup
