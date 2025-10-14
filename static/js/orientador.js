// ATUALIZAÇÃO DA FUNÇÃO popularOrientadoresEmSelect (Mantém a que eu te passei na última resposta, mas garante o retorno)
function popularOrientadoresEmSelect(select, data = []) {
  // Limpa as opções antigas
  select.innerHTML = '<option selected disabled>Selecione o orientador</option>';

  // Se já temos os dados, popula diretamente (não é o caso do botão Adicionar)
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
       // Não faz nada se for a opção "Selecione o curso"
       return;
  }
 
  // Faz o fetch (busca)
  fetch(`/api/orientadores/${cursoSelecionado}`)
      .then(response => response.json())
      .then(data => {
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

// NOVO CÓDIGO DO DOMContentLoaded
document.addEventListener("DOMContentLoaded", function () {
  // Referência ao <select> de curso
  const selectCurso = document.querySelector("select[name='curso']");

  // Quando o curso for alterado...
  selectCurso.addEventListener("change", function () {
      // Encontra TODOS os selects de orientador (o inicial e os adicionados)
      const selectsOrientadores = document.querySelectorAll('#orientadores-container .orientador-select');
     
      selectsOrientadores.forEach(selectOrientador => {
          // Repopula cada um com os orientadores do novo curso
          popularOrientadoresEmSelect(selectOrientador);
      });
  });
});

// A função adicionarCampoOrientador() deve permanecer como estava (e como está abaixo)
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

  // Atualiza a lista de opções com base no curso selecionado
  // ESSA CHAMADA GARANTE QUE O NOVO CAMPO SEJA POPULADO IMEDIATAMENTE!
  popularOrientadoresEmSelect(novoCampo.querySelector('select'));
}

// Remove o campo
function removerCampo(botao) {
  botao.parentElement.remove();
}
