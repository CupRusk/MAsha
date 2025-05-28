// Привет, начинаем!
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Ошибка входа");
        }

        const data = await response.json();
        alert(data.message); 
        window.location.href = "/front-end/html/main.html"; // Перенаправление на главную страницу
    } catch (error) {
        errorMsg.textContent = error.message;
    }
});