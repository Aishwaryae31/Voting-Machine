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

Website link:https://aishwaryamarsehttiwar.pythonanywhere.com/
<img width="1901" height="873" alt="{65FCD4ED-3BE4-4B14-9BDD-E4B7579C6A9B}" src="https://github.com/user-attachments/assets/19d82686-0372-44f2-a814-65e055c2ab24" />
<img width="1902" height="874" alt="{2984920B-5C08-4E3C-8E6C-A110C5F9839F}" src="https://github.com/user-attachments/assets/3defa4f4-033e-4f84-9e6e-4c7e9d3ef0ca" />
<img width="1902" height="887" alt="{E3496F9E-1B06-447E-8AB7-8227634C379E}" src="https://github.com/user-attachments/assets/e66c1f15-2caf-4393-bd41-2523e51e0ecb" />
<img width="1894" height="877" alt="{E14451E3-86B4-41FE-8A43-2F80BF0600FF}" src="https://github.com/user-attachments/assets/d8e85ccf-d71d-4827-bf7b-885d2cb0ef67" />
<img width="1919" height="869" alt="{11B44B5C-9F5A-4A68-98D7-58CD40E2BD81}" src="https://github.com/user-attachments/assets/b5ddfa3f-ece0-4fc5-be27-80939fa0f4af" />
<img width="1902" height="871" alt="{4220324C-DE89-4269-A9F2-816E92EF44A5}" src="https://github.com/user-attachments/assets/c5d6ac7f-0c18-44fa-a805-6f89b7538c63" />
<img width="1904" height="873" alt="{55C39B8E-3F53-48D0-8B0D-BB0B42EF0B5C}" src="https://github.com/user-attachments/assets/30d94023-0108-4750-9dbf-a4ebf3d9069e" />
<img width="1897" height="874" alt="{E26FA315-B8EB-4E41-818C-A4EDF01F356F}" src="https://github.com/user-attachments/assets/a92e765d-32c6-4053-a317-773f912a9a3f" />
<img width="1900" height="872" alt="{61882FEA-2C9F-4789-A2A5-FAAC0E7D8167}" src="https://github.com/user-attachments/assets/80652868-13e8-4766-9ed1-b7ccc629b379" />
<img width="1897" height="880" alt="{57594425-3F54-4588-A804-C6EEA6ECEF68}" src="https://github.com/user-attachments/assets/d37d1049-7207-47a3-9aaa-4a309399321b" />
<img width="1905" height="539" alt="{9B632615-4B06-40C2-8797-E70FFACD3918}" src="https://github.com/user-attachments/assets/74b07396-edb9-49cf-b528-c36e8ef89d64" />
<img width="1898" height="881" alt="{D20E3CCF-291F-4BDE-B624-1099C9147C31}" src="https://github.com/user-attachments/assets/084a8d6e-c8f7-4892-acdf-de24cb166db6" />
<img width="1896" height="703" alt="{171BC1AC-3A6D-461A-B211-60DAC486BC74}" src="https://github.com/user-attachments/assets/36c3e123-4d66-466b-aa3a-7aa53d793b1b" />
<img width="1895" height="876" alt="{99744883-2CA0-459F-8ADF-2FC861205DC1}" src="https://github.com/user-attachments/assets/427d956a-7c65-49f4-9f05-c6ed16713985" />
