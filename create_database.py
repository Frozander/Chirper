from chirper import db, create_app
app = create_app()
app.app_context().push()
db.drop_all()
db.create_all()
