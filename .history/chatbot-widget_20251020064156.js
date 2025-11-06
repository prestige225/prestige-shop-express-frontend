// ======================================
// CHATBOT WIDGET POUR PRESTIGE SHOP EXPRESS
// ======================================

// Injecter le CSS du chatbot
const chatbotStyles = `
<style id="chatbot-styles">
    /* Animation du chatbot */
    @keyframes chatbot-slideUp {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes chatbot-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .chatbot-container {
        animation: chatbot-slideUp 0.3s ease-out;
    }
    
    .chatbot-button-float {
        animation: chatbot-bounce 2s infinite;
    }
    
    .chatbot-button-float:hover {
        animation: none;
    }
    
    /* Animation des messages */
    @keyframes chatbot-fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chatbot-message {
        animation: chatbot-fadeIn 0.3s ease-out;
    }
    
    /* Animation de typing */
    .chatbot-typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    
    .chatbot-typing-dot {
        width: 8px;
        height: 8px;
        background: #9333ea;
        border-radius: 50%;
        animation: chatbot-typingDot 1.4s infinite;
    }
    
    .chatbot-typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .chatbot-typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes chatbot-typingDot {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    /* Scrollbar personnalisée */
    .chatbot-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chatbot-messages::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chatbot-messages::-webkit-scrollbar-thumb {
        background: #9333ea;
        border-radius: 10px;
    }
    
    .chatbot-messages::-webkit-scrollbar-thumb:hover {
        background: #7c3aed;
    }
</style>
`;

// Injecter le HTML du chatbot
const chatbotHTML = `
<!-- Bouton du chatbot flottant -->
<div id="chatbot-button" class="chatbot-button-float fixed bottom-6 right-6 z-[9999]" style="z-index: 9999;">
    <button onclick="toggleChatbot()" class="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white w-16 h-16 rounded-full shadow-2xl flex items-center justify-center transition-all transform hover:scale-110">
        <i class="fas fa-robot text-2xl"></i>
    </button>
    <!-- Badge de notification -->
    <span id="chatbot-notification-badge" class="hidden absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center">
        1
    </span>
</div>

<!-- Fenêtre du chatbot -->
<div id="chatbot-container" class="hidden chatbot-container fixed bottom-24 right-6 w-96 max-w-[calc(100vw-3rem)] h-[600px] max-h-[calc(100vh-8rem)] bg-white rounded-2xl shadow-2xl z-[9998] flex flex-col overflow-hidden" style="z-index: 9998;">
    
    <!-- Header -->
    <div class="bg-gradient-to-r from-purple-600 to-blue-600 p-4 flex items-center justify-between">
        <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center">
                <i class="fas fa-robot text-purple-600 text-xl"></i>
            </div>
            <div>
                <h3 class="text-white font-bold">Assistant IA</h3>
                <p class="text-white text-xs opacity-90">
                    <span class="inline-block w-2 h-2 bg-green-400 rounded-full mr-1"></span>
                    En ligne
                </p>
            </div>
        </div>
        <button onclick="toggleChatbot()" class="text-white hover:bg-white hover:bg-opacity-20 w-8 h-8 rounded-full flex items-center justify-center transition-all">
            <i class="fas fa-times"></i>
        </button>
    </div>

    <!-- Messages -->
    <div id="chatbot-messages" class="chatbot-messages flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        <!-- Message de bienvenue -->
        <div class="chatbot-message flex items-start space-x-2">
            <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                <i class="fas fa-robot text-white text-sm"></i>
            </div>
            <div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-md max-w-[80%]">
                <p class="text-gray-800 text-sm">
                    👋 Bonjour ! Je suis votre assistant virtuel. Comment puis-je vous aider aujourd'hui ?
                </p>
            </div>
        </div>
    </div>

    <!-- Suggestions rapides -->
    <div id="chatbot-quick-suggestions" class="p-3 bg-white border-t border-gray-200">
        <p class="text-xs text-gray-500 mb-2">Suggestions :</p>
        <div class="flex flex-wrap gap-2">
            <button onclick="sendQuickChatbotMessage('Voir les produits')" class="text-xs bg-purple-100 text-purple-700 px-3 py-1 rounded-full hover:bg-purple-200 transition-colors">
                📦 Voir les produits
            </button>
            <button onclick="sendQuickChatbotMessage('Suivre ma commande')" class="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full hover:bg-blue-200 transition-colors">
                🚚 Suivre commande
            </button>
            <button onclick="sendQuickChatbotMessage('Aide')" class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full hover:bg-green-200 transition-colors">
                💡 Aide
            </button>
        </div>
    </div>

    <!-- Input -->
    <div class="p-4 bg-white border-t border-gray-200">
        <div class="flex items-center space-x-2">
            <input 
                type="text" 
                id="chatbot-input" 
                placeholder="Tapez votre message..." 
                class="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                onkeypress="handleChatbotKeyPress(event)"
            >
            <button onclick="sendChatbotMessage()" class="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white w-10 h-10 rounded-full flex items-center justify-center transition-all transform hover:scale-110">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>
</div>
`;

// Injecter le chatbot dans la page
document.addEventListener('DOMContentLoaded', function() {
    // Injecter les styles
    document.head.insertAdjacentHTML('beforeend', chatbotStyles);
    
    // Injecter le HTML
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    
    // Initialiser le chatbot
    initChatbot();
});

// Configuration de l'assistant
const CHATBOT_CONFIG = {
    name: "Assistant Prestige Shop",
    welcomeMessage: "Bienvenue sur Prestige Shop Express ! 🎉",
    typing_delay: 1000
};

// Base de connaissances de l'assistant
const chatbotKnowledgeBase = {
    greetings: {
        patterns: ['bonjour', 'salut', 'hello', 'hi', 'bonsoir', 'coucou'],
        responses: [
            "Bonjour ! 👋 Comment puis-je vous aider aujourd'hui ?",
            "Salut ! Je suis là pour vous aider. Que cherchez-vous ?",
            "Bonjour ! Bienvenue sur Prestige Shop Express. En quoi puis-je vous être utile ?"
        ]
    },
    products: {
        patterns: ['produit', 'article', 'voir', 'catalogue', 'acheter', 'vendre'],
        responses: [
            "🛍️ Nous avons une large sélection de produits de qualité ! Vous pouvez parcourir notre catalogue sur cette page. Cherchez-vous quelque chose en particulier ?",
            "📦 Notre boutique propose des produits variés. Faites défiler la page pour voir tous nos articles disponibles !",
            "✨ Découvrez nos produits de prestige ! Ils sont affichés juste en dessous. Besoin d'aide pour trouver quelque chose ?"
        ]
    },
    orders: {
        patterns: ['commande', 'commander', 'acheter', 'panier', 'livraison', 'suivre'],
        responses: [
            "🚚 Pour passer commande, ajoutez simplement les produits à votre panier et cliquez sur 'Commander'. Vous serez redirigé vers WhatsApp pour finaliser.\n\nConnectez-vous pour suivre vos commandes dans 'Mes Commandes' !",
            "📱 Le processus est simple : Panier → Commander → WhatsApp → Livraison !\n\nVous êtes connecté ? Vous pouvez voir toutes vos commandes dans votre profil.",
            "🎯 Pour commander : Choisissez vos produits, validez votre panier, et confirmez par WhatsApp. C'est rapide et sécurisé !"
        ]
    },
    account: {
        patterns: ['connexion', 'compte', 'profil', 'inscription', 'connecter', 'créer compte'],
        responses: [
            "👤 Cliquez sur le bouton 'Connexion' en haut à droite pour vous connecter ou créer un compte.\n\nAvec un compte, vous pouvez suivre vos commandes et profiter d'une expérience personnalisée !",
            "🔐 Créez votre compte gratuitement pour accéder à l'historique de vos commandes et commander plus rapidement !",
            "✅ Cliquez sur 'Connexion' pour vous identifier ou créer un nouveau compte en quelques secondes."
        ]
    },
    payment: {
        patterns: ['prix', 'payer', 'paiement', 'coût', 'combien', 'tarif'],
        responses: [
            "💰 Les prix sont affichés en FCFA sur chaque produit. Le paiement se fait à la livraison ou selon les modalités convenues par WhatsApp.",
            "💵 Tous nos prix sont en Francs CFA. Vous verrez le prix total dans votre panier avant de commander.",
            "🏷️ Les tarifs varient selon les produits. Consultez notre catalogue pour voir les prix détaillés !"
        ]
    },
    help: {
        patterns: ['aide', 'help', 'comment', 'question', 'problème', 'soucis'],
        responses: [
            "💡 Je peux vous aider avec :\n• Voir les produits\n• Passer une commande\n• Créer un compte\n• Suivre une livraison\n• Questions sur les prix\n\nQue souhaitez-vous savoir ?",
            "🤝 Je suis là pour vous ! Posez-moi des questions sur nos produits, comment commander, créer un compte, ou tout autre sujet.",
            "📞 Besoin d'aide ? Je peux vous renseigner sur :\n✓ Nos produits\n✓ Comment commander\n✓ Votre compte\n✓ Le suivi de livraison\n\nQue voulez-vous savoir ?"
        ]
    },
    contact: {
        patterns: ['contact', 'téléphone', 'whatsapp', 'email', 'joindre'],
        responses: [
            "📱 Vous pouvez nous contacter directement via WhatsApp en passant une commande, ou via les informations de contact sur le site.",
            "💬 Notre équipe est disponible sur WhatsApp ! Passez une commande et vous serez en contact direct avec nous.",
            "📞 Pour nous joindre, utilisez notre système de commande WhatsApp intégré !"
        ]
    },
    goodbye: {
        patterns: ['au revoir', 'bye', 'merci', 'adieu', 'à bientôt'],
        responses: [
            "Au revoir ! 👋 N'hésitez pas à revenir si vous avez des questions. Bonne journée !",
            "Merci de votre visite ! 😊 À très bientôt sur Prestige Shop Express !",
            "À bientôt ! 🎉 Nous sommes toujours là pour vous aider !"
        ]
    }
};

// État du chatbot
let chatbotState = {
    isOpen: false,
    messageCount: 0
};

// Fonctions du chatbot
function toggleChatbot() {
    const container = document.getElementById('chatbot-container');
    const badge = document.getElementById('chatbot-notification-badge');
    
    chatbotState.isOpen = !chatbotState.isOpen;
    
    if (chatbotState.isOpen) {
        container.classList.remove('hidden');
        badge.classList.add('hidden');
        scrollChatbotToBottom();
        document.getElementById('chatbot-input').focus();
    } else {
        container.classList.add('hidden');
    }
}

function sendChatbotMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    addChatbotMessage(message, 'user');
    input.value = '';
    
    showChatbotTypingIndicator();
    
    setTimeout(() => {
        hideChatbotTypingIndicator();
        const response = generateChatbotResponse(message);
        addChatbotMessage(response, 'bot');
    }, CHATBOT_CONFIG.typing_delay);
}

function sendQuickChatbotMessage(message) {
    document.getElementById('chatbot-input').value = message;
    sendChatbotMessage();
}

function handleChatbotKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatbotMessage();
    }
}

function addChatbotMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chatbot-message flex items-start space-x-2';
    
    if (sender === 'user') {
        messageDiv.classList.add('flex-row-reverse', 'space-x-reverse');
        messageDiv.innerHTML = `
            <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <i class="fas fa-user text-white text-sm"></i>
            </div>
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl rounded-tr-none p-3 shadow-md max-w-[80%]">
                <p class="text-sm">${text}</p>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                <i class="fas fa-robot text-white text-sm"></i>
            </div>
            <div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-md max-w-[80%]">
                <p class="text-gray-800 text-sm whitespace-pre-line">${text}</p>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    chatbotState.messageCount++;
    scrollChatbotToBottom();
}

function showChatbotTypingIndicator() {
    const messagesContainer = document.getElementById('chatbot-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'chatbot-typing-indicator';
    typingDiv.className = 'chatbot-message flex items-start space-x-2';
    typingDiv.innerHTML = `
        <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
            <i class="fas fa-robot text-white text-sm"></i>
        </div>
        <div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-md">
            <div class="chatbot-typing-indicator">
                <div class="chatbot-typing-dot"></div>
                <div class="chatbot-typing-dot"></div>
                <div class="chatbot-typing-dot"></div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    scrollChatbotToBottom();
}

function hideChatbotTypingIndicator() {
    const indicator = document.getElementById('chatbot-typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function generateChatbotResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    for (const [category, data] of Object.entries(chatbotKnowledgeBase)) {
        for (const pattern of data.patterns) {
            if (message.includes(pattern)) {
                const responses = data.responses;
                return responses[Math.floor(Math.random() * responses.length)];
            }
        }
    }
    
    return "🤔 Je ne suis pas sûr de comprendre. Voici ce que je peux faire pour vous :\n\n• Renseigner sur nos produits\n• Aider avec les commandes\n• Expliquer comment créer un compte\n• Donner des infos sur les livraisons\n\nEssayez de reformuler votre question ou cliquez sur une suggestion ! 😊";
}

function scrollChatbotToBottom() {
    const messagesContainer = document.getElementById('chatbot-messages');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function showChatbotNotification() {
    if (!chatbotState.isOpen) {
        document.getElementById('chatbot-notification-badge').classList.remove('hidden');
    }
}

function initChatbot() {
    setTimeout(() => {
        if (!chatbotState.isOpen) {
            showChatbotNotification();
        }
    }, 5000);
}
