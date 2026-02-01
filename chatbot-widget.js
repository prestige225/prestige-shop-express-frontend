// ======================================
// CHATBOT WIDGET POUR PRESTIGE SHOP EXPRESS
// ======================================

// Variables pour la synthèse vocale et la reconnaissance vocale
let recognition;

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
    
    /* Bouton vocal */
    .chatbot-voice-button {
        position: absolute;
        top: -40px;
        right: 60px;
        background: #9333ea;
        color: white;
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .chatbot-voice-button:hover {
        background: #7c3aed;
        transform: scale(1.1);
    }
    
    .chatbot-voice-button.recording {
        background: #ef4444;
        animation: chatbot-pulse 1.5s infinite;
    }
    
    @keyframes chatbot-pulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    
    /* Animation de la main pour salutation */
    .chatbot-wave-hand {
        display: inline-block;
        animation: chatbot-wave 2s ease-in-out infinite;
        transform-origin: 70% 70%;
    }
    
    @keyframes chatbot-wave {
        0% { transform: rotate(0deg); }
        10% { transform: rotate(14deg); }
        20% { transform: rotate(-8deg); }
        30% { transform: rotate(14deg); }
        40% { transform: rotate(-4deg); }
        50% { transform: rotate(10deg); }
        60% { transform: rotate(0deg); }
        100% { transform: rotate(0deg); }
    }
    
    /* Animation d'attention pour PrestIA */
    .chatbot-attention-highlight {
        animation: chatbot-highlight 2s ease-in-out infinite;
        background: linear-gradient(45deg, #9333ea, #7c3aed, #9333ea);
        background-size: 200% 200%;
        border-radius: 10px;
        padding: 2px 6px;
        color: white;
        font-weight: bold;
    }
    
    @keyframes chatbot-highlight {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animation spéciale pour la salutation */
    .chatbot-greeting-animation {
        animation: chatbot-greeting-pop 0.5s ease-out;
    }
    
    @keyframes chatbot-greeting-pop {
        0% { transform: scale(0.5); opacity: 0; }
        70% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
`;

// Injecter le HTML du chatbot
const chatbotHTML = `
<!-- Bouton du chatbot flottant -->
<div id="chatbot-button" class="chatbot-button-float fixed bottom-6 right-6 left-auto z-[9999]" style="z-index: 9999;">
    <button onclick="toggleChatbot()" class="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white w-16 h-16 rounded-full shadow-2xl flex items-center justify-center transition-all transform hover:scale-110">
        <i class="fas fa-robot text-2xl"></i>
    </button>
    <!-- Badge de notification -->
    <span id="chatbot-notification-badge" class="hidden absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center">
        1
    </span>
</div>

<!-- Fenêtre du chatbot -->
<div id="chatbot-container" class="hidden chatbot-container fixed bottom-24 right-6 left-auto w-96 max-w-[calc(100vw-3rem)] h-[600px] max-h-[calc(100vh-8rem)] bg-white rounded-2xl shadow-2xl z-[9998] flex flex-col overflow-hidden" style="z-index: 9998;">
    
    <!-- Header -->
    <div class="bg-gradient-to-r from-purple-600 to-blue-600 p-4 flex items-center justify-between relative">
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
        <!-- Bouton vocal -->
        <button id="chatbot-voice-toggle" class="chatbot-voice-button" onclick="toggleVoiceAssistant()">
            <i class="fas fa-microphone"></i>
        </button>
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
    
    // Injecter le HTML avec un message de bienvenue personnalisé
    const personalizedWelcome = getPersonalizedWelcomeMessage();
    const chatbotHTMLWithWelcome = chatbotHTML.replace(
        '👋 Bonjour ! Je suis votre assistant virtuel. Comment puis-je vous aider aujourd\'hui ?',
        personalizedWelcome
    );
    document.body.insertAdjacentHTML('beforeend', chatbotHTMLWithWelcome);
    
    // Initialiser le chatbot
    initChatbot();
    
    // Initialiser la reconnaissance vocale
    initSpeechRecognition();
    
    // Ajouter des écouteurs d'événements pour détecter l'interaction utilisateur
    document.addEventListener('click', function() {
        if (!chatbotState.userHasInteracted) {
            chatbotState.userHasInteracted = true;
            triggerPendingSpeech();
        }
    }, { once: true });
    
    document.addEventListener('touchstart', function() {
        if (!chatbotState.userHasInteracted) {
            chatbotState.userHasInteracted = true;
            triggerPendingSpeech();
        }
    }, { once: true });
});

// Configuration de l'assistant
const CHATBOT_CONFIG = {
    name: "PrestIA",
    welcomeMessage: "Bienvenue sur Prestige Shop Express ! 🎉",
    typing_delay: 1000,
    // Messages de présentation vocale
    voiceIntroduction: [
        "Bonjour et bienvenue sur Prestige Shop Express !",
        "Je suis PrestIA, votre assistant vocal personnel.",
        "Je peux vous aider à trouver des produits, passer des commandes et répondre à vos questions.",
        "Pour une recherche plus rapide, cliquez sur nos différentes catégories :",
        "Mode, si vous recherchez des vêtements et accessoires de mode.",
        "Éducatif, si vous cherchez des fournitures scolaires et éducatives.",
        "Électronique, si vous voulez des appareils technologiques.",
        "Fast food, si vous désirez des plats rapides et délicieux.",
        "Dites-moi, que recherchez-vous aujourd'hui ?"
    ],
    // Questions vocales interactives
    voiceQuestions: [
        "Souhaitez-vous voir nos produits ?",
        "Avez-vous besoin d'aide pour passer une commande ?",
        "Souhaitez-vous créer un compte ou vous connecter ?"
    ]
};

// Base de connaissances de l'assistant
const chatbotKnowledgeBase = {
    greetings: {
        patterns: ['bonjour', 'salut', 'hello', 'hi', 'bonsoir', 'coucou', 'slt', 'bjr'],
        responses: [
            "<span class='chatbot-wave-hand'>👋</span> Bonjour ! Je suis <span class='chatbot-attention-highlight'>PrestIA</span>, votre assistant virtuel. Comment puis-je vous aider aujourd'hui ?",
            "<span class='chatbot-wave-hand'>👋</span> Salut ! Je suis <span class='chatbot-attention-highlight'>PrestIA</span>, là pour vous aider. Que cherchez-vous ?",
            "<span class='chatbot-wave-hand'>👋</span> Bonjour ! Je suis <span class='chatbot-attention-highlight'>PrestIA</span> de Prestige Shop Express. En quoi puis-je vous être utile ?"
        ]
    },
    products: {
        patterns: ['produit', 'article', 'voir', 'catalogue', 'acheter', 'vendre'],
        responses: [
            "🛍️ Nous avons une large sélection de produits de qualité ! Vous pouvez parcourir notre catalogue sur cette page. Pour une recherche plus rapide, cliquez sur nos différentes catégories :\n\n• <span class='chatbot-attention-highlight'>Mode</span> : Vêtements et accessoires de mode\n• <span class='chatbot-attention-highlight'>Beauté & Cosmétique</span> : Soins et maquillage\n• <span class='chatbot-attention-highlight'>Éducatif</span> : Fournitures scolaires et éducatives\n• <span class='chatbot-attention-highlight'>Électronique</span> : Appareils technologiques\n• <span class='chatbot-attention-highlight'>Fast food</span> : Plats rapides et délicieux\n\nCherchez-vous quelque chose en particulier ?",
            "📦 Notre boutique propose des produits variés. Faites défiler la page pour voir tous nos articles disponibles ! Pour trouver plus rapidement ce que vous cherchez, utilisez nos catégories :\n\n<span class='chatbot-attention-highlight'>Mode</span> pour les vêtements, <span class='chatbot-attention-highlight'>Beauté & Cosmétique</span> pour les soins et maquillage, <span class='chatbot-attention-highlight'>Éducatif</span> pour les fournitures scolaires, <span class='chatbot-attention-highlight'>Électronique</span> pour les gadgets, <span class='chatbot-attention-highlight'>Fast food</span> pour les plats.\n\nBesoin d'aide pour trouver quelque chose ?",
            "✨ Découvrez nos produits de prestige ! Ils sont affichés juste en dessous. Pour une recherche optimale, cliquez sur les catégories :\n\n👉 <span class='chatbot-attention-highlight'>Mode</span> : Si vous recherchez des vêtements\n👉 <span class='chatbot-attention-highlight'>Beauté & Cosmétique</span> : Si vous voulez des soins et maquillage\n👉 <span class='chatbot-attention-highlight'>Éducatif</span> : Si vous voulez des fournitures scolaires\n👉 <span class='chatbot-attention-highlight'>Électronique</span> : Si vous désirez des appareils technologiques\n👉 <span class='chatbot-attention-highlight'>Fast food</span> : Si vous cherchez des plats rapides\n\nQue désirez-vous explorer ?"
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
            "💡 Je peux vous aider avec :\n• Voir les produits\n• Passer une commande\n• Créer un compte\n• Suivre une livraison\n• Questions sur les prix\n\nPour trouver rapidement ce que vous cherchez, utilisez nos catégories :\n<span class='chatbot-attention-highlight'>Mode</span>, <span class='chatbot-attention-highlight'>Éducatif</span>, <span class='chatbot-attention-highlight'>Électronique</span>, <span class='chatbot-attention-highlight'>Fast food</span>\n\nQue souhaitez-vous savoir ?",
            "🤝 Je suis là pour vous ! Posez-moi des questions sur nos produits, comment commander, créer un compte, ou tout autre sujet.\n\nPour une recherche plus efficace, cliquez sur nos catégories principales :\n• <span class='chatbot-attention-highlight'>Mode</span> pour les vêtements\n• <span class='chatbot-attention-highlight'>Éducatif</span> pour les fournitures\n• <span class='chatbot-attention-highlight'>Électronique</span> pour les gadgets\n• <span class='chatbot-attention-highlight'>Fast food</span> pour les plats",
            "📞 Besoin d'aide ? Je peux vous renseigner sur :\n✓ Nos produits\n✓ Comment commander\n✓ Votre compte\n✓ Le suivi de livraison\n\nPour trouver rapidement ce que vous cherchez, utilisez les catégories en haut de la page !"
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
        patterns: ['au revoir', 'bye', 'merci', 'adieu', 'à bientôt', 'bye bye'],
        responses: [
            "Au revoir ! 👋 N'hésitez pas à revenir si vous avez des questions. Bonne journée !",
            "Merci de votre visite ! 😊 À très bientôt sur Prestige Shop Express !",
            "À bientôt ! 🎉 Nous sommes toujours là pour vous aider !"
        ]
    },
    categories: {
        patterns: ['categorie', 'catégorie', 'recherche', 'trouver', 'chercher', 'mode', 'educatif', 'electronique', 'fast food'],
        responses: [
            "🔍 Pour une recherche plus rapide, utilisez nos catégories principales :\n\n<span class='chatbot-attention-highlight'>Mode</span> : Vêtements et accessoires de mode\n<span class='chatbot-attention-highlight'>Éducatif</span> : Fournitures scolaires et éducatives\n<span class='chatbot-attention-highlight'>Électronique</span> : Appareils technologiques\n<span class='chatbot-attention-highlight'>Fast food</span> : Plats rapides et délicieux\n\nCliquez simplement sur la catégorie qui correspond à ce que vous recherchez !",
            "🎯 Pour trouver rapidement ce que vous cherchez, cliquez sur nos catégories :\n\n👉 <span class='chatbot-attention-highlight'>Mode</span> si vous recherchez des vêtements\n👉 <span class='chatbot-attention-highlight'>Éducatif</span> si vous voulez des fournitures scolaires\n👉 <span class='chatbot-attention-highlight'>Électronique</span> si vous désirez des appareils technologiques\n👉 <span class='chatbot-attention-highlight'>Fast food</span> si vous cherchez des plats rapides\n\nChaque catégorie vous mènera directement aux produits correspondants !",
            "✨ Facilitez votre recherche avec nos catégories principales :\n\n• <span class='chatbot-attention-highlight'>Mode</span> pour les vêtements et accessoires\n• <span class='chatbot-attention-highlight'>Éducatif</span> pour les fournitures scolaires\n• <span class='chatbot-attention-highlight'>Électronique</span> pour les gadgets et appareils\n• <span class='chatbot-attention-highlight'>Fast food</span> pour les plats délicieux\n\nCliquez sur une catégorie pour explorer les produits correspondants !"
        ]
    }
};

// État du chatbot
let chatbotState = {
    isOpen: false,
    messageCount: 0,
    isVoiceEnabled: true,
    isSpeaking: false,
    isFirstGreeting: true,
    autoOpenOnMessage: false,  // Désactivé par défaut
    userHasInteracted: false,  // Nouvelle propriété pour suivre l'interaction utilisateur
    pendingSpeech: null      // Nouvelle propriété pour stocker le texte en attente de lecture
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
        
        // Présentation vocale automatique lors de l'ouverture du chatbot pour la première fois
        if (chatbotState.messageCount === 1) {
            setTimeout(() => {
                speakIntroduction();
            }, 1000);
        }
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
        
        // Lire la réponse à haute voix si la fonction vocale est activée
        if (chatbotState.isVoiceEnabled) {
            speakText(response);
        }
        
        // Vérifier si c'est une salutation et déclencher l'animation spéciale
        if (isGreeting(message) && chatbotState.isFirstGreeting) {
            chatbotState.isFirstGreeting = false;
            showSpecialGreetingAnimation();
        }
    }, CHATBOT_CONFIG.typing_delay);
}

function isGreeting(message) {
    const lowerMessage = message.toLowerCase();
    const greetingPatterns = ['bonjour', 'salut', 'hello', 'hi', 'bonsoir', 'coucou', 'slt', 'bjr'];
    return greetingPatterns.some(pattern => lowerMessage.includes(pattern));
}

function showSpecialGreetingAnimation() {
    // Créer une animation spéciale pour la première salutation
    const messagesContainer = document.getElementById('chatbot-messages');
    const animationDiv = document.createElement('div');
    animationDiv.className = 'chatbot-message flex items-center justify-center my-2 chatbot-greeting-animation';
    animationDiv.innerHTML = `
        <div class="bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-2xl p-4 shadow-lg">
            <div class="flex items-center space-x-2">
                <span class="chatbot-wave-hand text-2xl">👋</span>
                <span class="font-bold chatbot-attention-highlight">Je suis PrestIA, votre assistant personnel !</span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(animationDiv);
    scrollChatbotToBottom();
    
    // Lire le message d'animation à haute voix
    if (chatbotState.isVoiceEnabled) {
        speakText("Je suis PrestIA, votre assistant personnel !");
    }
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
                <p class="text-gray-800 text-sm whitespace-pre-line"></p>
            </div>
        `;
        
        // Ajouter le texte avec les animations HTML
        const textElement = messageDiv.querySelector('.text-gray-800');
        textElement.innerHTML = text;
    }
    
    messagesContainer.appendChild(messageDiv);
    chatbotState.messageCount++;
    
    // Ouvrir automatiquement le chatbot lorsqu'un message est ajouté (sauf pour le message de bienvenue initial)
    if (chatbotState.autoOpenOnMessage && chatbotState.messageCount > 1) {
        openChatbotAutomatically();
    }
    
    scrollChatbotToBottom();
}

// Nouvelle fonction pour ouvrir automatiquement le chatbot
function openChatbotAutomatically() {
    const container = document.getElementById('chatbot-container');
    const badge = document.getElementById('chatbot-notification-badge');
    
    // Si le chatbot n'est pas déjà ouvert, l'ouvrir
    if (!chatbotState.isOpen) {
        chatbotState.isOpen = true;
        container.classList.remove('hidden');
        badge.classList.add('hidden');
        scrollChatbotToBottom();
        document.getElementById('chatbot-input').focus();
    }
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
    const user = getLoggedInUser();
    
    // Vérifier si c'est une salutation et personnaliser la réponse
    if (isGreeting(message)) {
        if (user && user.prenom) {
            return `<span class='chatbot-wave-hand'>👋</span> Bonjour ${user.prenom} ! Je suis <span class='chatbot-attention-highlight'>PrestIA</span>, votre assistant personnel. Comment puis-je vous aider aujourd'hui ?`;
        }
    }
    
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
    // Présentation vocale automatique au chargement de la page (après 3 secondes)
    setTimeout(() => {
        if (chatbotState.isVoiceEnabled) {
            speakIntroduction();
            // Ne plus ouvrir automatiquement le chatbot lors de la présentation vocale
            // openChatbotAutomatically();
        }
    }, 3000);
    
    // Notification après 5 secondes si le chatbot n'est pas ouvert
    setTimeout(() => {
        if (!chatbotState.isOpen) {
            showChatbotNotification();
        }
    }, 5000);
}

// Fonctions de synthèse vocale
function speakText(text) {
    // Vérifier si nous sommes sur un appareil mobile
    const isMobile = isMobileDevice();
    
    // Sur mobile, ne pas lire automatiquement sans interaction utilisateur
    if (isMobile && !chatbotState.userHasInteracted) {
        console.log("Synthèse vocale différée sur mobile - attente d'interaction utilisateur");
        // Stocker le texte à lire plus tard
        chatbotState.pendingSpeech = text;
        return;
    }
    
    if (!chatbotState.isVoiceEnabled || 'speechSynthesis' in window === false) {
        return;
    }
    
    // Nettoyer le texte des balises HTML pour la synthèse vocale
    const cleanText = text.replace(/<[^>]*>/g, '');
    
    // Annuler toute parole en cours
    window.speechSynthesis.cancel();
    
    // Créer un objet d’énonciation
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'fr-FR';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    
    // Définir les événements
    utterance.onstart = () => {
        chatbotState.isSpeaking = true;
        updateVoiceButtonState();
    };
    
    utterance.onend = () => {
        chatbotState.isSpeaking = false;
        updateVoiceButtonState();
        chatbotState.pendingSpeech = null; // Effacer le texte en attente
    };
    
    utterance.onerror = (event) => {
        console.error('Erreur de synthèse vocale:', event.error);
        chatbotState.isSpeaking = false;
        updateVoiceButtonState();
        chatbotState.pendingSpeech = null; // Effacer le texte en attente
    };
    
    // Parler
    try {
        window.speechSynthesis.speak(utterance);
    } catch (error) {
        console.error('Erreur lors de la synthèse vocale:', error);
    }
}

function speakIntroduction() {
    const user = getLoggedInUser();
    let introductionText = "";
    
    if (user && user.prenom) {
        introductionText = `Bonjour ${user.prenom} et bienvenue sur Prestige Shop Express ! Je suis PrestIA, votre assistant vocal personnel. Je peux vous aider à trouver des produits, passer des commandes et répondre à vos questions. Pour une recherche plus rapide, cliquez sur nos différentes catégories : Mode, si vous recherchez des vêtements et accessoires de mode. Éducatif, si vous cherchez des fournitures scolaires et éducatives. Électronique, si vous voulez des appareils technologiques. Fast food, si vous désirez des plats rapides et délicieux. Dites-moi ${user.prenom}, que recherchez-vous aujourd'hui ?`;
    } else {
        introductionText = CHATBOT_CONFIG.voiceIntroduction.join(" ");
    }
    
    speakText(introductionText);
    
    // Poser les questions interactives après l'introduction
    setTimeout(() => {
        if (chatbotState.isVoiceEnabled) {
            let question = "";
            if (user && user.prenom) {
                question = `Souhaitez-vous voir nos produits ${user.prenom} ?`;
            } else {
                question = CHATBOT_CONFIG.voiceQuestions[Math.floor(Math.random() * CHATBOT_CONFIG.voiceQuestions.length)];
            }
            speakText(question);
        }
    }, introductionText.length * 100 + 1000); // Attendre la fin de l'introduction
}

function updateVoiceButtonState() {
    const voiceButton = document.getElementById('chatbot-voice-toggle');
    const icon = voiceButton.querySelector('i');
    
    if (chatbotState.isVoiceEnabled) {
        if (chatbotState.isSpeaking) {
            icon.className = 'fas fa-volume-up';
        } else {
            icon.className = 'fas fa-microphone';
        }
    } else {
        icon.className = 'fas fa-microphone-slash';
    }
}

// Nouvelle fonction pour déclencher la lecture vocale en attente
function triggerPendingSpeech() {
    // Marquer que l'utilisateur a interagi
    chatbotState.userHasInteracted = true;
    
    // Si nous avons un texte en attente, le lire
    if (chatbotState.pendingSpeech) {
        const textToSpeak = chatbotState.pendingSpeech;
        chatbotState.pendingSpeech = null;
        speakText(textToSpeak);
    }
}

// Modifier la fonction toggleVoiceAssistant pour déclencher la lecture en attente
function toggleVoiceAssistant() {
    chatbotState.isVoiceEnabled = !chatbotState.isVoiceEnabled;
    updateVoiceButtonState();
    
    if (chatbotState.isVoiceEnabled) {
        // Si activé, faire une petite présentation
        speakText("L'assistant vocal est maintenant activé.");
        // Déclencher également la lecture en attente si elle existe
        triggerPendingSpeech();
    } else {
        // Si désactivé, arrêter toute parole en cours
        window.speechSynthesis.cancel();
        chatbotState.isSpeaking = false;
    }
}

// Fonctions de reconnaissance vocale
function initSpeechRecognition() {
    // Vérifier si l'API Web Speech est disponible
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'fr-FR';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('chatbot-input').value = transcript;
            sendChatbotMessage();
            updateVoiceButtonState();
        };
        
        recognition.onerror = function(event) {
            console.error('Erreur de reconnaissance vocale:', event.error);
            updateVoiceButtonState();
        };
        
        recognition.onend = function() {
            updateVoiceButtonState();
        };
    }
}

// Fonction de test pour l'animation de la main (pour débogage)
function testHandAnimation() {
    // Créer un élément de test pour l'animation de la main
    const testDiv = document.createElement('div');
    testDiv.innerHTML = `<span class="chatbot-wave-hand">👋</span> Test d'animation`;
    testDiv.style.position = 'fixed';
    testDiv.style.top = '20px';
    testDiv.style.right = '20px';
    testDiv.style.zIndex = '99999';
    testDiv.style.background = 'white';
    testDiv.style.padding = '10px';
    testDiv.style.borderRadius = '10px';
    testDiv.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    
    document.body.appendChild(testDiv);
    
    // Supprimer l'élément de test après 5 secondes
    setTimeout(() => {
        if (testDiv.parentNode) {
            testDiv.parentNode.removeChild(testDiv);
        }
    }, 5000);
}

function startVoiceRecognition() {
    if (recognition && chatbotState.isVoiceEnabled) {
        const voiceButton = document.getElementById('chatbot-voice-toggle');
        voiceButton.classList.add('recording');
        recognition.start();
    }
}

function stopVoiceRecognition() {
    if (recognition) {
        const voiceButton = document.getElementById('chatbot-voice-toggle');
        voiceButton.classList.remove('recording');
        recognition.stop();
    }
}

// Fonction pour obtenir le nom de l'utilisateur connecté
function getLoggedInUser() {
    // Vérifier d'abord dans localStorage
    let userData = localStorage.getItem('userData');
    if (userData) {
        try {
            const user = JSON.parse(userData);
            return user;
        } catch (e) {
            console.error('Erreur lors du parsing des données utilisateur depuis localStorage:', e);
        }
    }
    
    // Vérifier dans sessionStorage
    userData = sessionStorage.getItem('userData');
    if (userData) {
        try {
            const user = JSON.parse(userData);
            return user;
        } catch (e) {
            console.error('Erreur lors du parsing des données utilisateur depuis sessionStorage:', e);
        }
    }
    
    return null;
}

// Fonction pour personnaliser le message de bienvenue
function getPersonalizedWelcomeMessage() {
    const user = getLoggedInUser();
    if (user && user.prenom) {
        return `<span class='chatbot-wave-hand'>👋</span> Bonjour ${user.prenom} ! Je suis <span class='chatbot-attention-highlight'>PrestIA</span>, votre assistant virtuel. Comment puis-je vous aider aujourd'hui ?`;
    }
    return `<span class='chatbot-wave-hand'>👋</span> Bonjour ! Je suis <span class='chatbot-attention-highlight'>PrestIA</span>, votre assistant virtuel. Comment puis-je vous aider aujourd'hui ?`;
}

// Nouvelle fonction pour détecter les appareils mobiles
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}
