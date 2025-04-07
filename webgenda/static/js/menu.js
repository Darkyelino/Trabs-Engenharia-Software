document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggle-menu');
    const sidebar = document.getElementById('sidebar');

    toggleButton.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
    });
});
