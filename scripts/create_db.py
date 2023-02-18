import os

from wedding_fullstack.app import app, db

with app.app_context():
    if os.path.exists("instance/project.db"):
        os.remove("instance/project.db")
    db.create_all()
    os.chmod("/var/www/wedding_fullstack/instance", 0o0777)
    os.chmod("/var/www/wedding_fullstack/instance/project.db", 0o0777)
