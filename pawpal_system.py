
# This will be the "logic layer" where all your backend classes live.

# The real life entities:


# Task: Represents a single activity (description, time, frequency, completion status).

# Pet: Stores pet details and a list of tasks.

# Owner: Manages multiple pets and provides access to all their tasks.

# Scheduler: The "Brain" that retrieves, organizes, and manages tasks across pets.

# Copilot instructions:
#  Copilot to use Python Dataclasses for objects like Task and Pet to keep your code clean.

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List


@dataclass
class Task:
	description: str
	scheduled_time: datetime
	frequency: str
	completed: bool = False

	def mark_complete(self) -> None:
		pass

	def is_due_on(self, target_date: date) -> bool:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def get_todays_tasks(self) -> List[Task]:
		pass


class Owner:
	def __init__(self, name: str) -> None:
		self.name = name
		self.pets: List[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		pass

	def schedule_walk(self, pet_name: str, walk_time: datetime, frequency: str) -> Task:
		pass

	def see_todays_tasks(self) -> List[Task]:
		pass


class Scheduler:
	def collect_tasks(self, owner: Owner) -> List[Task]:
		pass

	def organize_tasks(self, tasks: List[Task]) -> List[Task]:
		pass

	def today_plan(self, owner: Owner) -> List[Task]:
		pass
