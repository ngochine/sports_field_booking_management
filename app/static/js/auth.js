function showAlert(container, message, category) {
    container.insertAdjacentHTML('beforeend', `
        <div class="alert alert-${category} m-3 alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `)
}

function handleMessages(container, data, type = "danger") {
    const messages = typeof data.message === "object"
        ? Object.values(data.message).flat()
        : [data.message]

    messages.forEach(m => showAlert(container, m, type))
}


function register() {
    const form = document.getElementById("registerForm")
    const container = document.getElementById("flash-container")

    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    const confirm = document.getElementById("confirm").value

    fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, confirm })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        container.innerHTML = ""
        showAlert(container, "Đăng ký thành công", "success")
        setTimeout(() => window.location.href = "/login", 2000)
    })
    .catch(err => {
        container.innerHTML = ""
        handleMessages(container, err)
    })
}


function login() {
    const form = document.getElementById("loginForm")
    const container = document.getElementById("flash-container")

    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify({ username, password })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        container.innerHTML = ""
        showAlert(container, "Đăng nhập thành công", "success")
        setTimeout(() => window.location.href = "/", 500)
    })
    .catch(err => {
        container.innerHTML = ""
        handleMessages(container, err)
    })
}


function logout() {
    fetch("/api/auth/logout", {
        method: "POST",
        credentials: "include"
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(() => {
        window.location.href = "/"
    })
    .catch(err => {
        container.innerHTML = ""
        handleMessages(container, err)
    })
}