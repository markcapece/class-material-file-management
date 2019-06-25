import json
from pathlib import Path
from datetime import date


class TodoManager(object):
    STATUS_ALL = 'all'
    STATUS_DONE = 'done'
    STATUS_PENDING = 'pending'
    CATEGORY_GENERAL = 'general'

    def __init__(self, base_todos_path, create_dir=True):
        self.base_todos_path = base_todos_path
        self.path = Path(self.base_todos_path)
        if self.path.exists():
            if self.path.is_file():
                raise ValueError('Invalid directory')
            elif self.path.is_dir():
                # OK
                pass
        else:
            if create_dir:
                self.path.mkdir(parents=True)
            else:
                raise ValueError('Directory does not exist')

    def list(self, status=STATUS_ALL, category=CATEGORY_GENERAL):
        result = {}
        for file in sorted(self.path.glob('*.json')):
            with file.open('r') as fp:
                jdict = json.load(fp)
            if status == TodoManager.STATUS_ALL:
                status = [TodoManager.STATUS_ALL, TodoManager.STATUS_DONE, TodoManager.STATUS_PENDING]
            result[jdict['category_name']] = [todo for todo in jdict['todos'] if todo['status'] in status]
        return result

    def new(self, task, category=CATEGORY_GENERAL, description=None,
            due_on=None):

        if due_on:
            if type(due_on) == date:
                due_on = due_on.isoformat()
            elif type(due_on) == str:
                # all good
                pass
            else:
                raise ValueError('Invalid due_on type. Must be date or str')

        # continue here
        new_todo = {
            'task': task,
            'description': description,
            'due_on': due_on,
            'status': TodoManager.STATUS_PENDING
        }

        new_dict = {
            'category_name': category.title(),
            'todos': []
        }

        p = self.path / '{}.json'.format(category)

        if p.exists():
            with p.open('r') as f:
                todo_dict = json.load(f)
        else:
            todo_dict = new_dict

        todo_dict['todos'].append(new_todo)

        with p.open('w') as f:
            json.dump(todo_dict, f)

    def complete(self, task, category=CATEGORY_GENERAL):
        p = self.path / '{}.json'.format(category)

        with p.open('r') as f:
            todo_dict = json.load(f)

        for todo in todo_dict['todos']:
            if todo['task'] == task:
                todo['status'] = self.STATUS_DONE

        with p.open('w') as f:
            json.dump(todo_dict, f)
