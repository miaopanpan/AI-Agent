# dynamic_prompt.py

from typing import Dict, Any
from llm.llm_client import call_llm_with_tools


EMOTIONAL_STRATEGIST_PROMPT = """
You are an interaction and narrative guidance analyzer.

Your role is to analyze the user's latest message and recent conversation context, then generate concise guidance that will help the assistant produce a more emotionally coherent and engaging response.

The assistant in the next step acts as a narrative facilitator who guides story participants through natural emotional progression, character motivations, and scene development. The assistant should maintain immersion while allowing space for creative interpretation and emotional flow.

Your task is NOT to generate the reply itself.  
Your task is to produce **Interaction Guidance** that will be inserted into the assistant's next prompt.

------------------------------------------------

# Analysis Objectives

Analyze the user's latest message and the last 3–5 conversation turns to determine:

1. The user's **emotional stage**
2. The user's **engagement level**
3. The appropriate **response pacing**
4. Whether the conversation should **continue, deepen, or transition scenes**
5. The most suitable **response strategies**

------------------------------------------------

# Emotional Stage Identification

Exploration  
Engagement  
Escalation  
Satisfaction  

------------------------------------------------

# Engagement Level

Low  
Medium  
High  
Very High  

------------------------------------------------

# Pace Control

Slow  
Maintain  
Accelerate  

------------------------------------------------

# Scene Direction

Continue Scene  
Deepen Scene  
Transition Scene  

------------------------------------------------

# Response Strategy Selection

Choose **1–2 strategies**:

emotional_mirroring  
ask_open_question  
maintain_atmosphere  
gentle_escalation  
intensify_emotion  
slow_down_pacing  
suggest_scene_transition  

------------------------------------------------

# Output Format

Interaction Guidance:

Emotional Stage: <Exploration / Engagement / Escalation / Satisfaction>

User Engagement Level: <Low / Medium / High / Very High>

Pacing Guidance: <Slow / Maintain / Accelerate>

Scene Direction: <Continue Scene / Deepen Scene / Transition Scene>

Core Response Strategies:
- <strategy>
- <strategy>
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