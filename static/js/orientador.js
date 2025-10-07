// Espera até que toda a página esteja carregada
document.addEventListener("DOMContentLoaded", function () {

    // Referência ao <select> de curso
    const selectCurso = document.querySelector("select[name='curso']");

    // Referência ao <select> de orientador
    const selectOrientador = document.getElementById("select-orientador");

    // Quando o curso for alterado...
    selectCurso.addEventListener("change", function () {
      const cursoSelecionado = this.value; // pega o código do curso

      // Verifica se foi selecionado um curso válido
      if (cursoSelecionado) {
        // Faz uma requisição GET para a API Flask usando o código do curso
        fetch(`/api/orientadores/${cursoSelecionado}`)
          .then(response => response.json()) // converte a resposta para JSON
          .then(data => {
            // Limpa o <select> de orientadores antes de adicionar os novos
            selectOrientador.innerHTML = '<option selected disabled>Selecione o orientador</option>';

            // Para cada orientador retornado pela API...
            data.forEach(function (orientador) {
              // Cria uma nova <option> com nome do orientador
              const option = document.createElement("option");
              option.value = orientador.nome_orientador; // valor do campo
              option.textContent = orientador.nome_orientador; // texto exibido
              selectOrientador.appendChild(option); // adiciona a opção ao <select>
            });
          })
          .catch(error => {
            // Em caso de erro, exibe no console
            console.error("Erro ao buscar orientadores:", error);
          });
      }
    });
  });

