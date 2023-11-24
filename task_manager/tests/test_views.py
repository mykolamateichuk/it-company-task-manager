from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Task, TaskType, Position

INDEX_URL = reverse("task_manager:index")
WORKER_LIST_URL = reverse("task_manager:worker-list")

NUMBER_OF_WORKERS = 5


class PublicTestIndexPageView(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestIndexPageView(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
            position=Position.objects.create(name="user_position")
        )
        self.client.force_login(self.user)

    def test_context(self) -> None:
        task_type = TaskType.objects.create(name="Task type")

        task1 = Task.objects.create(
            name=f"Task 1",
            deadline=timezone.now(),
            is_completed=True,
            task_type=task_type
        )
        task1.assignees.add(self.user)

        task2 = Task.objects.create(
            name=f"Task 2",
            deadline=timezone.now(),
            is_completed=False,
            task_type=task_type
        )
        task2.assignees.add(self.user)

        response = self.client.get(INDEX_URL)

        self.assertEqual(len(list(response.context["tasks"])), 2)
        self.assertEqual(response.context["due_tasks"], 1)


class PublicTestWorkerListView(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestWorkerListView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        workers_to_create = NUMBER_OF_WORKERS

        positions = ["pos1", "pos2", "pos3", "pos4", "pos5"]

        for worker_id in range(workers_to_create):
            get_user_model().objects.create(
                username=f"Worker {worker_id}",
                password=f"worker{worker_id}",
                position=Position.objects.create(name=positions[worker_id])
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
            position=Position.objects.create(name="user_position")
        )
        self.client.force_login(self.user)

    def test_get_all_workers(self) -> None:
        response = self.client.get(WORKER_LIST_URL)

        all_workers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["workers"]),
            1
        )
        self.assertEqual(
            list(response.context["workers"]),
            list(all_workers)
        )

    def test_filter_workers_by_position(self) -> None:
        filter_request1 = "pos1"

        response1 = self.client.get(
            reverse("task_manager:worker-list"),
            {"position": int(filter_request1[len(filter_request1) - 1])}
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(
            len(response1.context["workers"]),
            1
        )
        self.assertEqual(
            list(response1.context["workers"]),
            [get_user_model().objects.all().first()]
        )

        filter_request2 = "pos2"

        response2 = self.client.get(
            reverse("task_manager:worker-list"),
            {"position": int(filter_request2[len(filter_request2) - 1])}
        )

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            len(response2.context["workers"]),
            1
        )
        self.assertEqual(
            list(response2.context["workers"]),
            [get_user_model().objects.all()[1]]
        )
