// Scripts para o sistema de cadastro de alunos

document.addEventListener('DOMContentLoaded', function() {
    // --- 1. Preview da Foto ---
    const fotoInput = document.getElementById('foto');
    const fotoPreview = document.getElementById('fotoPreview');
    const semFoto = document.getElementById('semFoto');

    if (fotoInput && fotoPreview) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    fotoPreview.src = e.target.result;
                    fotoPreview.classList.remove('d-none');
                    if (semFoto) semFoto.classList.add('d-none');
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // --- 2. Calcular idade automaticamente ---
    const dataNascimentoInput = document.getElementById('data_nascimento');
    const idadePreview = document.getElementById('idade_preview');

    function calcularIdade() {
        const dataValor = dataNascimentoInput.value;
        if (dataValor) {
            // Divide a string YYYY-MM-DD para evitar problemas de fuso horário do objeto Date
            const partes = dataValor.split('-');
            const nascimento = new Date(partes[0], partes[1] - 1, partes[2]);
            const hoje = new Date();
            
            let idade = hoje.getFullYear() - nascimento.getFullYear();
            const mes = hoje.getMonth() - nascimento.getMonth();

            if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
                idade--;
            }

            if (!isNaN(idade) && idade >= 0) {
                idadePreview.textContent = idade + ' anos';
                idadePreview.className = 'badge bg-success';
            } else {
                idadePreview.textContent = '--';
                idadePreview.className = 'badge bg-info';
            }
        }
    }

    if (dataNascimentoInput && idadePreview) {
        // Escuta tanto 'input' quanto 'change' para garantir funcionamento em todos browsers
        dataNascimentoInput.addEventListener('input', calcularIdade);
        dataNascimentoInput.addEventListener('change', calcularIdade);
        
        // Executa ao carregar a página caso já exista valor (útil na edição)
        if (dataNascimentoInput.value) {
            calcularIdade();
        }
    }

    // --- 3. Mostrar/ocultar campo de trabalho ---
    const trabalhoCheckbox = document.querySelector('input[name="trabalho_ficha_adulto"]');
    const nomeTrabalhoInput = document.getElementById('nome_trabalho_profissao');

    if (trabalhoCheckbox && nomeTrabalhoInput) {
        function toggleTrabalho() {
            // O campo de texto fica desabilitado se o checkbox não estiver marcado
            nomeTrabalhoInput.disabled = !trabalhoCheckbox.checked;
            if (!trabalhoCheckbox.checked) {
                nomeTrabalhoInput.value = '';
            }
        }
        trabalhoCheckbox.addEventListener('change', toggleTrabalho);
        toggleTrabalho(); // Estado inicial
    }
});