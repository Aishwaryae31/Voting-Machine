// Vote Confirmation Modal
function confirmVote(candidateId, candidateName) {
    document.getElementById('candidateId').value = candidateId;
    document.getElementById('candidateName').textContent = candidateName;
    document.getElementById('voteModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('voteModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('voteModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Toggle blockchain block details
function toggleBlock(index) {
    const details = document.getElementById('block-' + index);
    const icon = document.getElementById('icon-' + index);
    
    if (details.style.display === 'block') {
        details.style.display = 'none';
        icon.textContent = '▼';
    } else {
        details.style.display = 'block';
        icon.textContent = '▲';
    }
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.style.borderColor = '#ef4444';
                } else {
                    input.style.borderColor = '#e5e7eb';
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
});

// Auto-hide alerts
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.display = 'none';
    });
}, 5000);