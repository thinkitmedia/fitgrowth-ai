from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load system prompt
with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# Load knowledge base
knowledge_text = ""

for filename in os.listdir("knowledge"):
    if filename.endswith(".txt"):
        file_path = os.path.join("knowledge", filename)
        with open(file_path, "r", encoding="utf-8") as f:
            knowledge_text += f"\n\nSOURCE: {filename}\n"
            knowledge_text += f.read()

business_type = input("Business Type: ")
location = input("Location (optional): ")
current_members = input("Current Members (optional): ")
monthly_budget = input("Marketing Budget (optional): ")
problem = input("Main Problem: ")

input_text = f"""
Use the knowledge base below when making recommendations.

KNOWLEDGE BASE:
{knowledge_text}

BUSINESS INFO:
Business Type: {business_type}
Location: {location}
Current Members: {current_members}
Monthly Marketing Budget: {monthly_budget}
Main Problem: {problem}
"""

response = client.responses.create(
    model="gpt-5",
    instructions=system_prompt,
    input=input_text
)

print("\n===== FITGROWTH AI =====\n")
print(response.output_text)