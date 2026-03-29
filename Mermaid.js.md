classDiagram
    class Owner {
        -name: str
        -pets: List~Pet~
        +add_pet(pet: Pet): void
        +schedule_walk(pet_name: str, time: datetime, frequency: str): Task
        +see_todays_tasks(): List~Task~
    }

    class Pet {
        -name: str
        -species: str
        -age: int
        -tasks: List~Task~
        +add_task(task: Task): void
        +get_todays_tasks(): List~Task~
    }

    class Task {
        -description: str
        -scheduled_time: datetime
        -frequency: str
        -completed: bool
        +mark_complete(): void
        +is_due_on(date: date): bool
    }

    class Scheduler {
        +sort_by_time(tasks: List~Task~): List~Task~
        +filter_tasks(owner: Owner, pet_name: str, completed: bool): List~Task~
        +collect_tasks(owner: Owner): List~Task~
        +organize_tasks(tasks: List~Task~): List~Task~
        +mark_task_complete(pet: Pet, task: Task): Task
        +detect_conflicts(owner: Owner): List~str~
        +today_plan(owner: Owner): List~Task~
    }

    Owner "1" o-- "0..*" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Scheduler ..> Owner : reads
    Scheduler ..> Pet : aggregates
    Scheduler ..> Task : organizes