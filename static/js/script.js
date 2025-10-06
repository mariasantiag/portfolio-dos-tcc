
// Espera o carregamento completo da estrutura HTML da página (DOM) antes de executar a função que está dentro dele.
document.addEventListener("DOMContentLoaded", function () {

// função para colocar op Sweet Alert2 do "deleter" 
    const botaoExcluir = document.getElementById("btn__excluir");
  
    botaoExcluir.addEventListener("click", function (e) {
      e.preventDefault(); // evita que o link recarregue a página
  
      Swal.fire({
        title: "Tem certeza que deseja excluir esse TCC?",
        text: "Você não poderá reverter isso!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim, deletar!"
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "Deletado!",
            text: "Seu item foi deletado com sucesso.",
            icon: "success"
          });
        }
      });
    });
  });
  