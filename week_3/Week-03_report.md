# Week 03 Assignment  
**Title:** Advanced Prompting: Zero-Shot, Few-Shot, and Chain-of-Thought (CoT)

---

## Overview
This week’s task was to explore different prompting strategies — **Zero-Shot, Few-Shot, and Chain-of-Thought (CoT)** — and compare their effect on reasoning accuracy, clarity, and completeness.  
I selected three types of problems from the provided datasets:  
- **Math problem** (from math-problems.json)  
- **Logic puzzle** (from logic-puzzles.json)  
- **Reasoning question** (from reasoning-tasks.json)  

---

## Prompts & Outputs

### 1. Math Problem
**Dataset Question:**  
A train travels 120 km in 2 hours. What is its average speed?

**Zero-Shot Prompt:**  
> Problem: A train travels 120 km in 2 hours. What is its average speed?  
> Instruction: Answer the question clearly and directly.  

**Output:**  
> The average speed is 60 km/h.  

---

**Few-Shot Prompt:**  
> Example 1: A car travels 100 km in 2 hours → Answer: 50 km/h  
> Example 2: A runner covers 42 km in 3 hours → Answer: 14 km/h  
> Now solve this: A train travels 120 km in 2 hours.  

**Output:**  
> Speed = 120 / 2 = 60 km/h.  
> Answer: 60 km/h.  

---

**Chain-of-Thought Prompt:**  
> Problem: A train travels 120 km in 2 hours.  
> Instruction: Think step by step.  

**Output:**  
> Step 1: Distance = 120 km.  
> Step 2: Time = 2 hours.  
> Step 3: Speed = 120 ÷ 2 = 60 km/h.  
> Final Answer: 60 km/h.  

---

### 2. Logic Puzzle
**Dataset Question:**  
If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?

**Zero-Shot Output:**  
> Yes.  

**Few-Shot Output:**  
> Example 1: All cats are animals → All cats are living beings → Yes.  
> Example 2: All squares are rectangles but some rectangles are red → Not all squares are red → No.  
> Now problem: Bloops → Razzies → Lazzies → Yes, all Bloops are Lazzies.  

**CoT Output:**  
> Step 1: Bloops are a subset of Razzies.  
> Step 2: Razzies are a subset of Lazzies.  
> Step 3: Therefore, Bloops must also be a subset of Lazzies.  
> Final Answer: Yes, all Bloops are Lazzies.  

---

### 3. Reasoning Question
**Dataset Question:**  
Passage: “The sun provides energy to plants through photosynthesis. Animals eat plants to gain energy. This creates a food chain.”  
Question: What role does the sun play in the food chain?

**Zero-Shot Output:**  
> The sun is the primary source of energy in the food chain.  

**Few-Shot Output:**  
> Example 1: Water boils at 100°C → Answer: 100°C.  
> Example 2: Birds build nests to protect eggs → Answer: To protect eggs.  
> Now: The sun provides energy for plants → Plants feed animals → The sun is the primary source of energy in the food chain.  

**CoT Output:**  
> Step 1: Plants use sunlight to perform photosynthesis and produce chemical energy (food).  
> Step 2: Animals eat plants to obtain that stored energy.  
> Step 3: Because plants convert sunlight into the energy that supports consumers, the sun provides the initial energy input that drives the whole food chain.  
> Final Answer: The sun is the primary source of energy for the food chain, powering photosynthesis in plants which supports all other organisms.

---

## Evaluation (Rubric Scores)

| Task       | Method     | Correctness | Reasoning Clarity | Completeness | Conciseness | **Total** |
|------------|-----------|-------------|-------------------|--------------|-------------|-----------|
| Math       | Zero-Shot | 3           | 1                 | 1            | 3           | **8**     |
| Math       | Few-Shot  | 3           | 2                 | 2            | 3           | **10**    |
| Math       | CoT       | 3           | 3                 | 3            | 3           | **12**    |
| Logic      | Zero-Shot | 3           | 1                 | 1            | 3           | **8**     |
| Logic      | Few-Shot  | 3           | 2                 | 2            | 3           | **10**    |
| Logic      | CoT       | 3           | 3                 | 3            | 3           | **12**    |
| Reasoning  | Zero-Shot | 2           | 1                 | 1            | 2           | **6**     |
| Reasoning  | Few-Shot  | 3           | 2                 | 2            | 3           | **10**    |
| Reasoning  | CoT       | 3           | 3                 | 3            | 3           | **12**    |

---

## Comparative Insights
1. **Zero-Shot** worked only for straightforward tasks (math, simple logic). It often lacked reasoning detail and was too short.  
2. **Few-Shot** improved accuracy by showing the model patterns. It worked well for logic and reasoning tasks, but sometimes still gave short reasoning.  
3. **Chain-of-Thought (CoT)** gave the **most reliable and complete answers**. It forced the model to break down the steps, which improved correctness, clarity, and completeness.  

---

## Reflection
- CoT prompting consistently outperformed Zero-Shot and Few-Shot, especially for reasoning-heavy tasks.  
- Few-Shot was useful when the dataset question followed clear patterns.  
- Zero-Shot is the weakest when reasoning is required, but can be acceptable for direct fact questions.  
- Overall, **CoT prompting is the most powerful strategy for reasoning tasks** because it structures the model’s thought process.  

---
