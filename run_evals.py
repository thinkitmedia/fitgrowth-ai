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

test_cases = [
    {
        "name": "CrossFit gym needs members",
        "business_type": "CrossFit Gym",
        "location": "Uptown Dallas",
        "current_members": "50",
        "monthly_budget": "$500/month",
        "problem": "Need more memberships",
        "must_include": [
            "Google Business Profile",
            "referral",
            ["Facebook", "meta"],
            "lead",
            "retention"
        ]
    },
    {
        "name": "Personal trainer needs leads",
        "business_type": "Personal Trainer",
        "location": "Dallas",
        "current_members": "10 clients",
        "monthly_budget": "$300/month",
        "problem": "Need more leads",
        "must_include": [
            "lead magnet",
            ["Facebook", "meta"],
            ["follow up", "follow-up", "nurture", "nurturing"],
            "offer",
            "local"
        ]
    },
    {
        "name": "Yoga studio needs retention",
        "business_type": "Yoga Studio",
        "location": "Plano",
        "current_members": "80",
        "monthly_budget": "$400/month",
        "problem": "Members keep canceling",
        "must_include": [
            "retention",
            "check-ins",
            "community",
            "goal",
            "referral"
        ]
    }
]


def get_fitgrowth_response(test_case):
    input_text = f"""
Use the knowledge base below when making recommendations.

KNOWLEDGE BASE:
{knowledge_text}

BUSINESS INFO:
Business Type: {test_case["business_type"]}
Location: {test_case["location"]}
Current Members: {test_case["current_members"]}
Monthly Marketing Budget: {test_case["monthly_budget"]}
Main Problem: {test_case["problem"]}
"""

    response = client.responses.create(
        model="gpt-5",
        instructions=system_prompt,
        input=input_text
    )

    return response.output_text


def score_response(answer, must_include):
    score = 0
    missing = []

    answer_lower = answer.lower()

    for item in must_include:

        if isinstance(item, list):
            found = any(term.lower() in answer_lower for term in item)
        else:
            found = item.lower() in answer_lower

        if found:
            score += 1
        else:
            missing.append(item)

    return score, missing


total_score = 0
total_possible = 0

print("\n===== FITGROWTH AI EVAL REPORT =====\n")

for test_case in test_cases:
    print(f"Running test: {test_case['name']}")

    answer = get_fitgrowth_response(test_case)

    score, missing = score_response(answer, test_case["must_include"])

    possible = len(test_case["must_include"])
    total_score += score
    total_possible += possible

    print(f"Score: {score}/{possible}")

    if missing:
        print("Missing:")
        for item in missing:
            print(f"- {item}")
    else:
        print("All required items included.")

    print("-" * 40)

overall_percentage = round((total_score / total_possible) * 100, 2)

print("\n===== FINAL SCORE =====")
print(f"Overall Score: {total_score}/{total_possible}")
print(f"Percentage: {overall_percentage}%")