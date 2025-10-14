// Função chamada quando o botão "Adicionar Orientador" é clicado
function adicionarCampo() {
    // Seleciona o container onde os campos de orientador serão adicionados
    const container = document.getElementById('orientadores-container');

    // Cria um novo elemento <div> que vai conter o novo campo de orientador e o botão de remover
    const novoCampo = document.createElement('div');

    // Adiciona classes CSS para espaçamento e layout
    novoCampo.className = 'orientador-input mb-2 d-flex align-items-center';

    // Define o conteúdo HTML do novo campo (um input + botão de remover)
    novoCampo.innerHTML = `
      <input type="text" class="form-control me-2" name="orientador_nome" placeholder="Nome do Orientador" required>
      <button type="button" class="btn btn-danger btn-sm" onclick="removerCampo(this)">Remover</button>
    `;

    // Adiciona o novo campo ao container principal
    container.appendChild(novoCampo);
  }

  // Função para remover um campo de orientador
  // Recebe como argumento o botão "Remover" que foi clicado
  function removerCampo(botao) {
    // Remove o <div> pai do botão, ou seja, o campo inteiro de orientador
    botao.parentElement.remove();
  }