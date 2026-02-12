🗳️ Blockchain-Based Voting Machine

A secure and tamper-resistant digital voting system built using Flask and blockchain principles to enhance transparency, integrity, and trust in electoral processes.
This project demonstrates how decentralized record-keeping concepts can be applied to real-world governance systems.

📌 Problem Statement
Traditional digital voting systems face critical challenges:
Risk of vote tampering
Centralized control of election data
Limited transparency
Lack of public verifiability
These issues reduce trust in democratic systems.
This project addresses these challenges by implementing a blockchain-inspired voting mechanism that ensures immutability and tamper detection.

💡 Solution Overview
The system records each vote as a block containing:
Hashed voter identifier
Selected candidate
Timestamp
Previous block hash
Current block hash
Each block is cryptographically linked to the previous one, ensuring that any modification to past votes is immediately detectable.

✨ Key Features
✔ Blockchain-based vote storage
✔ Tamper detection mechanism
✔ Secure vote recording with hashing
✔ QR code generation for verification
✔ SQLite-backed persistence
✔ Modular Flask architecture
✔ Deployment-ready structure

🛠️ Tech Stack
Backend: Python, Flask
Database: SQLite
Frontend: HTML, CSS, JavaScript
Blockchain Logic: Custom Python implementation
Deployment: Gunicorn

🏗️ System Architecture
User → Flask Application → Blockchain Module → SQLite Database

User casts a vote
Vote is converted into a blockchain block
Hash is generated and linked to previous block
Block is stored in the database
Tampering attempts are detectable through hash mismatch

🔐 Security Design

Hash-based block linking
Immutable vote records
Tamper validation logic
Structured database storage
Modular routing separation

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/aishwaryae31/voting-machine.git
2. Navigate to project folder
cd voting-machine
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python app.py

🌍 Impact & Relevance
Aligned with:
United Nations Sustainable Development Goal 16
Peace, Justice & Strong Institutions
This project promotes transparency, strengthens democratic systems, and demonstrates how emerging technologies can improve public trust in governance.

🔮 Future Improvements
User authentication & role-based access
Admin dashboard for election management
Real cryptographic signatures
Integration with public blockchain networks
Scalable cloud infrastructure

