from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_feedback(question, user_answer, reference_answer, missing_concepts, score):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful senior engineer giving feedback to a junior developer preparing for a technical job interview. You speak simply and directly — like a real person, not a textbook. You never use complicated academic words when simple ones work."
            },
            {
                "role": "user",
                "content": f"""
Question: {question}
Reference Answer: {reference_answer}
User's Answer: {user_answer}
Similarity Score: {score}/100
Missing Concepts: {', '.join(missing_concepts)}

Write an improved version of the user's answer that includes the missing concepts.

RULES:
- Exactly 3 sentences
- Simple everyday words
- The way someone would actually speak in a technical interview
- Not an essay, not a textbook

Format exactly like this:
IMPROVED ANSWER:
[3 sentences]
"""
            }
        ]
    )

    result = response.choices[0].message.content
    return result
    