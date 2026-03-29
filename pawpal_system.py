
# This will be the "logic layer" where all your backend classes live.

# The real life entities:


# Task: Represents a single activity (description, time, frequency, completion status).

# Pet: Stores pet details and a list of tasks.

# Owner: Manages multiple pets and provides access to all their tasks.

# Scheduler: The "Brain" that retrieves, organizes, and manages tasks across pets.

# Copilot instructions:
#  Copilot to use Python Dataclasses for objects like Task and Pet to keep your code clean.

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
	description: str
	scheduled_time: datetime
	frequency: str
	completed: bool = False

	def mark_complete(self) -> None:
		self.completed = True

	def is_due_on(self, target_date: date) -> bool:
		"""
		Determines if the task is due on the given target_date, based on its
		frequency (daily, weekly, monthly, or one-time). Returns True if the
		task is scheduled or recurring on that date, otherwise False.
		"""
		frequency = self.frequency.strip().lower()
		scheduled_date = self.scheduled_time.date()

		if frequency == "daily":
			return target_date >= scheduled_date

		if frequency == "weekly":
			if target_date < scheduled_date:
				return False
			return (target_date - scheduled_date).days % 7 == 0

		if frequency == "monthly":
			return target_date >= scheduled_date and target_date.day == scheduled_date.day

		# Default behavior for one-time or unknown frequency values
		return target_date == scheduled_date


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		self.tasks.append(task)

	def get_todays_tasks(self) -> List[Task]:
		"""
		Returns a list of incomplete Task objects from self.tasks that are due
		today.
		"""
		today = date.today()
		return [task for task in self.tasks if task.is_due_on(today) and not task.completed]


class Owner:
	def __init__(self, name: str) -> None:
		self.name = name
		self.pets: List[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		"""
		Appends the given pet to the owner's pets list.
		"""
		self.pets.append(pet)

	def schedule_walk(self, pet_name: str, walk_time: datetime, frequency: str) -> Task:
		"""
		Schedules a walk task for the specified pet by name at the given
		walk_time and frequency. Returns the created Task if the pet is found;
		raises ValueError if the pet does not exist for the owner.
		"""
		for pet in self.pets:
			if pet.name.lower() == pet_name.lower():
				task = Task(description="Walk", scheduled_time=walk_time, frequency=frequency)
				pet.add_task(task)
				return task

		raise ValueError(f"Pet '{pet_name}' not found for owner '{self.name}'.")

	def see_todays_tasks(self) -> List[Task]:
		"""
		Returns a list of today's tasks for all pets owned by the user, sorted
		by each task's scheduled_time.
		"""
		tasks: List[Task] = []
		for pet in self.pets:
			tasks.extend(pet.get_todays_tasks())
		return sorted(tasks, key=lambda task: task.scheduled_time)


class Scheduler:
	def sort_by_time(self, tasks: List[Task]) -> List[Task]:
		"""
		Returns a new list of Task objects sorted by scheduled_time.
		"""
		return sorted(tasks, key=lambda task: task.scheduled_time)

	def filter_tasks(
		self,
		owner: Owner,
		pet_name: Optional[str] = None,
		completed: Optional[bool] = None,
	) -> List[Task]:
		"""
		Returns tasks filtered by optional pet name and completion status.

		If pet_name is provided, matching is case-insensitive. If completed is
		provided, only tasks with that completion state are returned.
		"""
		filtered: List[Task] = []
		for pet in owner.pets:
			if pet_name is not None and pet.name.lower() != pet_name.lower():
				continue
			for task in pet.tasks:
				if completed is not None and task.completed != completed:
					continue
				filtered.append(task)

		return self.sort_by_time(filtered)

	def collect_tasks(self, owner: Owner) -> List[Task]:
		"""
		Returns a list of all Task objects associated with the pets owned by the
		given owner. Iterates through each pet and aggregates their tasks into a
		single list.
		"""
		all_tasks: List[Task] = []
		for pet in owner.pets:
			all_tasks.extend(pet.tasks)
		return all_tasks

	def organize_tasks(self, tasks: List[Task]) -> List[Task]:
		"""
		Sorts the given list of Task objects by their completed status and
		scheduled_time, returning the ordered list.
		"""
		return sorted(tasks, key=lambda task: (task.completed, task.scheduled_time))

	def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
		"""
		Marks a task complete and auto-creates the next recurring task when the
		frequency is daily or weekly.

		Returns the newly created recurring task, or None when no new task is
		created.
		"""
		if task not in pet.tasks:
			raise ValueError(f"Task '{task.description}' not found for pet '{pet.name}'.")

		if task.completed:
			return None

		task.mark_complete()

		frequency = task.frequency.strip().lower()
		next_time: Optional[datetime] = None
		if frequency == "daily":
			next_time = task.scheduled_time + timedelta(days=1)
		elif frequency == "weekly":
			next_time = task.scheduled_time + timedelta(weeks=1)

		if next_time is None:
			return None

		next_task = Task(
			description=task.description,
			scheduled_time=next_time,
			frequency=task.frequency,
		)
		pet.add_task(next_task)
		return next_task

	def detect_conflicts(self, owner: Owner) -> List[str]:
		"""
		Returns warning messages for tasks that share the exact same scheduled
		time across all pets.

		This is a lightweight strategy and only checks exact datetime matches.
		"""
		time_buckets: Dict[datetime, List[Tuple[str, Task]]] = {}
		for pet in owner.pets:
			for task in pet.tasks:
				time_buckets.setdefault(task.scheduled_time, []).append((pet.name, task))

		warnings: List[str] = []
		for conflict_time, scheduled_items in sorted(time_buckets.items(), key=lambda item: item[0]):
			if len(scheduled_items) < 2:
				continue

			details = ", ".join(
				f"{pet_name}: {task.description}" for pet_name, task in scheduled_items
			)
			warnings.append(
				f"Conflict at {conflict_time.strftime('%Y-%m-%d %I:%M %p')} -> {details}"
			)

		return warnings

	def today_plan(self, owner: Owner) -> List[Task]:
		"""
		Returns a list of Task objects for the given owner that are due today
		and not completed, organized using organize_tasks.
		"""
		today = date.today()
		todays_tasks = [
			task for task in self.collect_tasks(owner) if task.is_due_on(today) and not task.completed
		]
		return self.organize_tasks(todays_tasks)
