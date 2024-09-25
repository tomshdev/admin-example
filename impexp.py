from contextlib import contextmanager
from importlib.resources import files
import sys

from mongoengine import connect, disconnect
import json

from admin import System, Task
from app import Settings


@contextmanager
def mongodb():
    connect(**Settings.MONGODB_SETTINGS)
    yield
    disconnect()


def import_system(filepath: str):
    with open(filepath, 'r') as f:
        doc = json.load(fp=f)

    with mongodb():
        prompt = '\n'.join(doc.get('PROMPT'))
        system_props = System(
            TOKEN=doc.get('TOKEN'),
            ENGINE=doc.get('ENGINE'),
            PROMPT=prompt
            )
        system_props.save()


def export_system(filepath: str):
    with mongodb():
        doc = System.objects.only('TOKEN', 'ENGINE', 'PROMPT').first()

    with open(filepath, 'w') as f:
        json.dump(dict(
                TOKEN=doc.TOKEN,
                ENGINE=doc.ENGINE,
                PROMPT=doc.PROMPT.split("\n")),
            fp=f,
            indent=4)


def import_tasks(filepath: str):
    with open(filepath, 'r') as f:
        tasks = json.load(fp=f)

    with mongodb():
        for task_id, task_dict in tasks.items():
            task = Task(task_id=task_id, **task_dict)
            task.save()


def export_tasks(filepath: str):
    with mongodb():
        docs = list(Task.objects.all())
    
    tasks = dict()
    for task in docs:
        tasks[task.task_id] = dict(
            subjects=task.subjects,
            description=task.description)
    
    with open(filepath, 'w') as f:
        json.dump(tasks, fp=f, indent=4)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} <command> <filepath>")

    cmd = sys.argv[1]
    filepath = sys.argv[2]

    if cmd == "import-system":
        import_system(filepath)
    elif cmd == 'import-tasks':
        import_tasks(filepath)
    elif cmd == 'export-system':
        export_system(filepath)
    elif cmd == 'export-tasks':
        export_tasks(filepath)
    else:
        print(f"commands: import-system, import-tasks, export-system, export-tasks")

    print("done")
