/// Função para preencher o <select> de orientadores conforme o curso selecionado
function popularOrientadoresEmSelect(select, data = []) {
  // Limpa as opções antigas
  select.innerHTML = '<option selected disabled>Selecione o orientador</option>';

  /// Se já existe uma lista de orientadores, adiciona direto
  if (data.length > 0) {
      data.forEach(orientador => {
          const option = document.createElement("option");
          option.value = orientador.id;
          option.textContent = orientador.nome_orientador;
          select.appendChild(option);
      });
      return;
  }
 
  // Se não tem dados, busca o valor do <select name="curso">
  const selectCurso = document.querySelector("select[name='curso']");
  const cursoSelecionado = selectCurso ? selectCurso.value : null;

  // Verifica se um curso válido está selecionado
  if (!cursoSelecionado || selectCurso.options[selectCurso.selectedIndex].disabled) {
      // Se nenhum curso foi escolhido, sai da função
       return;
  }
 
  // Faz o fetch (busca os orientadores do curso no servidor) 
  fetch(`/api/orientadores/${cursoSelecionado}`)
      .then(response => response.json())
      .then(data => {
          // Adiciona cada orientador como uma opção no select
          data.forEach(orientador => {
              const option = document.createElement("option");
              option.value = orientador.cod_orientador;
              option.textContent = orientador.nome_orientador;
              select.appendChild(option);
          });
      })
      .catch(error => {
          console.error("Erro ao buscar orientadores:", error);
      });
}

// Quando a página carregar
document.addEventListener("DOMContentLoaded", function () {
  // Referência ao <select> de curso
  const selectCurso = document.querySelector("select[name='curso']");

  // Quando o curso for trocado, atualiza todos os selects de orientador
  selectCurso.addEventListener("change", function () {
      const selectsOrientadores = document.querySelectorAll('#orientadores-container .orientador-select');
     
      selectsOrientadores.forEach(selectOrientador => {
          popularOrientadoresEmSelect(selectOrientador);
      });
  });
});

// Adiciona um novo campo de orientador
function adicionarCampoOrientador() {
  const container = document.getElementById('orientadores-container');

  const novoCampo = document.createElement('div');
  novoCampo.className = 'orientador-input mb-2 d-flex align-items-center';

  novoCampo.innerHTML = `
      <select name="orientador[]" class="form-select orientador-select me-2" required>
        <option selected disabled>Selecione o orientador</option>
      </select>
      <button type="button" class="btn btn-danger btn-sm" onclick="removerCampo(this)">Remover</button>
  `;

  container.appendChild(novoCampo);

  // Preenche o novo campo com os orientadores do curso atual
  popularOrientadoresEmSelect(novoCampo.querySelector('select'));
}

// Remove o campo de orientador
function removerCampo(botao) {
  botao.parentElement.remove();
}
