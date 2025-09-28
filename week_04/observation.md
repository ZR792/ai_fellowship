#### Experiment: Effect of Temperature on Summarization

I tested the summarization of a news article using Gemini 1.5 Flash at three different temperatures: 0.1, 0.7, and 1.0. The goal was to observe how the summaries differ in style, creativity, and consistency.

🔹 Temperature = 0.1 (Deterministic / Robotic)

- The summary was very factual, short, and to the point.

- It avoided unnecessary detail and stuck closely to the article text.

- The output felt a bit “robotic” and sometimes repetitive.

**Example behavior:** listing facts without transitions.

**Best for:** tasks where accuracy and consistency are critical.

🔹 Temperature = 0.7 (Balanced / Natural)

The summary was concise but also readable.

It included all the important details while keeping the sentences natural.

Flow was better compared to 0.1, with smoother transitions.

This setting produced the most useful and balanced summaries.

**Best for:** general summarization, where both clarity and readability matter.

🔹 Temperature = 1.0 (Creative / Variable)

The summary was more expressive and sometimes rephrased things creatively.

It occasionally added emphasis (e.g., “a major milestone in space exploration”).

However, it sometimes introduced minor details that were not in the text or skipped smaller facts.

Felt more like a storytelling style than a strict summary.

**Best for:** fun summaries or creative writing tasks, not for precise reporting.

### Conclusion:

- 0.1 → Accurate but robotic.

- 0.7 → Balanced and most useful.

- 1.0 → Creative but less reliable.

*For this project, I found temperature = 0.7 gave the best results for summarizing news articles.*