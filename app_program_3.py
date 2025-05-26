from flask import Flask, request, render_template_string
from transformers import pipeline
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
generator = pipeline("text-generation", model="gpt2")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="AI-powered marketing automation" />
  <title>AI Marketing Automation</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif; }
    .hero { background: #343a40; color: white; padding: 60px 20px; text-align: center; }
    .section { padding: 40px 20px; }
    .footer { background: #212529; color: #aaa; padding: 20px; text-align: center; }
  </style>
</head>
<body>
  <div class="hero">
    <h1>AI-Powered Marketing Automation</h1>
    <p>Generate SEO content & personalized emails</p>
  </div>

  <div class="container section">
    <h2>🔍 SEO Content Generator</h2>
    <form method="post" action="/generate-content">
      <div class="mb-3">
        <label for="topic" class="form-label">Business Topic</label>
        <select name="topic" class="form-select" required>
          <option value="Cloud CRM for SMEs">Cloud CRM for SMEs</option>
          <option value="E-commerce automation">E-commerce automation</option>
          <option value="Healthcare AI solutions">Healthcare AI solutions</option>
          <option value="Digital Marketing Strategies">Digital Marketing Strategies</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="keywords" class="form-label">Target Keywords</label>
        <select name="keywords" class="form-select" multiple required>
          <option value="CRM">CRM</option>
          <option value="automation">automation</option>
          <option value="cloud">cloud</option>
          <option value="AI">AI</option>
          <option value="marketing">marketing</option>
        </select>
        <small class="text-muted">Hold Ctrl (Windows) or Cmd (Mac) to select multiple keywords</small>
      </div>
      <button type="submit" class="btn btn-primary">Generate Content</button>
    </form>
    {% if content %}
      <div class="alert alert-secondary mt-3"><strong>Generated Content:</strong><br>{{ content }}</div>
    {% endif %}
  </div>

  <div class="container section">
    <h2>📬 Personalized Email Campaign</h2>
    <form method="post" action="/send-email">
      <div class="mb-3">
        <label for="name" class="form-label">Customer Name</label>
        <input type="text" name="name" class="form-control" required>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Customer Email</label>
        <input type="email" name="email" class="form-control" required>
      </div>
      <div class="mb-3">
        <label for="activity" class="form-label">Recent Activity</label>
        <select name="activity" class="form-select" required>
          <option value="Visited pricing page">Visited pricing page</option>
          <option value="Signed up for free trial">Signed up for free trial</option>
          <option value="Downloaded whitepaper">Downloaded whitepaper</option>
          <option value="Attended webinar">Attended webinar</option>
        </select>
      </div>
      <button type="submit" class="btn btn-success">Send Email</button>
    </form>
    {% if message %}
      <div class="alert alert-info mt-3">{{ message }}</div>
    {% endif %}
  </div>

  <div class="footer">
    <p>&copy; 2025 Smart Marketing AI System</p>
  </div>
</body>
</html>
"""

def generate_seo_content(topic, keywords):
    prompt = f"Write an SEO-friendly paragraph about '{topic}' using these keywords: {', '.join(keywords)}"
    result = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
    return result.strip()

def generate_email(name, activity):
    # Template-based professional email
    return f"""
Hi {name},

Thanks for {activity.lower()}! We noticed your interest and would love to help you discover how our AI-powered CRM system can streamline your business processes, improve customer engagement, and save your valuable time.

Feel free to reach out if you have any questions or would like a personalized demo.

– The Smart CRM Team
"""


def send_email(to_email, subject, body):
    from_email = "sreea8309@gmail.com"
    password = "wjwi gegh hwim cjtq"  # Use an app password, not your main password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.send_message(msg)

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/generate-content', methods=['POST'])
def generate():
    topic = request.form['topic']
    keywords = request.form.getlist('keywords')
    content = generate_seo_content(topic, keywords)
    return render_template_string(HTML, content=content)

@app.route('/send-email', methods=['POST'])
def email():
    name = request.form['name']
    email = request.form['email']
    activity = request.form['activity']
    content = generate_email(name, activity)
    send_email(email, "Thank You from Smart CRM", content)
    return render_template_string(HTML, message=f"Email sent to {name} ({email})")

if __name__ == '__main__':
    app.run(debug=True)
