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


function loginBase(event, container) {
    event.preventDefault()
    
    const form = document.getElementById("loginForm")

    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    return fetch("/api/auth/login", {
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
    .catch(err => {
        console.log(err)
        container.innerHTML = ""
        handleMessages(container, err)
    })
}


function login(event){
    const container = document.getElementById("flash-container")
    loginBase(event, container).then(data =>
    {
        container.innerHTML = ""
        showAlert(container, "Đăng nhập thành công", "success")
        setTimeout(() => window.location.href = "/", 500)
    })
}

function loginAdmin(event){
    const container = document.getElementById("flash-container")
    loginBase(event, container).then(data =>
    {
        container.innerHTML = ""
        showAlert(container, "Đăng nhập thành công", "success")
        setTimeout(() => window.location.href = "/admin", 500)
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


function updateInfoUser(event) {

    event.preventDefault()
    const form = document.getElementById("updateProfileForm")

    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    const container =document.getElementById("flash-container")
    const email =document.getElementById("email").value
    const phone =document.getElementById("phone").value
    const firstName =document.getElementById("firstName").value
    const lastName =document.getElementById("lastName").value

    const avatarFile =document.getElementById("avatarInput").files[0]
    const formData = new FormData()

    formData.append("email", email)
    formData.append("phone", phone)
    formData.append("first_name", firstName)
    formData.append("last_name", lastName)

    if (avatarFile) {
        formData.append("avatar", avatarFile)
    }
    console.log(avatarFile)
    console.log(formData)
    fetch("/api/auth/current-user/profile", {
        method: "PATCH",
        credentials: "include",
        body: formData
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(data => {
        container.innerHTML = ""
        showAlert(container, "Cập nhật thông tin thành công", "success")
        setTimeout(() => {window.location.reload()}, 500)
    })
    .catch(err => {
        console.log(err)
        container.innerHTML = ""
        handleMessages(container, err)
    })
}


function changePassword(event){
    event.preventDefault()

    const currentPassword = document.getElementById("currentPassword").value
    const newPassword = document.getElementById("newPassword").value
    const confirmPassword = document.getElementById("confirmPassword").value

    if (newPassword !== confirmPassword) {
        alert("Xác nhận mật khẩu không khớp");
        return;
    }
    
    fetch("/api/auth/current-user/change-password", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ 
            "current_password": currentPassword,
            "new_password": newPassword,
            "confirm_password": confirmPassword
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err })
        }
        return res.json()
    })
    .then(async (data) => {

        alert(
            "Đổi mật khẩu thành công, vui lòng đăng nhập lại"
        )

        await fetch("/api/auth/logout", {
            method: "POST",
            credentials: "include"
        })

        window.location.href = "/login"
    })
    .catch(err => {
        console.log(err)
        let messages = []
        if (typeof err.message === "object") {
            Object.values(err.message)
                .forEach(msgArr => {
                    if (Array.isArray(msgArr)) {
                        messages.push(...msgArr)
                    } else {
                        messages.push(msgArr)
                    }
                })
        } else {
            messages.push(
                err.message || "Có lỗi xảy ra"
            )
        }
        alert(messages.join("\n"))
    })
}


function togglePassword(inputId, button) {
    const input =document.getElementById(inputId)
    const icon =button.querySelector("i")

    if (input.type === "password") {
        input.type = "text"
        icon.classList.remove("fa-eye")
        icon.classList.add("fa-eye-slash")
    } 
    else {
        input.type = "password"
        icon.classList.remove("fa-eye-slash")
        icon.classList.add("fa-eye")
    }
}