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

Yes. I renamed `User` to `Owner` to better match the scenario language and made the responsibilities clearer. I also expanded `Scheduler` beyond simple aggregation/sorting by adding `filter_tasks`, `mark_task_complete`, and `detect_conflicts`. This change happened because once I started implementing real scheduling behavior, it was cleaner to keep algorithmic decisions in one class rather than scattering them across UI code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler currently considers:

- task date/time ordering
- completion status
- pet-based filtering
- recurrence frequency (`daily`, `weekly`, `monthly`, `once`)
- exact-time conflicts across all pets

I prioritized these because they map directly to the core owner workflow: know what is due, in what order, and whether schedule collisions exist.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that conflict detection only checks **exact matching datetimes** instead of overlapping time windows. This makes the algorithm simple and fast to reason about (group by timestamp and flag groups larger than one), which is reasonable for a beginner-friendly pet-care scheduler where tasks are short and usually anchored to specific times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot for planning, implementation drafts, and test expansion. The most useful prompts were specific and constraint-driven, for example:

- "Add a lightweight conflict detection strategy that returns warnings, not errors."
- "Implement recurring task creation when a daily/weekly task is completed."
- "Suggest edge cases for scheduler tests."

I also used separate chat focus by phase (implementation vs testing vs documentation), which reduced context switching and kept decisions organized.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One AI suggestion favored a compact list-comprehension-heavy filter implementation. I modified it to a more explicit loop-based version because readability was more important for this project. I verified behavior by adding focused tests for filtering and re-running `pytest` after the refactor.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested:

- task completion state updates
- adding tasks to pets
- sorting tasks by time
- filtering by pet/status
- recurring task creation for daily completion
- conflict detection for duplicate times
- no-task and no-conflict edge cases

These tests were important because each one protects a core user-facing behavior from regressions and confirms the scheduler logic is deterministic.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence: **5/5** for current scope, based on passing automated tests and manual CLI checks.

Next edge cases I would test:

- monthly recurrence behavior around short months
- timezone-aware datetime handling
- duplicate pets with same name validation
- conflict detection for overlapping durations (not just exact start times)

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with keeping scheduling logic centralized in `Scheduler` while still exposing it clearly in the Streamlit UI.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add task durations and priority weights, then upgrade conflict detection from exact timestamp matching to interval overlap detection.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The key takeaway is that AI accelerates coding, but the human still has to be the lead architect: define boundaries, enforce readability, and verify correctness with tests.
