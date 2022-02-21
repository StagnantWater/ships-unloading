from functools import wraps
from flask import Flask, session, current_app, request, render_template


def is_group_permission_valid():
    config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('group_name', 'unauthorized')

    target = request.endpoint

    if group_name in config and target in config[group_name]:
        return True
    return False


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_group_permission_valid():
            return f(*args, **kwargs)
        return render_template('denied.html')
    return wrapper
