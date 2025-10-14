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
        navigator.clipboard.writeText('')
        e.preventDefault()
        alert('Esta função foi desabilitada para proteger o conteúdo do site.')       
    }

}, false); //


// Codigo para exibir o TCC
const pdfUrl = 'http://127.0.0.1:5000/static/pdf/Revisão Modernismo 3 fase e Concretismo.pdf'

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
}
) 

function viewpdf(buttonclose,elementoPDF){
    const button = document.getElementById("btn-view-tcc");

    button.addEventListener("click", () => {
        elementoPDF.style.display = 'block';
        buttonclose.style.display = 'block'
        tccContainer.classList.add('is-viewing')
    });
    
}

function closepdf(buttonclose,elementoPDF){
    buttonclose.addEventListener("click", () => {
        elementoPDF.style.display = 'none'
        buttonclose.style.display = 'none'
        tccContainer.classList.remove('is-viewing');
    })
    
}

const pdfFrame = document.getElementById("tcc-viewer-container");
const btnclose = document.getElementById("btn_close")
const tccContainer = document.querySelector('.tcc_view');

closepdf(btnclose,pdfFrame)

viewpdf(btnclose,pdfFrame);



