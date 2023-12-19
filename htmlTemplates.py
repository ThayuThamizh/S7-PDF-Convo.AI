# CSS styles
css = '''
<style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
        background-color: #f4f4f4; /* Background color for the chat container */
        border-radius: 8px;
        overflow-y: auto;
        max-height: 400px; /* Add a max-height and overflow for scrollable messages */
    }
    .chat-message-container {
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        margin-bottom: 10px; /* Add some margin between messages */
    }
    .chat-message-container.bot {
        justify-content: flex-start; /* Bot messages on the left */
    }
    .chat-message-container.user {
        justify-content: flex-end; /* User messages on the right */
    }
    .chat-message {
        display: flex;
        flex-direction: column;
        gap: 0.5rem; /* Add some gap between avatar and message */
    }
    .chat-message.user .avatar img,
    .chat-message.bot .avatar img {
        width: 40px; /* Adjust the width of the avatar */
        height: 40px; /* Adjust the height of the avatar */
        border-radius: 50%; /* Make the avatar round */
        margin-bottom: 0.5rem; /* Add some space between avatar and message bubble */
    }
    .avatar {
        display: flex;
        align-items: center; /* Center the avatar and message bubble vertically */
        overflow: hidden; /* Hide any overflowing content */
        width: 40px; /* Set the width of the avatar container */
        height: 40px; /* Set the height of the avatar container */
        border-radius: 50%; /* Make the avatar container round */
    }
    .avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .message-bubble {
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .message-bubble.user {
        background-color:   #007bff; /* User message color */
        color: #ffffff;
        align-self: flex-end;
    }
    .message-bubble.bot {
        background-color: #28a745; /* Bot message color */
        color: #ffffff;
        align-self: flex-start;
    }
</style>
'''

# HTML templates
bot_template = '''
<div class="chat-message-container bot">
    <div class="chat-message">
        <div class="avatar">
            <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" alt="Bot Avatar">
        </div>
        <div class="message-bubble bot">
            {{MSG}}
        </div>
    </div>
</div>
'''

user_template = '''
<div class="chat-message-container user">
    <div class="chat-message">
        <div class="avatar">
            <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png" alt="User Avatar">
        </div>
        <div class="message-bubble user">
            {{MSG}}
        </div>
    </div>
</div>
'''
