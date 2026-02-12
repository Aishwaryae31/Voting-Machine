from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import sqlite3
import hashlib
from blockchain import Blockchain
from tamper_demo import TamperDetectionDemo
from qr_generator import QRCodeGenerator
from translations import get_translation, get_all_translations
import base64
import json
import os
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this'

# Blockchain persistence file
BLOCKCHAIN_FILE = 'blockchain_data.json'

def save_blockchain():
    """Save blockchain to file"""
    try:
        chain_data = voting_blockchain.get_chain_data()
        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump(chain_data, f, indent=2)
        print(f"✅ Blockchain saved: {len(chain_data)} blocks")
    except Exception as e:
        print(f"❌ Error saving blockchain: {e}")

def load_blockchain():
    """Load blockchain from file"""
    global voting_blockchain
    
    if os.path.exists(BLOCKCHAIN_FILE):
        try:
            with open(BLOCKCHAIN_FILE, 'r') as f:
                chain_data = json.load(f)
            
            # Create new blockchain
            voting_blockchain = Blockchain()
            
            # Add blocks from saved data (skip genesis block at index 0)
            for block_data in chain_data[1:]:
                voting_blockchain.add_block(block_data['data'])
            
            print(f"✅ Loaded blockchain: {len(voting_blockchain.chain)} blocks")
            return
        except Exception as e:
            print(f"❌ Error loading blockchain: {e}")
    
    # If no saved blockchain or error, create fresh blockchain with test data
    print("📝 Creating new blockchain with test data...")
    voting_blockchain = Blockchain()
    
    # Add test votes for demo purposes
    test_votes = [
        {"voter_id": "test001", "candidate": "Candidate A", "type": "vote"},
        {"voter_id": "test002", "candidate": "Candidate B", "type": "vote"},
        {"voter_id": "test003", "candidate": "Candidate C", "type": "vote"},
        {"voter_id": "test004", "candidate": "Candidate A", "type": "vote"},
        {"voter_id": "test005", "candidate": "Candidate B", "type": "vote"},
    ]
    
    for vote in test_votes:
        voting_blockchain.add_block(vote)
    
    # Save the test blockchain
    save_blockchain()
    
    print(f"✅ Test blockchain created: {len(voting_blockchain.chain)} blocks")

# Initialize blockchain by loading from file
load_blockchain()

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Voters table
    c.execute('''CREATE TABLE IF NOT EXISTS voters
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  voter_id TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  has_voted INTEGER DEFAULT 0)''')
    
    # Candidates table
    c.execute('''CREATE TABLE IF NOT EXISTS candidates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  party TEXT NOT NULL,
                  votes INTEGER DEFAULT 0)''')
    
    # Add default candidates if none exist
    c.execute("SELECT COUNT(*) FROM candidates")
    if c.fetchone()[0] == 0:
        candidates = [
            ('Candidate A', 'Party 1'),
            ('Candidate B', 'Party 2'),
            ('Candidate C', 'Party 3')
        ]
        c.executemany("INSERT INTO candidates (name, party) VALUES (?, ?)", candidates)
    
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        voter_id = request.form['voter_id']
        password = request.form['password']
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO voters (name, email, voter_id, password) VALUES (?, ?, ?, ?)",
                     (name, email, voter_id, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('vote'))
        except sqlite3.IntegrityError:
            return "Voter ID or Email already exists!"
    
    return render_template('register.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        voter_id = request.form['voter_id'].strip()
        password = request.form['password']
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # First, check what's in the database for this voter
        c.execute("SELECT voter_id, password, has_voted FROM voters WHERE voter_id=?", (voter_id,))
        db_voter = c.fetchone()
        
        print("="*50)
        print(f"LOGIN ATTEMPT:")
        print(f"Voter ID entered: '{voter_id}'")
        print(f"Password entered: '{password}'")
        print(f"Hashed password: {hashed_password}")
        print(f"Database result: {db_voter}")
        if db_voter:
            print(f"DB Voter ID: '{db_voter[0]}'")
            print(f"DB Password Hash: {db_voter[1]}")
            print(f"Hashes match: {hashed_password == db_voter[1]}")
        print("="*50)
        
        if not db_voter:
            conn.close()
            return f"❌ Voter ID '{voter_id}' not found! Please register first."
        
        if hashed_password != db_voter[1]:
            conn.close()
            return f"❌ Wrong password for Voter ID '{voter_id}'!"
        
        if db_voter[2] == 1:
            conn.close()
            return "⚠️ You have already voted!"
        
        # Login successful
        session['voter_id'] = voter_id
        
        # Get candidates
        c.execute("SELECT * FROM candidates")
        candidates = c.fetchall()
        conn.close()
        
        return render_template('vote.html', candidates=candidates, logged_in=True)
    
    return render_template('vote.html', logged_in=False)

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    if 'voter_id' not in session:
        return redirect(url_for('vote'))
    
    candidate_id = request.form['candidate_id']
    voter_id = session['voter_id']
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Update candidate votes
    c.execute("UPDATE candidates SET votes = votes + 1 WHERE id=?", (candidate_id,))
    
    # Mark voter as voted
    c.execute("UPDATE voters SET has_voted = 1 WHERE voter_id=?", (voter_id,))
    
    # Get candidate name
    c.execute("SELECT name FROM candidates WHERE id=?", (candidate_id,))
    candidate_name = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    # Add to blockchain
    vote_data = {
        "voter_id": hashlib.sha256(voter_id.encode()).hexdigest()[:10],  # Anonymized
        "candidate": candidate_name,
        "type": "vote"
    }
    voting_blockchain.add_block(vote_data)
    
    # Save blockchain after each vote
    save_blockchain()
    
    session.pop('voter_id', None)
    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name, party, votes FROM candidates ORDER BY votes DESC")
    candidates = c.fetchall()
    conn.close()
    
    # Get blockchain data
    chain_data = voting_blockchain.get_chain_data()
    is_valid = voting_blockchain.is_chain_valid()
    
    return render_template('results.html', 
                         candidates=candidates, 
                         chain=chain_data, 
                         is_valid=is_valid)

@app.route('/api/blockchain')
def api_blockchain():
    return jsonify({
        'chain': voting_blockchain.get_chain_data(),
        'valid': voting_blockchain.is_chain_valid()
    })

@app.route('/api/results')
def api_results():
    """API endpoint for getting results and blockchain data"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name, party, votes FROM candidates ORDER BY votes DESC")
    candidates = c.fetchall()
    conn.close()
    
    candidates_list = [
        {'name': c[0], 'party': c[1], 'votes': c[2]}
        for c in candidates
    ]
    
    chain_data = voting_blockchain.get_chain_data()
    
    return jsonify({
        'candidates': candidates_list,
        'blockchain': chain_data,
        'is_valid': voting_blockchain.is_chain_valid()
    })

# ==================== ADMIN ROUTES ====================
ADMIN_PASSWORD = "admin123"

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid admin password!"
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get statistics
    c.execute("SELECT COUNT(*) FROM voters")
    total_voters = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM voters WHERE has_voted=1")
    voted_count = c.fetchone()[0]
    
    c.execute("SELECT * FROM candidates ORDER BY votes DESC")
    candidates = c.fetchall()
    
    c.execute("SELECT * FROM voters")
    voters = c.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_voters=total_voters,
                         voted_count=voted_count,
                         candidates=candidates,
                         voters=voters,
                         chain_length=len(voting_blockchain.chain))

@app.route('/admin/add_candidate', methods=['POST'])
def add_candidate():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    name = request.form['name']
    party = request.form['party']
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO candidates (name, party) VALUES (?, ?)", (name, party))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_candidate/<int:candidate_id>')
def delete_candidate(candidate_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM candidates WHERE id=?", (candidate_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reset_election')
def reset_election():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE voters SET has_voted=0")
    c.execute("UPDATE candidates SET votes=0")
    conn.commit()
    conn.close()
    
    # Reset blockchain
    global voting_blockchain
    voting_blockchain = Blockchain()
    
    # Delete saved blockchain file
    if os.path.exists(BLOCKCHAIN_FILE):
        os.remove(BLOCKCHAIN_FILE)
        print("🗑️ Blockchain file deleted")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/export_results')
def export_results():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name, party, votes FROM candidates ORDER BY votes DESC")
    candidates = c.fetchall()
    conn.close()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Candidate Name', 'Party', 'Votes'])
    for candidate in candidates:
        writer.writerow(candidate)
    
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=election_results.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# ==================== QR CODE ROUTES ====================

@app.route('/qr-code')
def qr_code_page():
    """QR Code generation page"""
    return render_template('qr_code.html')

@app.route('/api/qr/generate', methods=['POST'])
def generate_qr():
    """Generate QR code for voter"""
    if 'voter_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    voter_id = session['voter_id']
    
    # Get voter from database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM voters WHERE voter_id=?", (voter_id,))
    voter = c.fetchone()
    conn.close()
    
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    qr_image = QRCodeGenerator.generate_voter_qr(
        voter_id,
        voter[0],  # name
        None
    )
    
    return jsonify({
        'success': True,
        'qr_code': qr_image,
        'voter_id': voter_id,
        'name': voter[0]
    })

@app.route('/api/qr/verify', methods=['POST'])
def verify_qr():
    """Verify and login using QR code data"""
    data = request.json
    qr_data = data.get('qr_data')
    
    is_valid, voter_data = QRCodeGenerator.verify_qr_data(qr_data)
    
    if not is_valid:
        return jsonify({'error': 'Invalid QR code'}), 400
    
    voter_id = voter_data.get('voter_id')
    
    # Check voter in database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name, has_voted FROM voters WHERE voter_id=?", (voter_id,))
    voter = c.fetchone()
    conn.close()
    
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    # Check if already voted
    if voter[1] == 1:  # has_voted
        return jsonify({'error': 'Already voted'}), 400
    
    # Login the voter
    session['voter_id'] = voter_id
    session['name'] = voter[0]
    
    return jsonify({
        'success': True,
        'message': 'QR login successful',
        'voter': {
            'voter_id': voter_id,
            'name': voter[0]
        }
    })

# ==================== TRANSLATION ROUTES ====================

@app.route('/api/translations/<language>')
def get_translations_api(language):
    """Get all translations for a language"""
    if language not in ['en', 'hi']:
        language = 'en'
    
    return jsonify(get_all_translations(language))

@app.route('/api/translate', methods=['POST'])
def translate_key():
    """Translate a specific key"""
    data = request.json
    language = data.get('language', 'en')
    key = data.get('key', '')
    
    translation = get_translation(language, key)
    return jsonify({'translation': translation})

# ==================== TAMPER DETECTION ROUTES ====================

@app.route('/tamper-demo')
def tamper_demo_page():
    return render_template('tamper_demo.html')

@app.route('/api/tamper/demo', methods=['POST'])
def tamper_demo():
    """Demonstrate tampering attempt on blockchain"""
    data = request.json
    block_index = data.get('block_index', 1)
    new_vote = data.get('new_vote', {'candidate': 'HACKER', 'votes': 9999})
    
    result = TamperDetectionDemo.attempt_tamper(voting_blockchain, block_index, new_vote)
    return jsonify(result)

@app.route('/api/tamper/51attack', methods=['GET'])
def simulate_51_attack():
    """Simulate 51% attack"""
    result = TamperDetectionDemo.simulate_51_attack(voting_blockchain)
    return jsonify(result)

# ==================== ENHANCED API ROUTES ====================

@app.route('/api/results/detailed')
def detailed_results():
    """Get detailed results with statistics"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get candidates
    c.execute("SELECT name, party, votes FROM candidates")
    candidates_data = c.fetchall()
    
    # Get voter counts
    c.execute("SELECT COUNT(*) FROM voters")
    total_registered = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM voters WHERE has_voted=1")
    total_votes = c.fetchone()[0]
    
    conn.close()
    
    # Format candidates
    candidates = [
        {
            'name': c[0],
            'party': c[1],
            'votes': c[2],
            'percentage': (c[2] / total_votes * 100) if total_votes > 0 else 0
        }
        for c in candidates_data
    ]
    
    # Find winner
    winner = max(candidates, key=lambda x: x['votes']) if candidates else None
    
    turnout_percentage = (total_votes / total_registered * 100) if total_registered > 0 else 0
    
    return jsonify({
        'candidates': candidates,
        'statistics': {
            'total_registered_voters': total_registered,
            'total_votes_cast': total_votes,
            'turnout_percentage': round(turnout_percentage, 2),
            'winner': winner,
            'blockchain_blocks': len(voting_blockchain.chain),
            'chain_valid': voting_blockchain.is_chain_valid()
        }
    })

@app.route('/api/blockchain/verify')
def verify_blockchain_integrity():
    """Comprehensive blockchain verification"""
    chain_data = []
    is_valid = True
    
    for i, block in enumerate(voting_blockchain.chain):
        block_info = {
            'index': block.index,
            'timestamp': block.timestamp,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'is_valid': True,
            'errors': []
        }
        
        # Verify hash
        calculated_hash = block.calculate_hash()
        if calculated_hash != block.hash:
            block_info['is_valid'] = False
            block_info['errors'].append('Hash mismatch')
            is_valid = False
        
        # Verify previous hash linkage
        if i > 0:
            prev_block = voting_blockchain.chain[i - 1]
            if block.previous_hash != prev_block.hash:
                block_info['is_valid'] = False
                block_info['errors'].append('Previous hash mismatch')
                is_valid = False
        
        chain_data.append(block_info)
    
    return jsonify({
        'is_valid': is_valid,
        'total_blocks': len(voting_blockchain.chain),
        'blocks': chain_data,
        'verification_time': 'instant',
        'algorithm': 'SHA-256'
    })

# ==================== DEBUG ROUTE ====================

@app.route('/debug/blockchain')
def debug_blockchain():
    """Debug route to see blockchain state"""
    chain_info = []
    for i, block in enumerate(voting_blockchain.chain):
        chain_info.append({
            'index': i,
            'block_index': block.index,
            'data': block.data,
            'hash': block.hash[:16] + '...',
            'timestamp': block.timestamp
        })
    
    return jsonify({
        'total_blocks': len(voting_blockchain.chain),
        'blocks': chain_info,
        'file_exists': os.path.exists(BLOCKCHAIN_FILE)
    })

if __name__ == '__main__':
    app.run(debug=True)