/**
 * Exibe um SweetAlert para confirmar a exclusão de um TCC.
 * @param {number} tccCodigo - O código (ID) do TCC a ser excluído.
 */
function confirmarExclusao(tccCodigo) {
    Swal.fire({
        title: "Tem certeza?",
        text: "Você não poderá reverter esta ação!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim, excluir!",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        // Se o usuário clicar em "Sim, excluir!"
        if (result.isConfirmed) {
            // Monta a URL de exclusão
            const urlExclusao = `/apagartcc/${tccCodigo}`;
            
            // Exibe o alerta de sucesso e redireciona (opcional, você pode redirecionar direto)
            Swal.fire({
                title: "Excluído!",
                text: "O TCC será excluído. Redirecionando...",
                icon: "success",
                showConfirmButton: false, // Não mostra o botão para redirecionar mais rápido
                timer: 1500 // Tempo para o alerta de sucesso aparecer
            }).then(() => {
                 // Redireciona para a rota Flask que deleta o TCC no banco
                 window.location.href = urlExclusao;
            });
        }
    });
}

