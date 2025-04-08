// Você pode adicionar lógica para redirecionar com os botões no futuro
document.querySelectorAll(".atividade-btn").forEach((btn, index) => {
    btn.addEventListener("click", () => {
        alert(`Clicou no botão: ${btn.textContent}`);
        // Em breve: window.location.href = '/url_para_o_tipo_especifico/';
    });
});
