// Funções de formatação para campos de formulário
const Masks = {
    // Remove todos os caracteres não numéricos
    onlyNumbers: (value) => value.replace(/\D/g, ''),

    // Formata CPF: 000.000.000-00
    cpf: (value) => {
        value = value.replace(/\D/g, '');
        if (value.length > 11) value = value.substring(0, 11);
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        return value;
    },

    // Formata RG: 00.000.000-0
    rg: (value) => {
        value = value.replace(/\D/g, '');
        if (value.length > 9) value = value.substring(0, 9);
        value = value.replace(/(\d{2})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1})$/, '$1-$2');
        return value;
    },

    // Formata telefone: (00) 00000-0000 ou (00) 0000-0000
    telefone: (value) => {
        value = value.replace(/\D/g, '');
        if (value.length > 11) value = value.substring(0, 11);
        
        // Formato para celular (11 dígitos)
        if (value.length > 10) {
            value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
        } 
        // Formato para telefone fixo (10 dígitos)
        else {
            value = value.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
        }
        return value;
    },

    // Formata CEP: 00000-000
    cep: (value) => {
        value = value.replace(/\D/g, '');
        if (value.length > 8) value = value.substring(0, 8);
        value = value.replace(/^(\d{5})(\d{3})$/, '$1-$2');
        return value;
    },

    // Formata data: dd/mm/aaaa
    data: (value) => {
        value = value.replace(/\D/g, '');
        if (value.length > 8) value = value.substring(0, 8);
        value = value.replace(/(\d{2})(\d)/, '$1/$2');
        value = value.replace(/(\d{2})(\d)/, '$1/$2');
        return value;
    }
};

// Funções de validação
const Validators = {
    // Valida CPF
    cpf: (cpf) => {
        cpf = cpf.replace(/\D/g, '');
        if (cpf.length !== 11) return false;
        
        // Verifica se todos os dígitos são iguais
        if (/^(\d)\1+$/.test(cpf)) return false;
        
        // Calcula dígitos verificadores
        let soma = 0;
        let resto;
        
        for (let i = 1; i <= 9; i++) {
            soma = soma + parseInt(cpf.substring(i-1, i)) * (11 - i);
        }
        
        resto = (soma * 10) % 11;
        if ((resto === 10) || (resto === 11)) resto = 0;
        if (resto !== parseInt(cpf.substring(9, 10))) return false;
        
        soma = 0;
        for (let i = 1; i <= 10; i++) {
            soma = soma + parseInt(cpf.substring(i-1, i)) * (12 - i);
        }
        
        resto = (soma * 10) % 11;
        if ((resto === 10) || (resto === 11)) resto = 0;
        if (resto !== parseInt(cpf.substring(10, 11))) return false;
        
        return true;
    },

    // Valida data
    data: (data) => {
        if (!data) return false;
        
        const [dia, mes, ano] = data.split('/').map(Number);
        const dataObj = new Date(ano, mes - 1, dia);
        
        return dataObj.getDate() === dia &&
               dataObj.getMonth() === mes - 1 &&
               dataObj.getFullYear() === ano &&
               ano > 1900 &&
               ano < new Date().getFullYear();
    },

    // Valida telefone
    telefone: (telefone) => {
        const numeros = telefone.replace(/\D/g, '');
        return numeros.length >= 10 && numeros.length <= 11;
    },

    // Valida CEP
    cep: (cep) => {
        const numeros = cep.replace(/\D/g, '');
        return numeros.length === 8;
    }
};

// Função para aplicar máscara a um campo
function applyMask(input, maskFunction, validatorFunction = null) {
    const updateValue = (e) => {
        const cursorPosition = e.target.selectionStart;
        const originalLength = e.target.value.length;
        const newValue = maskFunction(e.target.value);
        e.target.value = newValue;
        
        // Mantém o cursor na posição correta após a formatação
        if (cursorPosition < originalLength) {
            e.target.setSelectionRange(cursorPosition, cursorPosition);
        }
        
        // Aplica validação se houver
        if (validatorFunction) {
            const isValid = validatorFunction(newValue);
            input.classList.toggle('is-invalid', !isValid);
            input.classList.toggle('is-valid', isValid);
            
            // Atualiza o feedback visual
            const feedbackElement = input.nextElementSibling;
            if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
                feedbackElement.style.display = isValid ? 'none' : 'block';
            }
        }
    };

    // Aplica a máscara no evento input
    input.addEventListener('input', updateValue);
    
    // Aplica a máscara no evento blur (quando o campo perde o foco)
    input.addEventListener('blur', updateValue);
    
    // Aplica a máscara inicialmente se já houver valor
    if (input.value) {
        const event = new Event('input', { bubbles: true });
        input.dispatchEvent(event);
    }
}

// Função para inicializar todas as máscaras
function initializeMasks() {
    // CPF
    const cpfInputs = document.querySelectorAll('input[data-mask="cpf"]');
    cpfInputs.forEach(input => applyMask(input, Masks.cpf, Validators.cpf));

    // RG
    const rgInputs = document.querySelectorAll('input[data-mask="rg"]');
    rgInputs.forEach(input => applyMask(input, Masks.rg));

    // Telefone
    const telefoneInputs = document.querySelectorAll('input[data-mask="telefone"]');
    telefoneInputs.forEach(input => applyMask(input, Masks.telefone, Validators.telefone));

    // CEP
    const cepInputs = document.querySelectorAll('input[data-mask="cep"]');
    cepInputs.forEach(input => applyMask(input, Masks.cep, Validators.cep));

    // Data
    const dataInputs = document.querySelectorAll('input[data-mask="data"]');
    dataInputs.forEach(input => applyMask(input, Masks.data, Validators.data));
}

// Inicializa as máscaras quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', initializeMasks);

// Exporta as funções para uso global
window.Masks = Masks;
window.Validators = Validators;
window.applyMask = applyMask;
window.initializeMasks = initializeMasks; 