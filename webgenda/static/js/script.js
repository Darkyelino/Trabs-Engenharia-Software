document.addEventListener('DOMContentLoaded', function () {

    // --- LÓGICA DO MENU LATERAL (SIDEBAR) ---
    const sidebar = document.getElementById('sidebar');
    const sidebarCollapseButton = document.getElementById('sidebarCollapse');
    if (sidebar && sidebarCollapseButton) {
        sidebarCollapseButton.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }

    // --- LÓGICA DO DROPDOWN DE USUÁRIO ---
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

    // --- LÓGICA DO MODO ESCURO (DARK MODE) ---
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

    // --- LÓGICA PARA O FILTRO NO CABEÇALHO DA TABELA ---
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

    // --- LÓGICA PARA FECHAMENTO DE MENUS (DROPDOWNS) AO CLICAR FORA ---
    window.addEventListener('click', function () {
        const userMenu = document.querySelector('.user-dropdown .dropdown-menu.show');
        if (userMenu) {
            userMenu.classList.remove('show');
        }
        document.querySelectorAll('.header-filter-menu.show').forEach(openMenu => {
            openMenu.classList.remove('show');
        });
    });

    // --- LÓGICA PARA FECHAMENTO AUTOMÁTICO DE ALERTAS DE SUCESSO ---
    const alerts = document.querySelectorAll('.alert-success');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade-out');
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });

    // --- LÓGICA DO CALENDÁRIO INTERATIVO ---
    const calendarContainer = document.querySelector('.calendar-container');
    // Só executa a lógica do calendário se o container dele existir na página atual
    if (calendarContainer) {
        const calendarTable = document.querySelector('.calendar-table');
        const modal = document.getElementById('details-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');
        const modalActions = document.getElementById('modal-actions');
        const closeButton = document.querySelector('.close-button');

        if (!calendarContainer.dataset.apiUrl || !calendarContainer.dataset.addEventUrlBase || !calendarContainer.dataset.deleteEventUrlBase || !calendarContainer.dataset.currentYear || !calendarContainer.dataset.currentMonth) {
            console.error("ERRO: Atributos 'data-' importantes faltando na div .calendar-container do HTML.");
            return;
        }

        const apiUrlBase = calendarContainer.dataset.apiUrl.replace('/0/0/0/', '');
        const addEventUrlBase = calendarContainer.dataset.addEventUrlBase.replace('/0/0/0/', '');
        const deleteEventUrlBase = calendarContainer.dataset.deleteEventUrlBase.replace('/0/', '');
        const ano = calendarContainer.dataset.currentYear;
        const mes = calendarContainer.dataset.currentMonth;

        if (calendarTable) {
            calendarTable.addEventListener('click', function(event) {
                const target = event.target;
                const isClickableDay = target.tagName === 'TD' && target.classList.contains('day');
                if (isClickableDay) {
                    const dia = target.textContent;
                    const apiUrl = `${apiUrlBase}/${ano}/${mes}/${dia}/`;
                    fetch(apiUrl)
                        .then(response => {
                            if (!response.ok) { throw new Error('Erro na rede ou na API: ' + response.statusText); }
                            return response.json();
                        })
                        .then(data => {
                            modalTitle.textContent = `Compromissos para ${dia}/${mes}/${ano}`;
                            let contentHtml = '';
                            if (data.eventos && data.eventos.length > 0) {
                                contentHtml += '<h3>Eventos</h3><ul>';
                                data.eventos.forEach(evento => {
                                    const deleteUrl = deleteEventUrlBase + evento.id + '/';
                                    contentHtml += `<li><div class="modal-item-header"><div><strong>${evento.titulo}</strong> <span class="event-time">${evento.hora}</span></div><a href="${deleteUrl}" class="delete-link">&times;</a></div><p>${evento.descricao || ''}</p>${evento.atividade ? `<p class="related-activity"><strong>Atividade:</strong> ${evento.atividade}</p>` : ''}</li>`;
                                });
                                contentHtml += '</ul>';
                            }
                            if (data.atividades && data.atividades.length > 0) { /* ... lógica para atividades ... */ }
                            if (contentHtml === '') { contentHtml = '<p>Nenhum compromisso para este dia.</p>'; }
                            modalBody.innerHTML = contentHtml;
                            const addEventUrl = `${addEventUrlBase}/${ano}/${mes}/${dia}/`;
                            modalActions.innerHTML = `<a href="${addEventUrl}" class="btn-primary">Adicionar Evento para este dia</a>`;
                            modal.style.display = 'block';
                        })
                        .catch(error => {
                            console.error("Falha ao buscar dados da API:", error);
                            alert("Não foi possível buscar os detalhes para este dia. Verifique o console para mais informações.");
                        });
                }
            });
        }
        if(closeButton) { closeButton.onclick = function() { modal.style.display = "none"; } }
        window.addEventListener('click', function(event) { if (event.target == modal) { modal.style.display = "none"; } });
    }

}); 


// --- FUNÇÕES GLOBAIS  ---

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