document.addEventListener("DOMContentLoaded", function() {
    console.log("Industrial Knowledge Mapping System Loaded Successfully");

    // Floating Chatbot Logic
    const launcher = document.getElementById('chatbot-launcher');
    const popup = document.getElementById('chatbot-popup');
    const closeBtn = document.getElementById('chatbot-close');
    
    if (launcher && popup && closeBtn) {
        launcher.addEventListener('click', () => {
            popup.style.display = 'flex';
            launcher.style.display = 'none';
        });

        closeBtn.addEventListener('click', () => {
            popup.style.display = 'none';
            launcher.style.display = 'flex';
        });

        // Chat Form Logic
        const chatForm = document.getElementById('chatbot-form');
        const userInput = document.getElementById('chatbot-input');
        const chatContainer = document.getElementById('chatbot-messages');
        const typingIndicator = document.getElementById('chatbot-typing');

        function scrollToBottom() {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function appendMessage(sender, htmlContent) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message-bubble ${sender === 'user' ? 'user-message' : 'bot-message shadow-sm'}`;
            messageDiv.innerHTML = htmlContent;
            chatContainer.appendChild(messageDiv);
            scrollToBottom();
        }

        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const message = userInput.value.trim();
            if (!message) return;

            // Append user message
            appendMessage('user', message);
            userInput.value = '';
            
            // Show typing indicator
            typingIndicator.style.display = 'block';
            scrollToBottom();

            // Send to backend
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                typingIndicator.style.display = 'none';
                appendMessage('bot', data.response);
            })
            .catch(error => {
                typingIndicator.style.display = 'none';
                appendMessage('bot', '<span class="text-danger"><i class="fa-solid fa-triangle-exclamation"></i> Error connecting to the database.</span>');
                console.error('Error:', error);
            });
        });
    }
});
