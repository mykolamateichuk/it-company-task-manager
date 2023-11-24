from django.urls import path

from task_manager.views import (
    index,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    task_update_status,
    task_detail_view,
    WorkerCreateView,
    WorkerListView,
    worker_detail_view,
    WorkerUpdateView,
    deadlines_view
)

urlpatterns = [
    path("", index, name="index"),
    path("create-task/",
         TaskCreateView.as_view(),
         name="create-task"),
    path("task/<int:pk>/",
         task_detail_view,
         name="task-detail"),
    path("delete-task/<int:pk>/",
         TaskDeleteView.as_view(),
         name="delete-task"),
    path("update-task/<int:pk>/",
         TaskUpdateView.as_view(),
         name="update-task"),
    path("update-task-status/<int:pk>/",
         task_update_status,
         name="update-task-status"),
    path("create-account/",
         WorkerCreateView.as_view(),
         name="create-account"),
    path("worker-list/",
         WorkerListView.as_view(),
         name="worker-list"),
    path("worker/<int:pk>/",
         worker_detail_view,
         name="worker-detail"),
    path("update-worker/<int:pk>/",
         WorkerUpdateView.as_view(),
         name="worker-update"),
    path("deadlines/",
         deadlines_view,
         name="deadlines"),
]

app_name = "task_manager"
