document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const submitButton = document.getElementById('submit-button');
    const notification = document.getElementById('notification');
    const progressBar = document.getElementById('form-progress');
    const completionPercentage = document.getElementById('completion-percentage');

    // Add smooth transition for notification
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                transform: translateY(150%);
                transition: transform 0.3s ease, opacity 0.3s ease;
                opacity: 0;
                z-index: 1000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                max-width: 400px;
            }
            .notification.success {
                background-color: #28a745;
            }
            .notification.error {
                background-color: #dc3545;
            }
            .notification.info {
                background-color: #17a2b8;
            }
            .notification.show {
                transform: translateY(0);
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
    }

    // Form validation and progress tracking
    function updateFormProgress() {
        const requiredFields = form.querySelectorAll('[required]');
        const totalFields = requiredFields.length;
        let filledFields = 0;
        
        requiredFields.forEach(field => {
            if (field.type === 'checkbox' || field.type === 'radio') {
                if (field.checked) filledFields++;
            } else if (field.value.trim() !== '') {
                filledFields++;
            }
        });
        
        const percent = Math.round((filledFields / totalFields) * 100);
        progressBar.style.width = `${percent}%`;
        completionPercentage.textContent = `${percent}%`;
    }

    form.addEventListener('input', updateFormProgress);
    updateFormProgress();

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                form.reset();
            } else {
                showNotification(data.message, 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Export to JSON
    document.getElementById('export-json').addEventListener('click', () => {
        fetch('/export-json')
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'students.json';
                a.click();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Export to Excel
    document.getElementById('export-excel').addEventListener('click', () => {
        fetch('/export-excel')
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'students.xlsx';
                a.click();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Export to PDF
    document.getElementById('export-pdf').addEventListener('click', () => {
        fetch('/export-pdf')
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'students.pdf';
                a.click();
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Helper functions
    function showNotification(message, type = 'info') {
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }
});

// Check registration
function checkRegistration() {
    const idNumber = document.getElementById('id_number').value;
    const email = document.getElementById('email').value;
    const mobile = document.getElementById('mobile').value;

    fetch('/check-registration', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idNumber, email, mobile }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}