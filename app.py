
"""
Phase 3: UI and Backend Integration

Currently, your logic (pawpal_system.py) and your user interface (app.py) live in separate worlds. In this phase, you will act as the "bridge" to ensure that when a user clicks a button in the app, your Python classes actually respond.

Step 1: Establish the Connection

To use the Owner, Pet, and Task classes inside your Streamlit script, you must first make them accessible.

Use a Python import statement to bring specific classes from pawpal_system.py into app.py.
Step 2: Manage the Application "Memory"

Streamlit is stateless, meaning it runs your code from top to bottom every time you click a button. If you simply create an Owner at the top of the script, it will be "reborn" (and empty) every time the page refreshes.


Use AI to investigate st.session_state. Find out how to check if an object (like your Owner instance) already exists in the "vault" of the session before creating a new one.

Think of st.session_state as a dictionary. You want to store your Owner object there so your data persists while you navigate the app.
Step 3: Wiring UI Actions to Logic


Locate the UI components for "Adding a Pet" or "Scheduling a Task" in app.py. Replace those placeholders with calls to the methods you wrote in Phase 2.

If a user submits a form to add a new pet, which class method should handle that data, and how does the UI get updated to show the change?
📍Checkpoint: Your app.py successfully imports your logic layer! Adding a pet in the browser actually creates a Pet object that stays in memory.

"""


import streamlit as st
from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Session memory for backend objects
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

st.markdown("### Add a Pet")
pet_col1, pet_col2, pet_col3 = st.columns(3)
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with pet_col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with pet_col3:
    age = st.number_input("Age", min_value=0, max_value=40, value=2)

if st.button("Add pet"):
    if not pet_name.strip():
        st.error("Please provide a pet name.")
    elif any(existing_pet.name.lower() == pet_name.strip().lower() for existing_pet in owner.pets):
        st.warning("A pet with that name already exists.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
        st.success(f"Added pet: {pet_name.strip()}")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age, "task_count": len(pet.tasks)}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add a Task")
st.caption("This now creates real Task objects in your backend classes.")

if owner.pets:
    task_col1, task_col2, task_col3 = st.columns(3)
    with task_col1:
        selected_pet_name = st.selectbox("Choose pet", [pet.name for pet in owner.pets])
    with task_col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with task_col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly", "monthly"], index=1)

    task_time = st.time_input("Task time")

    if st.button("Add task"):
        selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)
        if selected_pet is None:
            st.error("Selected pet not found.")
        elif not task_title.strip():
            st.error("Please provide a task title.")
        else:
            scheduled_datetime = datetime.combine(datetime.today().date(), task_time)
            selected_pet.add_task(
                Task(
                    description=task_title.strip(),
                    scheduled_time=scheduled_datetime,
                    frequency=frequency,
                )
            )
            st.success(f"Added task for {selected_pet.name}: {task_title.strip()}")
else:
    st.info("Add a pet first to start assigning tasks.")

all_tasks = [
    {
        "pet": pet.name,
        "task": task.description,
        "time": task.scheduled_time.strftime("%I:%M %p"),
        "frequency": task.frequency,
        "completed": task.completed,
    }
    for pet in owner.pets
    for task in pet.tasks
]

if all_tasks:
    st.write("Current tasks:")
    st.table(all_tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This calls your Scheduler and displays today's plan.")

if st.button("Generate schedule"):
    todays_plan = scheduler.today_plan(owner)
    if todays_plan:
        st.success("Today's schedule generated.")
        st.table(
            [
                {
                    "task": task.description,
                    "time": task.scheduled_time.strftime("%I:%M %p"),
                    "frequency": task.frequency,
                    "completed": task.completed,
                }
                for task in todays_plan
            ]
        )
    else:
        st.info("No tasks due today yet.")
