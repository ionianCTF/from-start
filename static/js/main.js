// Initializing document variables
var loading, error;
const username_regex = new RegExp('^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$');

window.onload = () => {
    loading = document.getElementById('loading');
    error = document.getElementById('error');
    hideMessage('loading');
    hideMessage('error');

    // Check for server error
    const options = {
        method: 'GET'
    }
    fetch('/')
        .then(response => {
            if (response === null) {
                alert('error')
            }
            response.json();
        })
        .then(data => {
            if (data === '') {
                displayMessage('error', 'Something went wrong, please try again')
            }
        })
        .catch(error => {
            console.log(error);
            displayMessage('error', 'Something went wrong, please try again');
        })
}

function login(event) {
    // Validate user input
    //if (event.target.username.value)

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
            } else if (data.success === true) {
                window.location.reload()
            }
        })
        .catch(error => {
            console.log(error);
            displayMessage('error', 'Something went wrong, please try again');
        })
}

function signup(event) {
    event.preventDefault();
    // Validate user input
    if (!username_regex.test(event.target.username.value)) {
        displayMessage('error', 'Username not available')
        return 0;
    } else if (event.target.password.value != event.target.password_confirmation.value) {
        displayMessage('error', 'Passwords don\'t match')
        return 0;
    }
    const options = {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target))
    }
    displayMessage('loading','');
    //email_unavailable, username_unavailable, not_match
    fetch('/signup', options)
        .then(response => response.json())
        .then(data => { 
            if (data.status === 'email_unavailabe') {
                displayMessage('error', 'Email already in use');
            } else if (data.status === 'username_unavailable') {
                displayMessage('error', 'Username already in use');
            } else if (data.status === 'not_match') {
                displayMessage('error', 'Passwords don\'t match');
            } else if (data.status === 'success') {
                window.location.reload();
            }
        })
        .catch(error => {
            console.log(error);
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
        }, 2000)
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