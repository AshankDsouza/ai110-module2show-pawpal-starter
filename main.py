from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
	# Create owner, pets, and scheduler
	owner = Owner("Alex")
	scheduler = Scheduler()
	buddy = Pet(name="Buddy", species="Dog", age=4)
	luna = Pet(name="Luna", species="Dog", age=2)

	owner.add_pet(buddy)
	owner.add_pet(luna)

	# Add tasks out of order (all for today)
	now = datetime.now()
	buddy.add_task(
		Task(description="Evening walk", scheduled_time=now.replace(hour=19, minute=15, second=0, microsecond=0), frequency="daily")
	)
	luna.add_task(
		Task(description="Lunch feed", scheduled_time=now.replace(hour=12, minute=0, second=0, microsecond=0), frequency="once")
	)
	buddy.add_task(
		Task(description="Morning walk", scheduled_time=now.replace(hour=8, minute=0, second=0, microsecond=0), frequency="daily")
	)

	# Intentional conflict (same time for different pets)
	luna.add_task(
		Task(description="Vet reminder", scheduled_time=now.replace(hour=8, minute=0, second=0, microsecond=0), frequency="weekly")
	)

	print("All tasks sorted by time")
	print("=" * 20)
	for task in scheduler.sort_by_time(scheduler.collect_tasks(owner)):
		print(f"{task.scheduled_time.strftime('%I:%M %p')} - {task.description} ({task.frequency})")

	print("\nIncomplete tasks for Buddy")
	print("=" * 30)
	buddy_open_tasks = scheduler.filter_tasks(owner, pet_name="Buddy", completed=False)
	for task in buddy_open_tasks:
		print(f"{task.scheduled_time.strftime('%I:%M %p')} - {task.description}")

	print("\nMarking Buddy's morning walk complete...")
	morning_walk = next(task for task in buddy.tasks if task.description == "Morning walk")
	next_occurrence = scheduler.mark_task_complete(buddy, morning_walk)
	if next_occurrence:
		print(
			f"Created recurring task for {next_occurrence.scheduled_time.strftime('%Y-%m-%d %I:%M %p')}"
		)

	print("\nConflict warnings")
	print("=" * 20)
	conflicts = scheduler.detect_conflicts(owner)
	if not conflicts:
		print("No conflicts detected.")
	else:
		for warning in conflicts:
			print(f"⚠️  {warning}")


if __name__ == "__main__":
	main()