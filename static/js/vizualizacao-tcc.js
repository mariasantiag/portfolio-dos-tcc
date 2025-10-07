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
}, false); //


// Codigo para exibir o TCC
const pdfUrl = '../pdf/Proteção de PDF.pdf'

pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js`;

const loadingTask = pdfjsLib.getDocument(pdfUrl)
const pdfViewer = document.getElementById('tcc-renderer')

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
},
function(reason){
    console.error('Erro ao carregar o PDF', reason)
}
) // 


