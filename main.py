from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Task


def main() -> None:
	# Create owner and pets
	owner = Owner("Alex")
	buddy = Pet(name="Buddy", species="Dog", age=4)
	luna = Pet(name="Luna", species="Dog", age=2)

	owner.pets.append(buddy)
	owner.pets.append(luna)

	# Add tasks with different times (all for today)
	now = datetime.now()
	buddy.tasks.append(
		Task(description="Morning walk", scheduled_time=now.replace(hour=8, minute=0, second=0, microsecond=0), frequency="daily")
	)
	luna.tasks.append(
		Task(description="Afternoon walk", scheduled_time=now.replace(hour=14, minute=30, second=0, microsecond=0), frequency="daily")
	)
	buddy.tasks.append(
		Task(description="Evening walk", scheduled_time=now.replace(hour=19, minute=15, second=0, microsecond=0), frequency="daily")
	)

	# Print today's schedule
	todays_tasks = []
	for pet in owner.pets:
		for task in pet.tasks:
			if task.scheduled_time.date() == now.date():
				todays_tasks.append((task.scheduled_time, pet.name, task))

	todays_tasks.sort(key=lambda item: item[0])

	print("Today's Schedule")
	print("=" * 20)
	for task_time, pet_name, task in todays_tasks:
		print(f"{task_time.strftime('%I:%M %p')} - {pet_name}: {task.description} ({task.frequency})")


if __name__ == "__main__":
	main()