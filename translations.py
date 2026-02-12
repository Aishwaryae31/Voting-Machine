"""
Multi-language translations for voting system
Supports English (en) and Hindi (hi)
"""

TRANSLATIONS = {
    'en': {
        # Navigation
        'home': 'Home',
        'register': 'Register',
        'vote': 'Vote',
        'results': 'Results',
        'admin': 'Admin',
        
        # Registration
        'register_title': 'Voter Registration',
        'full_name': 'Full Name',
        'email': 'Email Address',
        'voter_id': 'Voter ID',
        'password': 'Password',
        'submit': 'Submit',
        'register_button': 'Register to Vote',
        
        # Login/Vote
        'login_title': 'Login to Vote',
        'login_button': 'Login',
        'cast_vote_title': 'Cast Your Vote',
        'select_candidate': 'Select a Candidate',
        'cast_vote_button': 'Cast Vote',
        'already_voted': 'You have already voted!',
        
        # Results
        'results_title': 'Election Results',
        'candidate_name': 'Candidate Name',
        'party': 'Party',
        'votes': 'Votes',
        'blockchain_status': 'Blockchain Status',
        'blockchain_valid': 'Valid',
        'blockchain_invalid': 'Invalid',
        
        # Messages
        'vote_success': 'Your vote has been cast successfully!',
        'vote_error': 'Error casting vote',
        'login_error': 'Invalid credentials',
        'already_registered': 'Voter ID already registered',
        
        # QR Code
        'qr_title': 'Your Voter QR Code',
        'qr_scan': 'Scan this QR code to vote quickly',
        'download_qr': 'Download QR Code',
        
        # Common
        'back': 'Back',
        'logout': 'Logout',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
    },
    
    'hi': {
        # Navigation
        'home': 'होम',
        'register': 'पंजीकरण',
        'vote': 'वोट',
        'results': 'परिणाम',
        'admin': 'प्रशासन',
        
        # Registration
        'register_title': 'मतदाता पंजीकरण',
        'full_name': 'पूरा नाम',
        'email': 'ईमेल पता',
        'voter_id': 'मतदाता आईडी',
        'password': 'पासवर्ड',
        'submit': 'जमा करें',
        'register_button': 'वोट के लिए पंजीकरण करें',
        
        # Login/Vote
        'login_title': 'वोट करने के लिए लॉगिन करें',
        'login_button': 'लॉगिन',
        'cast_vote_title': 'अपना वोट डालें',
        'select_candidate': 'एक उम्मीदवार चुनें',
        'cast_vote_button': 'वोट डालें',
        'already_voted': 'आप पहले ही वोट कर चुके हैं!',
        
        # Results
        'results_title': 'चुनाव परिणाम',
        'candidate_name': 'उम्मीदवार का नाम',
        'party': 'पार्टी',
        'votes': 'वोट',
        'blockchain_status': 'ब्लॉकचेन स्थिति',
        'blockchain_valid': 'मान्य',
        'blockchain_invalid': 'अमान्य',
        
        # Messages
        'vote_success': 'आपका वोट सफलतापूर्वक डाला गया है!',
        'vote_error': 'वोट डालने में त्रुटि',
        'login_error': 'अमान्य प्रमाण पत्र',
        'already_registered': 'मतदाता आईडी पहले से पंजीकृत है',
        
        # QR Code
        'qr_title': 'आपका मतदाता क्यूआर कोड',
        'qr_scan': 'जल्दी वोट करने के लिए इस क्यूआर कोड को स्कैन करें',
        'download_qr': 'क्यूआर कोड डाउनलोड करें',
        
        # Common
        'back': 'पीछे',
        'logout': 'लॉगआउट',
        'loading': 'लोड हो रहा है...',
        'error': 'त्रुटि',
        'success': 'सफलता',
    }
}

def get_translation(language, key):
    """
    Get translation for a specific key
    Args:
        language: 'en' or 'hi'
        key: translation key
    Returns:
        Translated string or key if not found
    """
    if language not in TRANSLATIONS:
        language = 'en'
    
    return TRANSLATIONS[language].get(key, key)

def get_all_translations(language):
    """
    Get all translations for a language
    Args:
        language: 'en' or 'hi'
    Returns:
        Dictionary of all translations
    """
    if language not in TRANSLATIONS:
        language = 'en'
    
    return TRANSLATIONS[language]