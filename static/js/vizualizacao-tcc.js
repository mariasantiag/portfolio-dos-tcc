// Codigo para proteger o site


document.addEventListener('contextmenu', function(e){
    e.preventDefault();
    Swal.fire({
        title: "Esta função foi desabilitada para proteger o conteúdo do site.",
        icon: "error",
        draggable: true
      });
})

document.addEventListener('keydown', function(e){
    if (e.ctrlKey && (e.key === 'c' || e.key==='u' || e.key === 's' || e.key === 'p')){
        e.preventDefault()
        Swal.fire({
            title: "Esta função foi desabilitada para proteger o conteúdo do site.",
            icon: "error",
            draggable: true
          });      
    }
    if (e.ctrlKey && (e.key === 'Insert')){
        navigator.clipboard.writeText('')
        e.preventDefault()
        Swal.fire({
            title: "Capturas de tela foram dasabilitadas",
            icon: "error",
            draggable: true
          });       
    }
    if (e.key === 'F12'){
        e.preventDefault() 
        Swal.fire({
            title: "Esta função foi desabilitada para proteger o conteúdo do site.",
            icon: "error",
            draggable: true
          });      
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



