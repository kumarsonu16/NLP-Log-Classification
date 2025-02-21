from dotenv import load_dotenv
from groq import Groq
import json
import re

load_dotenv()
groq = Groq()

def classify_with_llm(log_msg):
    """
    Generate a variant of the input sentence. For example,
    If input sentence is "User session timed out unexpectedly, user ID: 9250.",
    variant would be "Session timed out for user 9251"
    """
    prompt = f"""Classify the log message into one of these categories: 
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Provide only the final answer without any reasoning or <think> tags.
    Strictly return only one of these: Workflow Error, Deprecation Warning, or Unclassified.
    Do not provide any explanation, preamble, or additional text.

    Log message: {log_msg}

    Final answer:"""

    chat_completion = groq.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        # model="llama-3.3-70b-versatile",
        model="deepseek-r1-distill-llama-70b",
        temperature=0.5
    )

    content = chat_completion.choices[0].message.content
    # Post-process the output to remove <think> sections
    cleaned_output = remove_think_section(content)
    return cleaned_output

def remove_think_section(output):
    """
    Remove the <think> section from the model's output.
    """
    # Use regex to remove everything between <think> and </think>
    cleaned_output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL)
    # Strip any leading/trailing whitespace
    return cleaned_output.strip()

if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))