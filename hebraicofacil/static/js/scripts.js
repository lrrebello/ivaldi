// Scripts para a aplicação HebraicoFácil

// Função para formatar campos de entrada
function formatInputFields() {
    // Formatar CPF
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) {
                value = value.substring(0, 11);
            }
            if (value.length > 9) {
                value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*/, '$1.$2.$3-$4');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{3})(\d{3})(\d{3}).*/, '$1.$2.$3');
            } else if (value.length > 3) {
                value = value.replace(/^(\d{3})(\d{3}).*/, '$1.$2');
            }
            e.target.value = value;
        });
    }
    
    // Formatar CEP
    const cepInput = document.getElementById('cep');
    if (cepInput) {
        cepInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 8) {
                value = value.substring(0, 8);
            }
            if (value.length > 5) {
                value = value.replace(/^(\d{5})(\d{3}).*/, '$1-$2');
            }
            e.target.value = value;
        });
    }
    
    // Formatar data de nascimento
    const birthDateInput = document.getElementById('birth_date');
    if (birthDateInput) {
        birthDateInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 8) {
                value = value.substring(0, 8);
            }
            if (value.length > 4) {
                value = value.replace(/^(\d{2})(\d{2})(\d{4}).*/, '$1/$2/$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{2}).*/, '$1/$2');
            }
            e.target.value = value;
        });
    }
    
    // Formatar cartão de crédito
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 16) {
                value = value.substring(0, 16);
            }
            if (value.length > 12) {
                value = value.replace(/^(\d{4})(\d{4})(\d{4})(\d{4}).*/, '$1 $2 $3 $4');
            } else if (value.length > 8) {
                value = value.replace(/^(\d{4})(\d{4})(\d{4}).*/, '$1 $2 $3');
            } else if (value.length > 4) {
                value = value.replace(/^(\d{4})(\d{4}).*/, '$1 $2');
            }
            e.target.value = value;
        });
    }
    
    // Formatar validade do cartão
    const cardExpiryInput = document.getElementById('card_expiry');
    if (cardExpiryInput) {
        cardExpiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 4) {
                value = value.substring(0, 4);
            }
            if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{2}).*/, '$1/$2');
            }
            e.target.value = value;
        });
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    formatInputFields();
});