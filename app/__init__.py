from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import Security
from flask_security import current_user
from flask import redirect, url_for, request
from flask_security import SQLAlchemyUserDatastore
from app.exceptions import BaseHttpException, http_exception_handler, python_exception_handler

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app.models import *


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class TaskModelView(ModelView):
    def is_accessible(self):
        return current_user.is_superuser

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class TaskReview(BaseView):
    @expose('/')
    def task_review(self):
        users_list = User.query.filter_by(is_superuser='true')
        return self.render('admin/task_review.html', users_list=users_list)


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(TaskModelView(Task, db.session))
admin.add_view(TaskReview(name='Task review', endpoint='task_review'))

app.register_error_handler(BaseHttpException, http_exception_handler)
app.register_error_handler(Exception, python_exception_handler)

from app import routes, models

