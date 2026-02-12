import qrcode
import io
import base64
import json
import hashlib

class QRCodeGenerator:
    """Generate and verify QR codes for voter authentication"""
    
    @staticmethod
    def generate_voter_qr(voter_id, name, email):
        """
        Generate QR code for voter
        Returns: base64 encoded image string
        """
        # Create voter data
        voter_data = {
            'voter_id': voter_id,
            'name': name,
            'type': 'voter_auth',
            'hash': hashlib.sha256(f"{voter_id}{name}".encode()).hexdigest()[:16]
        }
        
        # Convert to JSON
        qr_data = json.dumps(voter_data)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def verify_qr_data(qr_data_string):
        """
        Verify QR code data
        Returns: (is_valid, voter_data)
        """
        try:
            voter_data = json.loads(qr_data_string)
            
            # Verify structure
            if 'voter_id' not in voter_data or 'type' not in voter_data:
                return False, None
            
            if voter_data['type'] != 'voter_auth':
                return False, None
            
            # Verify hash
            expected_hash = hashlib.sha256(
                f"{voter_data['voter_id']}{voter_data['name']}".encode()
            ).hexdigest()[:16]
            
            if voter_data.get('hash') != expected_hash:
                return False, None
            
            return True, voter_data
            
        except Exception as e:
            print(f"QR verification error: {e}")
            return False, None