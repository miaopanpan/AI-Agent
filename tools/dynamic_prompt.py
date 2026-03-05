# dynamic_prompt.py

from typing import Dict, Any
from llm.llm_client import call_llm_with_tools


EMOTIONAL_STRATEGIST_PROMPT = """
You are the Emotional Progression & Intent Strategist in a role-playing chat system.

Your responsibility is not only to analyze user intent, but to determine:

- Relationship progression stage
- Emotional intensity level
- Desire escalation speed
- Scene transition readiness
- Whether to satisfy, delay, redirect, or deepen

Your goal is to protect narrative rhythm, maintain immersion, and optimize emotional payoff pacing.

Never create abrupt progression.
Never shut down user enthusiasm.
Never escalate without emotional groundwork.

Core Evaluation Framework

1️⃣ Intent Classification
2️⃣ Emotional State & Intensity Level (0-5 Scale)
3️⃣ Relationship Stage Detection (1-5)
4️⃣ Escalation Decision Logic
5️⃣ Scene Transition Check

Output Format (STRICT):
Role response direction: ...
Points to focus on: ...
"""


PROMPT_ENGINEER_TEMPLATE = """
As an AI prompting engineer, generate a new dynamic system prompt
based on the chat logs and role data below
to improve future chat interactions.

Return ONLY the generated prompt.

Character Data:
{character_data}

Chat Logs:
{chat_logs}
"""


def call_llm_simple(system_prompt: str, user_prompt: str, temperature: float = 0.3):
    """
    简单封装一个不带tools的LLM调用
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = call_llm_with_tools(messages=messages, tools=[])

    if response and response.content:
        return response.content

    return ""


def should_generate_new_prompt(strategy_output: str) -> bool:
    strategy_output = strategy_output.lower()

    print("Emotional Strategist Output:", strategy_output)
    trigger_keywords = [
        "stabilize",
        "redirect",
        "slow",
        "challenge",
        "deep",
        "escalation exceeded",
        "slow escalation",
        "delay"
    ]

    return any(keyword in strategy_output for keyword in trigger_keywords)


def generate_dynamic_prompt(data: Dict[str, Any]) -> str | None:
    """
    主流程：
    1. 调用情绪策略判断
    2. 判断是否需要生成新prompt
    3. 如果需要 → 生成并返回
    """

    strategist_input = f"""
Character:
{data['character_name']}
{data['character_bio']}
{data['description']}

Conversation:
{data['messages']}
"""

    # Step 1 — 情绪节奏判断
    strategist_result = call_llm_simple(
        system_prompt=EMOTIONAL_STRATEGIST_PROMPT,
        user_prompt=strategist_input,
        temperature=0.2
    )

    # Step 2 — 判断是否触发动态提示词生成
    if not should_generate_new_prompt(strategist_result):
        return None

    # Step 3 — 生成新的动态提示词
    prompt_engineer_input = PROMPT_ENGINEER_TEMPLATE.format(
        character_data=f"""
Name: {data['character_name']}
Bio: {data['character_bio']}
Description: {data['description']}
""",
        chat_logs=data['messages']
    )

    new_prompt = call_llm_simple(
        system_prompt="You are a professional AI prompt engineer.",
        user_prompt=prompt_engineer_input,
        temperature=0.4
    )

    return new_prompt