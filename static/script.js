async function sendMessage(){

    const message =
    document.getElementById("message").value;

    const chatBox =
    document.getElementById("chat-box");

    // STOP EMPTY MESSAGE

    if(message.trim() === ""){

        return;
    }

    // USER MESSAGE

    chatBox.innerHTML += `

    <div class="user-message">
        ${message}
    </div>

    `;

    // SEND TO FLASK

    const response = await fetch('/chat', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    // BOT MESSAGE

    let botHTML = `

    <div class="bot-message">

    `;

    // PRODUCT IMAGE

    if(data.image){

        botHTML += `

        <img src="${data.image}" class="small-image">

        `;
    }

    // BOT REPLY

    botHTML += `

        <p>${data.reply}</p>

    </div>

    `;

    chatBox.innerHTML += botHTML;

    // CLEAR INPUT

    document.getElementById("message").value = "";

    // AUTO SCROLL

    chatBox.scrollTop = chatBox.scrollHeight;
}

/* ENTER BUTTON SEND MESSAGE */

document
.getElementById("message")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        sendMessage();
    }
});