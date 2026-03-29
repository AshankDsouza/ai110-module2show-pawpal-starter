# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The scheduluer controls User and indirectly iteracts with and organizes



- What classes did you include, and what responsibilities did you assign to each?
Classes: Owner, Scheduler, Pet and Task

Responsibilities:
Owner - adds pets, schedules walks, and views today's tasks.
Scheduler - collects and sorts tasks across all pets.
Pet - stores pet info and its task list.
Task - stores one activity's details and completion status.


Copilot Instructions: 
 Copilot to create a Mermaid.js class diagram based on your brainstormed attributes and methods.

Owner
three core actions a Owner should be able to perform:
 1) add a pet
 2) schedule a walk
 3) see today's tasks


UML Relations:
Owner has Pets --> This means an owner should have pets attribute

Task: Represents a single activity (description, time, frequency, completion status).
Pet: Stores pet details and a list of tasks.

Owner: Manages multiple pets and provides access to all their tasks.
Scheduler: The "Brain" that retrieves, organizes, and manages tasks across pets.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

 I also expanded Scheduler beyond simple aggregation/sorting by adding filter_tasks, mark_task_complete, and detect_conflicts. The new changes with respect to algorithms was made to make the scheduling cleaner and keep the logic part away from the UI part. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler currently considers: time, completion status and time conflicts. 

I prioritized these because they map directly to the core owner workflow: know what is due, in what order, and whether schedule collisions exist.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that conflict detection only checks instead of overlapping time windows. This makes the algorithm simple and fast to reason about.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot for testing (generate tests), making the skeleton, making meaningful commits (generate commits) and also for the in code documentation (docstring). 

I also used separate chat focus by phase, which avoided confusing Copilot. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

AI could not make the images. I had to do this manually. Also, Copilot did not recommened to use clean image organization (keeping images in its own folder), I decided to do this even though i did not get any prompt from the AI. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested:
 1) task completion state updates
 2) adding tasks to pets
 3) sorting tasks by time
 4) conflict detection for duplicate times

and others as well.

These tests were important because now we can refactor and extend the code and avoid breaking correct behaviour. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence: Very high for current scope, based on passing automated tests and manual CLI checks.

Next edge cases I would test:

1) Duplicate names 
2) Pet owning conditions like should own at least one pet
3) State management --invalid states should not be reachable(negative no. of pets, negative no. of tasks)

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with keeping scheduling logic centralized in `Scheduler` and keeping UI logic separate -- this follows separation of concerns keeping things clean and extensible for future modeifications. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add task durations and task priority. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Testing is important. And we can check for correct behaviour by writing tests and also we can use tests as a prompt and additional context that is affored to the AI. 
