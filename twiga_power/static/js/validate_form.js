// Exécution du script une fois que tout le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    // Sélection du formulaire personnalisé avec validation
    const form = document.querySelector('#customValidationForm');
  
    // Récupération de tous les champs du formulaire (inputs, textarea, select)
    const inputs = form.querySelectorAll('input, textarea, select');
  
    // Gestion de la soumission du formulaire
    form.addEventListener('submit', (event) => {
        let isValid = true;
  
        // Parcours de tous les champs du formulaire
        inputs.forEach((input) => {
            // Si un champ est invalide, on le valide manuellement
            if (!input.checkValidity()) {
                isValid = false;
                validateField(input); // Affiche les erreurs si présentes
            }
        });
  
        // Si au moins un champ est invalide, on empêche l’envoi du formulaire
        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
  
            // Ajout d’une classe CSS pour styliser les champs invalides (ex: Bootstrap)
            form.classList.add('was-validated');
        }
    });
  
    // Ajout d’écouteurs sur chaque champ pour valider automatiquement
    // lors de la saisie (input) ou lorsqu'on quitte le champ (blur)
    inputs.forEach((input) => {
        input.addEventListener('input', () => validateField(input));
        input.addEventListener('blur', () => validateField(input));
    });
  
    /**
     * Fonction de validation personnalisée d’un champ
     * @param {HTMLElement} field - Champ à valider
     */
    function validateField(field) {
        let feedback = field.nextElementSibling; // Élément suivant pour le message d’erreur
  
        if (!feedback) return; // Si pas de feedback (ex: <div class="invalid-feedback">), on quitte
  
        // Si le champ est valide, on met les bonnes classes et on vide le message
        if (feedback && field.validity.valid) {
            field.classList.remove("is-invalid");
            field.classList.add("is-valid");
            feedback.textContent = '';
        } else {
            // Sinon, on marque le champ comme invalide
            field.classList.remove("is-valid");
            field.classList.add("is-invalid");
  
            // Affichage de messages d’erreur personnalisés selon le type d'erreur
            if (field.validity.valueMissing) {
                feedback.textContent = `Ce champ ne peut pas être laissé vide !`;
            } else if (field.validity.tooShort) {
                feedback.textContent = `Ce champ doit contenir au moins ${field.minLength || 0} caractères !`;
            } else if (field.validity.tooLong) {
                feedback.textContent = `Ce champ ne doit pas dépasser ${field.maxLength || 0} caractères !`;
            } else if (field.validity.patternMismatch) {
                feedback.textContent = `Veuillez respecter le format requis pour ce champ !`;
            } else if (field.type === 'radio' && !isRadioGroupValid(field)) {
                feedback.textContent = `Ce champ ne peut pas être laissé vide !`;
            } else if (field.type === 'checkbox' && !isCheckboxValid(field)) {
                feedback.textContent = `Ce champ ne peut pas être laissé vide !`;
            } else {
                feedback.textContent = `Ce champ est invalide !`;
            }
        }
    }
  
    /**
     * Vérifie si au moins une option est sélectionnée dans un groupe de boutons radio
     * @param {HTMLInputElement} radio - Un des boutons radio du groupe
     * @returns {boolean} - true si au moins un est coché
     */
    function isRadioGroupValid(radio) {
        const radioGroup = document.querySelectorAll(`input[name="${radio.name}"]`);
        return Array.from(radioGroup).some(radio => radio.checked);
    }
  
    /**
     * Vérifie si une case à cocher est bien cochée
     * @param {HTMLInputElement} checkbox
     * @returns {boolean}
     */
    function isCheckboxValid(checkbox) {
        return checkbox.checked;
    }
  });
  