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
                "content": "You are an expert technical interviewer and educator. You are speaking directly to the candidate who just answered the question. Address them directly using 'you' and 'your'. Never refer to them as 'the user' or 'the candidate'."
            },
            {
                "role": "user",
                "content": f"""
Question: {question}
Reference Answer: {reference_answer}
User's Answer: {user_answer}
Similarity Score: {score}/100
Missing Concepts: {', '.join(missing_concepts)}

"Please provide:
1. SUGGESTIONS: 2-3 specific, constructive suggestions directly addressing the candidate using 'you' and 'your'
2. IMPROVED ANSWER: A professional, complete version of the answer"

Format your response exactly like this:
SUGGESTIONS:
[your suggestions here]

IMPROVED ANSWER:
[improved answer here]
"""
            }
        ]
    )

    result = response.choices[0].message.content
    return result
    