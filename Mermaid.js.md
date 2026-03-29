classDiagram
    class User {
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
        +get_todays_tasks(date: date): List~Task~
    }

    class Task {
        -description: str
        -time: datetime
        -frequency: str
        -completed: bool
        +mark_complete(): void
        +is_due_on(date: date): bool
    }

    class Scheduler {
        +collect_tasks(user: User): List~Task~
        +organize_tasks(tasks: List~Task~): List~Task~
        +today_plan(user: User): List~Task~
    }

    User "1" o-- "0..*" Pet : owns
    Pet "1" o-- "0..*" Task : has
    Scheduler ..> User : reads
    Scheduler ..> Pet : aggregates
    Scheduler ..> Task : organizes