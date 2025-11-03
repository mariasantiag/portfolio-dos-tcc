document.addEventListener('DOMContentLoaded', () => {
    const cursoSelect = document.getElementById('curso-delete');
    const orientadorSelect = document.getElementById('orientador-delete');

    if (cursoSelect) {
        cursoSelect.addEventListener('change', async () => {
            const cod_curso = cursoSelect.value;
            
            // Limpa as opções atuais
            orientadorSelect.innerHTML = '<option selected disabled>Carregando...</option>';

            if (!cod_curso) {
                orientadorSelect.innerHTML = '<option selected disabled>Selecione o curso primeiro</option>';
                return;
            }

            try {
                // Busca orientadores da API que você já criou
                const response = await fetch(`/api/orientadores/${cod_curso}`);
                if (!response.ok) {
                    throw new Error('Erro ao buscar orientadores');
                }
                const orientadores = await response.json();

                // Popula o dropdown de orientadores
                orientadorSelect.innerHTML = '<option value="" selected>Selecione o orientador (ou deixe em branco para excluir o curso)</option>';
                
                if (orientadores.length === 0) {
                    orientadorSelect.innerHTML = '<option selected disabled>Nenhum orientador encontrado</option>';
                } else {
                    orientadores.forEach(orientador => {
                        const option = document.createElement('option');
                        // A API retorna 'cod_orientador' e 'nome_orientador'
                        option.value = orientador.cod_orientador; 
                        option.textContent = orientador.nome_orientador;
                        orientadorSelect.appendChild(option);
                    });
                }
            } catch (error) {
                console.error('Erro:', error);
                orientadorSelect.innerHTML = '<option selected disabled>Erro ao carregar</option>';
            }
        });
    }
});