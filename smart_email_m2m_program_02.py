import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json

# ----------------------------------
# 1. Define User Profile & Intent
# ----------------------------------
user_profile = {
    "name": "John Smith",
    "company": "TechNova Inc.",
    "interests": ["AI", "enterprise software", "cloud computing"],
    "email_tone": "formal"
}

# ----------------------------------
# 2. Intent Selection Menu
# ----------------------------------
def choose_intent():
    intents = {
        "1": "Cold outreach",
        "2": "Follow-up after meeting",
        "3": "Schedule a product demo",
        "4": "Thank you email",
        "5": "Partnership proposal"
    }

    print("Select Email Intent:")
    for k, v in intents.items():
        print(f"{k}. {v}")
    
    choice = input("Enter choice number: ").strip()
    return intents.get(choice, "Cold outreach")

# ----------------------------------
# 3. Email Prompt Builder
# ----------------------------------
def build_prompt(profile, intent):
    prompt = f"""Write a {profile['email_tone']} business email.
Sender: {profile['name']} from {profile['company']}.
Recipient is interested in: {', '.join(profile['interests'])}.
Goal: {intent}.

Email:
"""
    return prompt

# ----------------------------------
# 4. Load GPT-2 Medium
# ----------------------------------
def load_model():
    print("Loading GPT-2 Medium model (1st time may take a minute)...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
    model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
    return model, tokenizer

# ----------------------------------
# 5. Email Generator
# ----------------------------------
def generate_email(prompt, model, tokenizer, max_length=300):
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_length=max_length,
        do_sample=True,
        top_k=40,
        top_p=0.92,
        temperature=0.7,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated = result[len(prompt):].strip()
    return generated

# ----------------------------------
# 6. Main CLI
# ----------------------------------
def main():
    intent = choose_intent()
    prompt = build_prompt(user_profile, intent)
    model, tokenizer = load_model()
    email = generate_email(prompt, model, tokenizer)

    print("\n" + "-"*50)
    print(f"📝 Personalized Email ({intent})\n")
    print(email)
    print("-"*50)

if __name__ == "__main__":
    main()
