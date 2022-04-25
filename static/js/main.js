// Initializing document variables
var loading, error;

window.onload = () => {
    loading = document.getElementById('loading');
    error = document.getElementById('error');
    hideMessage('loading');
    hideMessage('error');
}

function login(event) {
    event.preventDefault();
    const options = {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target))
    }
    displayMessage('loading', '');
    fetch('/login', options)
        .then(response => response.json())
        .then(data => {
            if (data.success === false) {
                displayMessage('error', 'Invalid username and password compination');
            }
        })
        .catch(error => {
            console.log(error);
            displayMessage('error', 'Something went wrong, please try again');
        })
}

function signup(event) {
    event.preventDefault();
    const options = {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target))
    }
    displayMessage('loading','');
    //email_unavailable, username_unavailable, not_match
    fetch('/signup', options)
        .then(response => { 
            console.log(response) 
            window.location.reload()
        })
        .catch(error => {
            console.log(error)
            displayMessage('error', 'Something went wrong, please try again');
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

function displayMessage(msg, inner) {
    if (msg === 'error') {
        setTimeout(() => {
            error.style.display = 'none';
        }, 1000)
        loading.style.display = 'none';
        error.innerHTML = inner;
        error.style.display = 'block'
    } else {
        error.style.display = 'none';
        loading.style.display = 'block';
    }

}

function hideMessage(msg) {
    if (msg === 'error') {
        error.style.display = 'none';
    } else {
        loading.style.display = 'none';
    }
}