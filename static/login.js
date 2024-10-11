const users = [
    {
        email: "user@gmail.com",
        password: "123",
    },
];

document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const validUser = users.find(user => user.email === email && user.password === password);

    if (validUser) {
        window.location.href = 'index.html';
    } else {
        document.getElementById('error-msg').innerText = 'Email ou senha inválidos!';
    }
});


const menuBtn = document.querySelector('.menu-btn');
const sideMenu = document.getElementById('side-menu');

menuBtn.addEventListener('click', () => {
    sideMenu.classList.toggle('open');
});


document.getElementById('logout').addEventListener('click', function () {
    localStorage.removeItem('userLoggedIn');
    window.location.href = 'login.html';
});

