from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_scheduler_sort_and_filter_tasks() -> None:
	owner = Owner("Alex")
	buddy = Pet(name="Buddy", species="Dog", age=4)
	luna = Pet(name="Luna", species="Dog", age=2)
	owner.add_pet(buddy)
	owner.add_pet(luna)
	scheduler = Scheduler()

	base = datetime(2026, 3, 29, 8, 0)
	b_task = Task(description="Buddy walk", scheduled_time=base.replace(hour=19), frequency="daily")
	l_task = Task(description="Luna feed", scheduled_time=base.replace(hour=12), frequency="once")
	buddy.add_task(b_task)
	luna.add_task(l_task)

	sorted_tasks = scheduler.sort_by_time(scheduler.collect_tasks(owner))
	assert [task.description for task in sorted_tasks] == ["Luna feed", "Buddy walk"]

	b_task.mark_complete()
	filtered = scheduler.filter_tasks(owner, pet_name="Buddy", completed=True)
	assert len(filtered) == 1
	assert filtered[0].description == "Buddy walk"


def test_mark_task_complete_creates_next_daily_task() -> None:
	scheduler = Scheduler()
	pet = Pet(name="Buddy", species="Dog", age=4)
	task = Task(
		description="Morning walk",
		scheduled_time=datetime(2026, 3, 29, 8, 0),
		frequency="daily",
	)
	pet.add_task(task)

	next_task = scheduler.mark_task_complete(pet, task)

	assert task.completed is True
	assert next_task is not None
	assert next_task.scheduled_time == datetime(2026, 3, 30, 8, 0)
	assert len(pet.tasks) == 2


def test_detect_conflicts_returns_warning_for_same_time() -> None:
	owner = Owner("Alex")
	buddy = Pet(name="Buddy", species="Dog", age=4)
	luna = Pet(name="Luna", species="Dog", age=2)
	owner.add_pet(buddy)
	owner.add_pet(luna)
	scheduler = Scheduler()

	conflict_time = datetime(2026, 3, 29, 8, 0)
	buddy.add_task(Task(description="Morning walk", scheduled_time=conflict_time, frequency="daily"))
	luna.add_task(Task(description="Morning meds", scheduled_time=conflict_time, frequency="daily"))

	conflicts = scheduler.detect_conflicts(owner)

	assert len(conflicts) == 1
	assert "Conflict" in conflicts[0]
	assert "Buddy: Morning walk" in conflicts[0]
	assert "Luna: Morning meds" in conflicts[0]
