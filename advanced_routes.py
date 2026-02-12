# Advanced Routes for Flask App
# Add these to your app.py

from flask import jsonify, request, session, send_file
from tamper_demo import TamperDetectionDemo
from qr_generator import QRCodeGenerator
from translations import get_translation, get_all_translations
import io
from PIL import Image
import base64

# 1. TAMPER DETECTION DEMO ROUTES

@app.route('/api/tamper/demo', methods=['POST'])
def tamper_demo():
    """
    Demonstrate tampering attempt on blockchain
    """
    data = request.json
    block_index = data.get('block_index', 1)
    new_vote = data.get('new_vote', {'candidate': 'HACKER', 'votes': 9999})
    
    result = TamperDetectionDemo.attempt_tamper(blockchain, block_index, new_vote)
    return jsonify(result)

@app.route('/api/tamper/51attack', methods=['GET'])
def simulate_51_attack():
    """
    Simulate 51% attack
    """
    result = TamperDetectionDemo.simulate_51_attack(blockchain)
    return jsonify(result)

# 2. QR CODE ROUTES

@app.route('/api/qr/generate', methods=['POST'])
def generate_qr():
    """
    Generate QR code for voter
    """
    if 'voter_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    voter_id = session['voter_id']
    voter = next((v for v in voters if v['voter_id'] == voter_id), None)
    
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    qr_image = QRCodeGenerator.generate_voter_qr(
        voter_id,
        voter['name'],
        voter.get('registered_at', None)
    )
    
    return jsonify({
        'success': True,
        'qr_code': qr_image,
        'voter_id': voter_id,
        'name': voter['name']
    })

@app.route('/api/qr/verify', methods=['POST'])
def verify_qr():
    """
    Verify and login using QR code data
    """
    data = request.json
    qr_data = data.get('qr_data')
    
    is_valid, voter_data = QRCodeGenerator.verify_qr_data(qr_data)
    
    if not is_valid:
        return jsonify({'error': 'Invalid QR code'}), 400
    
    voter_id = voter_data.get('voter_id')
    voter = next((v for v in voters if v['voter_id'] == voter_id), None)
    
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    # Check if already voted
    if voter_id in voted_voters:
        return jsonify({'error': 'Already voted'}), 400
    
    # Login the voter
    session['voter_id'] = voter_id
    session['name'] = voter['name']
    
    return jsonify({
        'success': True,
        'message': 'QR login successful',
        'voter': {
            'voter_id': voter_id,
            'name': voter['name']
        }
    })

# 3. TRANSLATION ROUTES

@app.route('/api/translations/<language>')
def get_translations(language):
    """
    Get all translations for a language
    """
    if language not in ['en', 'hi']:
        language = 'en'
    
    return jsonify(get_all_translations(language))

@app.route('/api/translate', methods=['POST'])
def translate_key():
    """
    Translate a specific key
    """
    data = request.json
    language = data.get('language', 'en')
    key = data.get('key', '')
    
    translation = get_translation(language, key)
    return jsonify({'translation': translation})

# 4. ENHANCED RESULTS ROUTE

@app.route('/api/results/detailed')
def detailed_results():
    """
    Get detailed results with statistics
    """
    results = get_results()
    
    # Calculate statistics
    total_votes = sum(c['votes'] for c in results['candidates'])
    total_registered = len(voters)
    turnout_percentage = (total_votes / total_registered * 100) if total_registered > 0 else 0
    
    # Find winner
    winner = max(results['candidates'], key=lambda x: x['votes']) if results['candidates'] else None
    
    # Calculate vote percentages
    for candidate in results['candidates']:
        candidate['percentage'] = (candidate['votes'] / total_votes * 100) if total_votes > 0 else 0
    
    return jsonify({
        **results,
        'statistics': {
            'total_registered_voters': total_registered,
            'total_votes_cast': total_votes,
            'turnout_percentage': round(turnout_percentage, 2),
            'winner': winner,
            'blockchain_blocks': len(blockchain.chain),
            'chain_valid': blockchain.is_chain_valid()
        }
    })

# 5. BLOCKCHAIN INTEGRITY CHECK

@app.route('/api/blockchain/verify')
def verify_blockchain():
    """
    Comprehensive blockchain verification
    """
    chain_data = []
    is_valid = True
    errors = []
    
    for i, block in enumerate(blockchain.chain):
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
            prev_block = blockchain.chain[i - 1]
            if block.previous_hash != prev_block.hash:
                block_info['is_valid'] = False
                block_info['errors'].append('Previous hash mismatch')
                is_valid = False
        
        chain_data.append(block_info)
    
    return jsonify({
        'is_valid': is_valid,
        'total_blocks': len(blockchain.chain),
        'blocks': chain_data,
        'verification_time': 'instant',
        'algorithm': 'SHA-256'
    })

