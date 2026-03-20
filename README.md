# IDOR Auditor v3.1 (Improved interface for user)
## Preview

### 1. Tool Banner & Interface
![Banner](static/preview.png)

### 2. High-Speed Asynchronous Scanning
![Scan](static/in_work.png)

### 3. Settings
![Settings](static/changing_values.png)

### 4. Saving as .txt
![Report](static/saving-txt.png)

### 5. Generated Report (TXT Output)
![Report](static/output.png)


1. Interactive Dashboard (CLI)
The new centralized control panel for real-time configuration and audit management.

2. Smart Scraping & Async Engine
Asynchronous execution with semaphore-based rate limiting and CSS selector-based data extraction.

Project Overview
IDOR Auditor v3.1 is a high-performance security auditing tool designed to identify Insecure Direct Object Reference (IDOR) vulnerabilities. Unlike basic scripts, v3.1 is built on a Modular Architecture, separating the User Interface, the Scanning Engine, and Utility functions.

This version introduces Smart Scraping, allowing researchers to target specific data points using CSS selectors, making it adaptable to any web environment.

Key Features (v3.1)
Modular Architecture: Clean separation of concerns (main.py, new_scanner.py, utils.py).

Interactive Dashboard: Configure targets, ranges, and performance settings without touching the code.

Smart Scraping (CSS Selectors): Target specific HTML elements (e.g., span.user-name or div#profile).

Asynchronous Core: Powered by asyncio and aiohttp for maximum efficiency.

Traffic Shaping: Integrated Semaphore to prevent server-side Rate Limiting or DoS conditions.

Robust Reporting: Automated report generation with URL-sanitized filenames.

Technical Stack
Python 3.10+

Aiohttp & Asyncio: High-speed concurrent networking.

BeautifulSoup4: Advanced DOM parsing and data extraction.

Colorama: Professional terminal styling and feedback.

Regex (re): Intelligent filename sanitization and URL processing.

Project Structure
.
├── app.py           # Vulnerable Flask Lab
├── main.py          # Dashboard & CLI logic
├── scanner.py       # Async Engine
├── utils.py         # Helper functions
├── requirements.txt # Dependencies
└── README.md        # Documentation

## 🔍 How to Run the Lab

1. **Cloning git:**
   ```bash
   git clone https://github.com/ich-bin-eugenius/IDOR-Educational-Project

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt


3. **Start the vulnerable server:**
   ```bash
   python app.py

4. **Run the security scanner:**
   ```bash
   python main.py


⚖️ Legal & Ethical Notice
FOR EDUCATIONAL PURPOSES ONLY. This tool is intended for security researchers and developers to test their own systems. Unauthorized testing of third-party websites is illegal. The author is a 14-year-old student practicing ethical hacking and responsible disclosure.

Author
Eugene Zavirukha

Date: 20.03.2026

Focus: Web Security, Asynchronous Python Automation, and Security Auditing