document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('access_token');
    if (token) {
        window.location.href = '/todolist';
    }
});

document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const data = {
        email: email,
        password: password
    };

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(errorResponse.error || 'Erro ao fazer login');
        }

        const result = await response.json();
        localStorage.setItem('access_token', result.access_token);

        window.location.href = '/todolist';
    } catch (error) {
        document.getElementById('error-msg').innerText = error.message;
    }
});
