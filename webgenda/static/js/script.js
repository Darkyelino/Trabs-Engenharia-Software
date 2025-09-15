document.addEventListener('DOMContentLoaded', function () {

    // LÓGICA DO MENU LATERAL
    const sidebar = document.getElementById('sidebar');
    const sidebarCollapseButton = document.getElementById('sidebarCollapse');
    if (sidebar && sidebarCollapseButton) {
        sidebarCollapseButton.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    const userDropdown = document.querySelector('.user-dropdown');
    if (userDropdown) {
        const trigger = userDropdown.querySelector('.user-trigger');
        const menu = userDropdown.querySelector('.dropdown-menu');
        if(trigger && menu) {
            trigger.addEventListener('click', function (event) {
                event.stopPropagation();
                menu.classList.toggle('show');
            });
        }
    }

    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        if (localStorage.getItem('theme') === 'dark') {
            themeToggle.classList.remove('bi-brightness-high-fill');
            themeToggle.classList.add('bi-moon-fill');
        }
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            let theme = 'light';
            if (document.body.classList.contains('dark-mode')) {
                theme = 'dark';
                this.classList.remove('bi-brightness-high-fill');
                this.classList.add('bi-moon-fill');
            } else {
                this.classList.remove('bi-moon-fill');
                this.classList.add('bi-brightness-high-fill');
            }
            localStorage.setItem('theme', theme);
        });
    }

    const filterIcons = document.querySelectorAll('.th-with-filter .filter-icon');
    filterIcons.forEach(icon => {
        const filterMenu = icon.closest('.th-with-filter').querySelector('.header-filter-menu');
        if (filterMenu) {
            icon.addEventListener('click', function (event) {
                event.stopPropagation();
                document.querySelectorAll('.header-filter-menu.show').forEach(openMenu => {
                    if (openMenu !== filterMenu) {
                        openMenu.classList.remove('show');
                    }
                });
                filterMenu.classList.toggle('show');
            });
        }
    });

    window.addEventListener('click', function () {
        const userMenu = document.querySelector('.user-dropdown .dropdown-menu.show');
        if (userMenu) {
            userMenu.classList.remove('show');
        }
        document.querySelectorAll('.header-filter-menu.show').forEach(openMenu => {
            openMenu.classList.remove('show');
        });
    });

    const alerts = document.querySelectorAll('.alert-success');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade-out');
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });

});

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

const togglePassword = document.querySelector('#togglePassword');
if (togglePassword) {
    const password = document.querySelector('#id_password');
    togglePassword.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('bi-eye');
        this.classList.toggle('bi-eye-slash');
    });
}