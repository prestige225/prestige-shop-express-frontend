/**
 * Script utilitaire pour le panier et les commandes
 * Ajoute des fonctionnalités complémentaires sans modifier index.html
 */

// Fonction pour pré-remplir le formulaire de commande avec les données utilisateur
function autofillCustomerForm() {
    const userData = JSON.parse(localStorage.getItem('userData') || sessionStorage.getItem('userData') || '{}');
    
    if (userData && userData.id) {
        // Remplir le nom si vide
        const nameField = document.getElementById('customer-name');
        if (nameField && !nameField.value.trim()) {
            nameField.value = `${userData.prenom || ''} ${userData.nom || ''}`.trim();
        }
        
        // Remplir le téléphone si vide
        const phoneField = document.getElementById('customer-phone');
        if (phoneField && !phoneField.value.trim()) {
            phoneField.value = userData.telephone || '';
        }
    }
}

// Surveillance l'ouverture du panier et auto-remplissage
const originalToggleCart = window.toggleCart;
if (originalToggleCart) {
    window.toggleCart = function() {
        const modal = document.getElementById('cart-modal');
        if (modal.classList.contains('hidden')) {
            // Le panier va s'ouvrir, on attend qu'il soit affiché
            setTimeout(() => {
                autofillCustomerForm();
            }, 100);
        }
        originalToggleCart.apply(this, arguments);
    };
}

// Surveillance également de displayCart
const originalDisplayCart = window.displayCart;
if (originalDisplayCart) {
    window.displayCart = function() {
        const result = originalDisplayCart.apply(this, arguments);
        // Après affichage du panier, pré-remplir le formulaire
        setTimeout(() => {
            autofillCustomerForm();
        }, 100);
        return result;
    };
}

console.log('✅ Script cart-utils chargé - Auto-remplissage du formulaire activé');
