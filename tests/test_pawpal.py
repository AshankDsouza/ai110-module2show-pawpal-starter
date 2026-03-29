from datetime import datetime

from pawpal_system import Pet, Task


def test_task_completion_marks_task_as_completed() -> None:
	task = Task(
		description="Morning walk",
		scheduled_time=datetime.now(),
		frequency="daily",
	)

	assert task.completed is False
	task.mark_complete()
	assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
	pet = Pet(name="Buddy", species="Dog", age=4)
	initial_count = len(pet.tasks)

	task = Task(
		description="Evening walk",
		scheduled_time=datetime.now(),
		frequency="daily",
	)
	pet.add_task(task)

	assert len(pet.tasks) == initial_count + 1
	assert pet.tasks[-1] is task
