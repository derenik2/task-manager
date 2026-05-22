from ..extensions import db
from ..models.task import Task


def get_tasks_for_user(owner_id: int) -> list[Task]:
    return db.session.execute(
        db.select(Task).where(Task.owner_id == owner_id)
    ).scalars().all()


def create_task(title: str, owner_id: int) -> Task:
    task = Task(title=title, owner_id=owner_id)
    db.session.add(task)
    db.session.commit()
    return task


def toggle_task(task_id: int) -> Task | None:
    task = db.session.get(Task, task_id)
    if task is None:
        return None
    task.done = not task.done
    db.session.commit()
    return task


def delete_task(task_id: int) -> bool:
    task = db.session.get(Task, task_id)
    if task is None:
        return False
    db.session.delete(task)
    db.session.commit()
    return True
