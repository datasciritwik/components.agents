# Agent Interaction Flow Diagram

```mermaid
graph TD
  UserInput[User Input] --> IntentClassifier[Intention Classifier]

  IntentClassifier -->|Explain| Teacher[Teacher Agent]
  IntentClassifier -->|Ask Doubt| DoubtSolver[Doubt Solver Agent]
  IntentClassifier -->|Take Test| Examiner[Examiner Agent]
  IntentClassifier -->|Plan Study| Planner[Planner Agent]
  IntentClassifier -->|Take Notes| NoteTaker[Note Taker Agent]

  Teacher --> CheckConfusion{User Confused?}
  CheckConfusion -- Yes --> DoubtSolver
  CheckConfusion -- No --> MemoryManager[Memory Manager]

  DoubtSolver --> MemoryManager
  Examiner -->|User struggles| Teacher
  Examiner --> MemoryManager
  Planner --> MemoryManager
  NoteTaker --> MemoryManager

  MemoryManager --> TokenCheck{STM Token Limit Exceeded?}
  TokenCheck -- Yes --> Summarize[Summarize & Store in LTM]
  TokenCheck -- No --> ResponseGen[Generate Response]

  Summarize --> ResponseGen
  ResponseGen --> UserOutput[Output to User]

  UserOutput -->|Follow-up| UserInput
```

### Agent Descriptions

* **Teacher Agent**
  Explains concepts clearly by retrieving and synthesizing knowledge from user-uploaded documents. Acts like a personalized tutor.

* **Doubt Solver Agent**
  Handles specific questions and clarifications by leveraging document embeddings and conversational context to resolve learner doubts effectively.

* **Examiner Agent**
  Creates and evaluates quizzes or tests based on the learned material, helping users assess their understanding and track progress.

* **Planner Agent**
  Designs personalized study plans and schedules by analyzing user goals and learning history to optimize study efficiency.

* **Note Taker Agent**
  Converts interactions, summaries, and key points into structured notes, enabling easy review and retention over time.

* **Memory Manager Agent**
  Oversees short-term and long-term memory, summarizing and storing conversations to maintain context and enable multi-session learning.
