// Global AbortController variable
let controller = null;

// Function to fetch data from a URL
async function fetchData(url) {
    try {
        // Create a new AbortController for each fetch
        controller = new AbortController();
        const signal = controller.signal;

        console.log(`Starting fetch from: ${url}`);

        // Start the fetch with the abort signal
        const response = await fetch(url, { signal });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON data
        const data = await response.json();

        // Display the data in the output div
        document.getElementById('output').textContent = 
            JSON.stringify(data, null, 2);

        console.log('Fetch successful');

    } catch (error) {
        // Handle different types of errors
        if (error.name === 'AbortError') {
            document.getElementById('output').textContent = 
                "Fetch request was canceled.";
            console.warn("Request was aborted by user");
        } else {
            document.getElementById('output').textContent = 
                `Fetch error: ${error.message}`;
            console.error("Fetch error details:", error);
        }
    }
}

// Ensure DOM is fully loaded before adding event listeners
document.addEventListener('DOMContentLoaded', () => {
    const fetchButton = document.getElementById('fetch-btn');
    const abortButton = document.getElementById('abort-btn');

    if (!fetchButton || !abortButton) {
        console.error('Fetch or Abort button not found!');
        return;
    }

    // Event listener for fetch button
    fetchButton.addEventListener('click', () => {
        // Fetch data from a sample API
        fetchData('https://jsonplaceholder.typicode.com/posts');
    });

    // Event listener for abort button
    abortButton.addEventListener('click', () => {
        // Abort the ongoing fetch if a controller exists
        if (controller) {
            controller.abort();
            console.log("Fetch aborted by user");
        }
    });

    console.log("Event listeners added successfully");

    // Debug: Log all elements to ensure they exist
    console.log('Checking DOM elements...');
    
    const chatIcon = document.getElementById('chat-icon');
    const chatbox = document.getElementById('chatbox');

    // Comprehensive element existence check
    if (!chatIcon) {
        console.error('❌ Chat icon not found! Check your HTML.');
        return;
    }

    if (!chatbox) {
        console.error('❌ Chatbox not found! Check your HTML.');
        return;
    }

    // Ensure chatbox is initially hidden
    chatbox.style.display = 'none';
    console.log('✅ Chatbox initially hidden');

    // Detailed click handler for chat icon
    chatIcon.addEventListener('click', (event) => {
        console.log('🖱️ Chat icon clicked');
        
        // Prevent event from propagating
        event.stopPropagation();
        event.preventDefault();
        
        // Toggle chatbox visibility with logging
        if (chatbox.style.display === 'none') {
            chatbox.style.display = 'flex';
            console.log('📬 Chatbox opened');
        } else {
            chatbox.style.display = 'none';
            console.log('🔒 Chatbox closed');
        }
    });

    // Global click handler with detailed logging
    document.addEventListener('click', (event) => {
        console.log('🌍 Document clicked');
        console.log('Click target:', event.target);
        console.log('Is inside chat icon:', chatIcon.contains(event.target));
        console.log('Is inside chatbox:', chatbox.contains(event.target));

        // Close chatbox when clicking outside
        if (!chatIcon.contains(event.target) && 
            !chatbox.contains(event.target)) {
            chatbox.style.display = 'none';
            console.log('🚪 Chatbox closed due to outside click');
        }
    }, true);  // Use capture phase for more reliable event handling

    // Prevent chatbox from closing when clicking inside
    chatbox.addEventListener('click', (event) => {
        console.log('💬 Inside chatbox click');
        event.stopPropagation();
    });

    // Optional: Message sending functionality
    const sendButton = chatbox.querySelector('button');
    const messageInput = chatbox.querySelector('input');
    const chatBody = chatbox.querySelector('.chat-body');

    if (sendButton && messageInput && chatBody) {
        sendButton.addEventListener('click', () => {
            const messageText = messageInput.value.trim();
            if (messageText) {
                const messageElement = document.createElement('div');
                messageElement.textContent = messageText;
                messageElement.classList.add('user-message');
                
                chatBody.appendChild(messageElement);
                messageInput.value = '';
                chatBody.scrollTop = chatBody.scrollHeight;
            }
        });

        messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendButton.click();
            }
        });
    } else {
        console.warn('⚠️ Some chat elements are missing');
    }

    console.log('✨ Chatbot initialization complete');
});

// Optional: Log when script is loaded
console.log("Fetch script loaded successfully");
