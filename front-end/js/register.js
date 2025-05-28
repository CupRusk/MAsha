document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });
        if (password.length < 8) {
            throw new Error("Пароль должен содержать не менее 8 символов");
        }
        if (!username || !password) {
            throw new Error("Пожалуйста, заполните все поля");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Ошибка регистрации");
        }

        alert(data.message);
        window.location.href = "/front-end/html/main.html";
    } catch (error) {
        if (errorMsg) errorMsg.textContent = error.message;
    }
});


function togglePasswordVisibility() {
    const passwordInput = document.getElementById("password");
    const toggleButton = document.getElementById("togglePassword");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.textContent = "Скрыть пароль";
    } else {
        passwordInput.type = "password";
        toggleButton.textContent = "Показать пароль";
    }
}