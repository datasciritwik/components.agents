# Agent Interaction Flow Diagram [Project Path is unclear, that's why on hold]
- If you're a researcher and don't like reading too many research papers, then plz contact me will do some automation where we try to optimise the overall learning pipeline of knowledge gain by minimising effort.
- [Email](mailto:officialritwik098@gmail.com)

```mermaid
graph TD
  START((Start)) --> UserInput[User Input]
  UserInput --> IntentClassifier[Intention Classifier]

  IntentClassifier -->|Trigger Plan| PlanExecutor[Plan Executor]
  IntentClassifier -->|Free Input| ActionSelector[Action Selector-RAG]

  %% Plan executor flows like a proactive agent
  PlanExecutor --> ActionSelector

  %% Central decision-making unit
  ActionSelector -->|Explain| Teacher[Teacher Agent]
  ActionSelector -->|Ask Doubt| DoubtSolver[Doubt Solver Agent]
  ActionSelector -->|Take Test| Examiner[Examiner Agent]
  ActionSelector -->|Plan Study| Planner[Planner Agent]
  ActionSelector -->|Take Notes| NoteTaker[Note Taker Agent]
  ActionSelector -->|Unknown| Fallback[Fallback / Direct to Output]

  %% Agent interaction outcomes
  Teacher --> CheckConfusion{Is User Still Confused?}
  CheckConfusion -->|Yes| DoubtSolver
  CheckConfusion -->|No| IntermediateMemory[Memory Manager]

  DoubtSolver --> IntermediateMemory
  Examiner -->|User Struggles| Teacher
  Examiner --> IntermediateMemory
  Planner --> IntermediateMemory
  NoteTaker --> IntermediateMemory
  Fallback --> IntermediateMemory

  %% Memory & summarization logic
  IntermediateMemory --> TokenCheck{STM Token Limit Exceeded?}
  TokenCheck -->|Yes| Summarizer[Summarize & Store in LTM]
  TokenCheck -->|No| Refiner[Summarize & Correct Output]

  Summarizer --> Refiner

  %% Evaluate result quality
  Refiner --> Evaluator[Evaluate Result Quality]
  Evaluator -->|Good Enough| UserOutput[Output to User]
  Evaluator -->|Needs Work| RetryCheck{Retries Left?}
  RetryCheck -->|Yes| ActionSelector
  RetryCheck -->|No| UserOutput

  %% Close the loop
  UserOutput -->|Follow-up| UserInput
  UserOutput --> END((End))
```

``` mermaid
flowchart TD
  START((Start)) --> UserInput[User Provides Topic]

  UserInput --> OutlineGen[Generate High‑Level Outline]
  OutlineGen --> Approval{User Approves Outline?}
  
  Approval -->|No| OutlineEdit[User Updates Suggestions]
  OutlineEdit --> OutlineGen
  
  Approval -->|Yes| LoopStart([Begin Teaching Loop])

  subgraph Loop [Looping Over Each Subtopic]
    LoopStart --> Teach[Teacher Agent Explains Subtopic]
    Teach --> Notes[Note Generator Summarizes]
    Notes --> DepthCheck{Depth Sufficient?}
    DepthCheck -->|No| AutoQ[Auto‑Generate Deeper Follow‑Up]
    AutoQ --> Teach
    DepthCheck -->|Yes| NextSub{More Subtopics?}
    NextSub -->|Yes| LoopStart
    NextSub -->|No| LoopEnd([Loop Complete])
  end

  LoopEnd --> Results[Compile & Return Final Explanation + Notes]
  Results --> END((End))
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
