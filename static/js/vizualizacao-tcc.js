// Codigo para proteger o site


document.addEventListener('contextmenu', function(e){
    e.preventDefault();
    alert('Esta função foi desabilitada para proteger o conteudo do site.')
})

document.addEventListener('keydown', function(e){
    if (e.ctrlKey && (e.key === 'c' || e.key==='u' || e.key === 's' || e.key === 'p')){
        e.preventDefault()
        alert('Esta função foi desabilitada para proteger o conteúdo do site.')
    }
    if (e.ctrlKey && (e.key === 'Insert')){
        navigator.clipboard.writeText('')
        e.preventDefault()
        alert('Capturas de tela foram dasabilitadas')       
    }
    if (e.key === 'F12'){
        e.preventDefault()
        alert('Esta função foi desabilitada para proteger o conteúdo do site.')       
    }
    
}, false); //




pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js`;

const pdfViewer = document.querySelector('.tcc-renderer')


function viewpdf(pdfUrl){

    let loadingTask = pdfjsLib.getDocument(pdfUrl)
    
    loadingTask.promise.then(function(pdf){
        console.log('TCC carregado com sucesso!')
            
            for(let pageNum = 1; pageNum<=pdf.numPages; pageNum++){
                pdf.getPage(pageNum).then(function(page){
                    const scale=1.5;
                    const viewport = page.getViewport({scale:scale})
                    
                    const canvas = document.createElement('canvas')
                    const context = canvas.getContext('2d')
                    canvas.height = viewport.height
                    canvas.width = viewport.width
                    
                    pdfViewer.appendChild(canvas)
                    
                    const renderContext= {
                        canvasContext: context,
                        viewport:viewport
                    }
                    page.render(renderContext)
                })
                
            }
        }
        ) 

        tccContainer.style.display = 'block';
        btnclose.style.display = 'block'
        tccContainer.classList.add('is-viewing')
        
        
    
}

function closepdf(buttonclose,elementoPDF){
    
    buttonclose.addEventListener('click', () => {
        elementoPDF.style.display = 'none'
        buttonclose.style.display = 'none'
        tccContainer.classList.remove('is-viewing')
        
        pdfViewer.innerHTML = '';
    })


 

}

const btnclose = document.querySelector(".btn-close")
const tccContainer = document.querySelector('.tcc_view');

closepdf(btnclose,tccContainer) 

viewpdf(btnclose,tccContainer) ;



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