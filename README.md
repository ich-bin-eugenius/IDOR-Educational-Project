# IDOR Vulnerability Simulation & Security Auditor

This project is a cybersecurity educational lab consisting of a **vulnerable web application** and a **security scanning tool**. It demonstrates the risks of **Insecure Direct Object Reference (IDOR)** and how automated tools can be used for security auditing.

## 📖 Background
I discovered a real-world IDOR vulnerability where personal data of students and teachers was exposed through unauthenticated URL parameter manipulation. To document this safely in my portfolio, I created this local laboratory environment to simulate the flaw and its detection.

## 🛠️ Project Structure

- `app.py`: A Python Flask application simulating a student portal. It contains a deliberate IDOR flaw where user profiles are accessible by changing the `person` ID in the URL without any authorization check.
- `scanner.py`: An automated security tool that performs "fuzzing" on the ID parameter. It uses `BeautifulSoup` to parse the HTML and confirm if sensitive data (like names) is actually being leaked, filtering out false positives.

## 🚀 How to Run the Lab

1. **Install dependencies:**
   ```bash
   pip install flask requests beautifulsoup4 colorama
Start the vulnerable server:

Bash
python app.py
The server will run on https://www.google.com/search?q=http://127.0.0.1:5000

Run the security scanner:

Bash
python scanner.py
🔍 Vulnerability Explained
The flaw exists in how the server handles the person parameter:
http://127.0.0.1:5000/story.php?person=7235

The application retrieves the user data directly from the ID provided by the client without verifying if the requester has the right to see that specific data.

Security Auditor Logic:
The scanner doesn't just look for a 200 OK response. It performs a content-based validation:

It targets the specific HTML tag: <span style="margin-left:2px;">

It verifies if the tag contains a non-empty string.

This distinguishes between a real data leak and a generic "Page Not Found" or "Empty Profile" template.

🛡️ Responsible Disclosure & Ethics
As a student interested in cybersecurity, I follow White Hat principles. When I found this bug in a real system:

I did not download or leak any private data.

I reported the vulnerability to the vendor immediately.

I used this local simulation to showcase the technical aspect without compromising real-world security.