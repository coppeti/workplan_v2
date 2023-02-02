;(function(){
    const modal = new bootstrap.Modal(document.getElementById('addMemberModal'))

    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === 'addMemberDialog'){
            modal.show()
        }
    })

    htmx.on('htmx:beforeSwap', (e) => {
        if (e.detail.target.id === 'addMemberDialog' && !e.detail.xhr.response){
            modal.hide()
            e.detail.shouldSwap = false
        }
    })

    htmx.on('hidden.bs.modal', (e) => {
        document.getElementById('addMemberDialog').innerHTML = ''
    })
})()