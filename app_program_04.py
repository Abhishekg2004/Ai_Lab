from sentence_transformers import SentenceTransformer, util

# Predefined marketing content database
content_database = {
    "AI in Marketing": "Leverage AI to automate and personalize customer journeys.",
    "Email Personalization": "Use behavioral data to send tailored emails that convert.",
    "SEO Optimization": "Enhance your website visibility using smart keyword strategies.",
    "Social Media Insights": "Analyze user engagement trends to boost campaign effectiveness.",
    "Customer Retention": "Implement AI tools to predict churn and retain loyal users.",
    "Content Automation": "Automatically generate blog posts and social content using AI."
}

# Load BERT-based model
print("Loading BERT model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode all content entries once
corpus_sentences = list(content_database.values())
corpus_embeddings = model.encode(corpus_sentences, convert_to_tensor=True)

# Ask user for input
query = input("Enter your query: ")

# Encode the user query
query_embedding = model.encode(query, convert_to_tensor=True)

# Compute cosine similarities
cosine_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

# Get the top matching result
top_result_idx = cosine_scores.argmax()
top_title = list(content_database.keys())[top_result_idx]
top_content = corpus_sentences[top_result_idx]
top_score = float(cosine_scores[top_result_idx])

# Output
print("\n🔍 Best Match:")
print(f"Title: {top_title}")
print(f"Content: {top_content}")
print(f"Similarity Score: {top_score:.4f}")
