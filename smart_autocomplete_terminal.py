from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load upgraded model and tokenizer
print("Loading GPT-2 Medium model... (first time only)")
model_name = "gpt2-medium"  # More accurate than gpt2
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_suggestions(prompt, max_new_tokens=15, num_suggestions=5):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    outputs = model.generate(
        input_ids,
        max_length=input_ids.shape[1] + max_new_tokens,
        num_return_sequences=num_suggestions,
        do_sample=True,
        top_k=40,               # Sample from top 40 words
        top_p=0.92,             # Nucleus sampling
        temperature=0.7,        # Lower temp for focused output
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id,
    )

    suggestions = set()
    for output in outputs:
        full_text = tokenizer.decode(output, skip_special_tokens=True)
        if prompt in full_text:
            suggestion = full_text[len(prompt):].strip()
            suggestion = suggestion.split('.')[0].strip()  # get first clause
            if suggestion and len(suggestion.split()) > 1:
                suggestions.add(suggestion)

    return list(suggestions)[:num_suggestions]

def main():
    user_input = input("Start typing your email: ").strip()

    while True:
        suggestions = generate_suggestions(user_input)

        if not suggestions:
            print("No suggestions found. Try again.")
            break

        print("\nSuggestions:")
        for idx, suggestion in enumerate(suggestions, 1):
            print(f"{idx}. {suggestion}")

        choice = input("\nChoose a suggestion number to append (or press Enter to exit): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
            selected = suggestions[int(choice) - 1]
            user_input += " " + selected
            print(f"\nUpdated text: {user_input}")
        else:
            break

        print("\n----------------------------")

    print(f"\nFinal composed text:\n{user_input}")

if __name__ == "__main__":
    main()
