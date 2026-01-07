// Scripts para o sistema de cadastro de alunos

document.addEventListener('DOMContentLoaded', function() {
    // Preview da foto
    const fotoInput = document.getElementById('foto');
    const fotoPreview = document.getElementById('fotoPreview');
    const semFoto = document.getElementById('semFoto');

    if (fotoInput && fotoPreview && semFoto) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    fotoPreview.src = e.target.result;
                    fotoPreview.classList.remove('d-none');
                    semFoto.classList.add('d-none');
                }
                reader.readAsDataURL(file);
            } else {
                fotoPreview.classList.add('d-none');
                semFoto.classList.remove('d-none');
            }
        });
    }

    // Calcular idade automaticamente
    const dataNascimento = document.getElementById('data_nascimento');
    const idadePreview = document.getElementById('idade_preview');

    if (dataNascimento && idadePreview) {
        dataNascimento.addEventListener('change', function() {
            const data = new Date(this.value);
            if (!isNaN(data.getTime())) {
                const hoje = new Date();
                let idade = hoje.getFullYear() - data.getFullYear();
                const mes = hoje.getMonth() - data.getMonth();

                if (mes < 0 || (mes === 0 && hoje.getDate() < data.getDate())) {
                    idade--;
                }

                idadePreview.textContent = idade + ' anos';
                idadePreview.className = 'badge bg-success';
            }
        });

        // Calcular idade inicial se já houver valor
        if (dataNascimento.value) {
            dataNascimento.dispatchEvent(new Event('change'));
        }
    }

    // Mostrar/ocultar campo de trabalho
    const trabalhoCheckbox = document.querySelector('input[name="trabalho_ficha_adulto"]');
    const campoTrabalho = document.getElementById('campoTrabalho');

    if (trabalhoCheckbox && campoTrabalho) {
        function toggleTrabalho() {
            if (trabalhoCheckbox.checked) {
                campoTrabalho.style.display = 'block';
            } else {
                campoTrabalho.style.display = 'none';
                document.getElementById('nome_trabalho_profissao').value = '';
            }
        }

        trabalhoCheckbox.addEventListener('change', toggleTrabalho);
        toggleTrabalho(); // Estado inicial
    }

    // Formatação de moeda
    const rendaInput = document.getElementById('renda_familiar');
    if (rendaInput) {
        rendaInput.addEventListener('blur', function() {
            let value = parseFloat(this.value.replace(',', '.'));
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });

        rendaInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9.,]/g, '');
        });
    }

    // Validação de números
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < this.min) {
                this.value = this.min;
            }
            if (this.value > this.max) {
                this.value = this.max;
            }
        });
    });

    // Confirmação para exclusão
    const deleteForms = document.querySelectorAll('form[action*="/excluir/"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Tem certeza que deseja excluir este aluno? Esta ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });

    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Animações de entrada
    const cards = document.querySelectorAll('.card, .stat-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
});
