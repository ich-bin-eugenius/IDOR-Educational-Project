# IDOR Security Auditor (v1.2)

## 🖼️ Preview

### 1. Tool Banner & Interface
![Banner](static/img1.png)
*Professional ASCII interface and environment selection.*

### 2. Scanning in Action
![Scan](static/img2.png)
*Real-time vulnerability detection and data extraction with custom range selection.*

### 3. Generated Report (TXT Output)
![Report](static/img3.png)
*Automatically generated report showing ID and username correlation.*

---

## 📖 Project Overview
This project is a cybersecurity educational lab consisting of a **vulnerable web application** and a **security auditing tool**. It demonstrates the risks of **Insecure Direct Object Reference (IDOR)**—a flaw where an application provides direct access to objects based on user-supplied input.

I developed this tool after discovering a real-world vulnerability in a local system. To document the finding safely, I created this simulation to show how automated auditing can identify and log sensitive data leaks.

## 🚀 Key Features

- **Professional CLI:** Featuring an ASCII banner and color-coded feedback for better user experience.
- **Dynamic Scoping:** Users can define a specific `Start ID` and `End ID` at runtime.
- **Environment Selection:** Support for both a local Flask testbed and custom online targets.
- **Heuristic Parsing:** Uses `BeautifulSoup4` to analyze the DOM and verify if personal data is actually present, filtering out false positives.
- **Automated Reporting:** Generates a sanitized `.txt` file containing all confirmed vulnerabilities.

## 🛠️ Technical Stack
- **Python 3**
- **Requests:** For handling HTTP communication.
- **BeautifulSoup4:** For parsing and analyzing HTML structure.
- **Colorama:** For terminal styling.
- **Flask:** For the vulnerable web application simulation.

## 📁 Project Structure
- `app.py`: The vulnerable portal simulation (Flask).
- `scanner.py`: The main auditing engine.
- `requirements.txt`: List of necessary Python libraries.

## 🔍 How to Run the Lab

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
Start the vulnerable server:

Bash
python app.py
Run the security scanner:

Bash
python scanner.py
Follow the on-screen instructions to select the target and set the ID range.

⚖️ Legal & Ethical Notice
FOR EDUCATIONAL PURPOSES ONLY. This tool is intended for security researchers and developers to test their own systems. Unauthorized testing of third-party websites is illegal. The author is a 14-year-old student practicing ethical hacking and responsible disclosure.

👤 Author
Eugene Zavirukha

Date: 16.03.2026

Focus: Web Security, Python Automation, and Security Auditing