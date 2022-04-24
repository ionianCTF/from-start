window.onload = () => {
}

function login(event) {
    event.preventDefault();
    const options = {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target))
    }
    fetch('/login', options)
        .then(response => response.json())
        .then(data => {
            if (data.success === true) {
                window.location.reload()
            } else {
                alert('smth')
            }    
        })
        .catch(error => {
            console.log(error)
        })
}

function signup(event) {
    event.preventDefault();
    const options = {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target))
    }
    fetch('/signup', options)
        .then(response => { 
            console.log(serverData)
            console.log(response) 
            window.location.reload()
        })
        .catch(error => {
            console.log(error)
        })
}


function change(event) {
    event.preventDefault();
    const options = {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target))
    }
    fetch('/settings', options)
        .then((response) => { 
                console.log(response) 
                window.location.reload()
            }
        )
        .catch(error => {
            console.log(error)
        })
}