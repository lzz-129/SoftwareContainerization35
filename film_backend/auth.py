# auth.py
import jwt
from flask import current_app, jsonify
from datetime import datetime, timedelta

def generate_token(username):
    """generate JWT token"""
    try:
        # 设置令牌的过期时间
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1), # 例如设置1天后过期
            'iat': datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_token(token):
    """decode JWT token"""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub'] # 返回用户ID或用户名
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired. Please log in again.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token. Please log in again.'}), 401