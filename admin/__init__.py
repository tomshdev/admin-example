from flask_admin.contrib.mongoengine import ModelView
from mongoengine import Document, StringField, ListField


class System(Document):
    TOKEN = StringField()
    ENGINE = StringField()
    PROMPT = StringField()


class SystemForm(ModelView):
    column_list = ('TOKEN', 'ENGINE', 'PROMPT')
    form_columns = ('TOKEN', 'ENGINE', 'PROMPT')


##############


class Task(Document):
    task_id = StringField(required=True, max_length=20)
    subjects = ListField(StringField())
    description = StringField()


class TaskForm(ModelView):
    column_list = ('task_id', 'description')
    column_sortable_list = ('task_id',)
    column_searchable_list = ('task_id', 'description')
    column_filters = ('task_id',)
    form_columns = ('task_id', 'subjects', 'description')

    def on_model_change(self, form, model, is_created):
        # Convert subjects to a list if it's a string
        if isinstance(model.subjects, str):
            model.subjects = [subject.strip() for subject in model.subjects.split(',')]
