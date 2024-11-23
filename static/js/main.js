// Handle file upload
document.getElementById('uploadForm').onsubmit = async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const file = fileInput.files[0];
    
    if (!file) {
        uploadStatus.textContent = 'Please select a file first.';
        uploadStatus.style.color = '#dc3545';  // red color for error
        return;
    }

    // Show loading status
    uploadStatus.textContent = 'Uploading and processing file...';
    uploadStatus.style.color = '#007bff';  // blue color for processing

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (response.ok) {
            uploadStatus.style.color = '#28a745';  // green color for success
            uploadStatus.textContent = result.message;
            // Clear the file input for next upload
            fileInput.value = '';
        } else {
            uploadStatus.style.color = '#dc3545';  // red color for error
            uploadStatus.textContent = result.message || 'Error uploading file';
        }
    } catch (error) {
        console.error('Error:', error);
        uploadStatus.style.color = '#dc3545';  // red color for error
        uploadStatus.textContent = 'Error uploading file: Network or server error';
    }
};

// Toggle UI elements during processing
function toggleUIElements(disabled) {
    document.getElementById('userInput').disabled = disabled;
    document.getElementById('sendButton').disabled = disabled;
    document.getElementById('typingIndicator').style.display = disabled ? 'block' : 'none';
}

// Add message to chat
function addMessage(content, isUser = false) {
    const chatOutput = document.getElementById('chatOutput');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'Bot'}:</strong> ${content}`;
    chatOutput.appendChild(messageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

// Handle sending messages
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const question = userInput.value.trim();
    
    if (!question) return;

    // Add user message and clear input
    addMessage(question, true);
    userInput.value = '';

    // Disable input and show typing indicator
    toggleUIElements(true);

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({question: question})
        });
        const result = await response.json();
        
        // Hide typing indicator and add bot response
        toggleUIElements(false);
        addMessage(result.answer);
    } catch (error) {
        console.error('Error:', error);
        toggleUIElements(false);
        addMessage('Error: Failed to get response');
    }
}

// Handle Enter key in input
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey && !this.disabled) {
        e.preventDefault();
        sendMessage();
    }
});

// Show filename when file is selected
document.getElementById('fileInput').addEventListener('change', function(e) {
    const uploadStatus = document.getElementById('uploadStatus');
    if (this.files[0]) {
        uploadStatus.textContent = `Selected file: ${this.files[0].name}`;
        uploadStatus.style.color = '#000';  // Reset color to default
    } else {
        uploadStatus.textContent = '';
    }
});

// Initial setup
document.addEventListener('DOMContentLoaded', function() {
    // Enable input and button initially
    toggleUIElements(false);
    
    // Clear any existing upload status
    document.getElementById('uploadStatus').textContent = '';
});