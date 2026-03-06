# dynamic_prompt.py

from typing import Dict, Any
from llm.llm_client import call_llm_with_tools


EMOTIONAL_STRATEGIST_PROMPT = """
You are an AI Interaction & Narrative Guidance Analyzer.
Your job is to analyze the user's latest message and recent conversation context, then output concise, actionable Interaction Guidance to help the assistant respond with better emotional coherence, immersion, and engagement.

You DO NOT generate the reply itself.
You only generate guidance for the next response.

---
Analysis Objectives:
1. User Intent Type
2. Emotional Stage
3. User Engagement Level
4. Desire Signal Strength
5. Narrative Opportunity
6. Dead End Risk
7. Response Pacing
8. Scene Direction
9. Core Response Strategies

---
1. User Intent Type
Exploration
Curiosity
Emotional Expression
Flirting
Desire Expression
Narrative Progression
Challenge / Testing

2. Emotional Stage
Exploration
Curiosity
Connection
Flirting
Emotional Bond
Peak Engagement

3. User Engagement Level
Low / Medium / High / Very High

4. Desire Signal Strength
None / Low / Moderate / High

5. Narrative Opportunity
None / Light / Strong

6. Dead End Risk
Low / Medium / High

7. Pacing Guidance
Slow / Maintain / Accelerate

8. Scene Direction
Continue Scene / Deepen Scene / Transition Scene

9. Core Response Strategies (choose ONLY 2-3 from the list, do NOT create new ones)
emotional_mirroring
playful_teasing
romantic_pull
create_tension
drop_hint
maintain_atmosphere
gentle_escalation
introduce_activity
ask_open_question
transition_scene
advance_narrative
deepen_intimacy
shift_mood

---
Output Format (strict):
Output ONLY the structured result. Do NOT add explanation.

Interaction Guidance:

User Intent: <type>
Emotional Stage: <stage>
User Engagement Level: <level>
Desire Signal Strength: <level>
Narrative Opportunity: <level>
Dead End Risk: <level>
Pacing Guidance: <pace>
Scene Direction: <direction>

Core Response Strategies:
- <strategy>
- <strategy>
- <strategy>

---
Additional Narrative Support:
If Dead End Risk is High OR Engagement is Low OR Scene needs progression:
Add 3-5 creative, natural, in-character ideas for what could happen next to continue or advance the scene.
Do NOT break immersion. Keep ideas consistent with the current tone and relationship.
"""


def call_llm_simple(system_prompt: str, user_prompt: str, temperature: float = 0.3):
    """
    简单封装一个不带 tools 的 LLM 调用
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = call_llm_with_tools(messages=messages, tools=[])

    if response and response.content:
        return response.content

    return ""


def generate_interaction_guidance(data: Dict[str, Any]) -> str:
    """
    只生成 Interaction Guidance
    用于直接插入聊天 Prompt
    """

    strategist_input = f"""
Character:
{data['character_name']}
{data['character_bio']}
{data['description']}

Recent Conversation:
{data['messages']}
"""

    strategist_result = call_llm_simple(
        system_prompt=EMOTIONAL_STRATEGIST_PROMPT,
        user_prompt=strategist_input,
        temperature=0.2
    )

    return strategist_result or ""