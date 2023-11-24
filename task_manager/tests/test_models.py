from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import TaskType, Position


class ModelsTests(TestCase):
    def test_task_type_str(self) -> None:
        name = "task"
        task_type = TaskType.objects.create(name=name)

        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self) -> None:
        name = "position"
        position = Position.objects.create(name=name)

        self.assertEqual(str(position), position.name)

    def test_worker_str(self) -> None:
        username = "username"
        password = "password"
        first_name = "first_name"
        last_name = "last_name"

        position = Position.objects.create(name="position")

        worker = get_user_model().objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            position=position
        )

        self.assertEqual(
            str(worker),
            f"{username} ({first_name} {last_name}) - {position}"
        )

    def test_worker_creation(self) -> None:
        username = "username"
        password = "password"
        position = Position.objects.create(name="position")

        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position
        )

        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.position, position)
