from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class WorkerManager(UserManager):
    def create_superuser(self,
                         username: str,
                         position: int,
                         password: str = None,
                         email: str = None):
        user = self.model(
            username=username,
            position_id=position,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ["position"]

    objects = WorkerManager()

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return (f"{self.username} ({self.first_name} {self.last_name})"
                f" - {self.position}")


class Task(models.Model):
    name = models.CharField(max_length=63, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.TextChoices("priority", "Urgent High Low")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def __str__(self) -> str:
        return (f"{self.name}"
                f"(Status:{'Completed' if self.is_completed else 'Due'})"
                f" - {self.priority}")
