document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const sidebarCollapseButton = document.getElementById('sidebarCollapse');

    if (sidebar && sidebarCollapseButton) {
        sidebarCollapseButton.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    }
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

document.addEventListener('DOMContentLoaded', function() {
    console.log("Script da agenda carregado!");

    const calendarTable = document.querySelector('.calendar-table');
    const modal = document.getElementById('details-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const modalActions = document.getElementById('modal-actions');
    const closeButton = document.querySelector('.close-button');
    const calendarContainer = document.querySelector('.calendar-container');

    if (!calendarContainer || !calendarContainer.dataset.apiUrl || !calendarContainer.dataset.addEventUrlBase || !calendarContainer.dataset.deleteEventUrlBase || !calendarContainer.dataset.currentYear || !calendarContainer.dataset.currentMonth) {
        console.error("ERRO: Atributos 'data-' importantes faltando na div .calendar-container do HTML. A interatividade não funcionará.");
        return;
    }

    const apiUrlBase = calendarContainer.dataset.apiUrl.replace('/0/0/0/', '');
    const addEventUrlBase = calendarContainer.dataset.addEventUrlBase.replace('/0/0/0/', '');
    const deleteEventUrlBase = calendarContainer.dataset.deleteEventUrlBase.replace('0/', '');
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
                                contentHtml += `<li><div class="modal-item-header"><div><strong>${evento.titulo}</strong> <span class="event-time">${evento.hora}</span></div><a href="${deleteUrl}" class="delete-link">&times;</a></div><p>${evento.descricao}</p></li>`;
                            });
                            contentHtml += '</ul>';
                        }
                        
                        if (data.atividades && data.atividades.length > 0) {
                            contentHtml += '<h3>Atividades</h3><ul>';
                            data.atividades.forEach(atividade => {
                                contentHtml += `<li><strong>${atividade.titulo}</strong> (${atividade.tipo})</li>`;
                            });
                            contentHtml += '</ul>';
                        }

                        if(contentHtml === '') {
                            contentHtml = '<p>Nenhum compromisso para este dia.</p>';
                        }

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
    if(closeButton) { 
        closeButton.onclick = function() { 
            modal.style.display = "none"; 
        } 
    }
    window.onclick = function(event) { 
        if (event.target == modal) { 
            modal.style.display = "none"; 
        } 
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const userDropdown = document.querySelector('.user-dropdown');

    if (userDropdown) {
        const trigger = userDropdown.querySelector('.user-trigger');
        const menu = userDropdown.querySelector('.dropdown-menu');

        trigger.addEventListener('click', function (event) {
            event.stopPropagation(); 
            menu.classList.toggle('show');
        });

        window.addEventListener('click', function (event) {
            if (menu.classList.contains('show')) {
                menu.classList.remove('show');
            }
        });
    }
});

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#id_password');

togglePassword.addEventListener('click', function (e) {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('bi-eye');
    this.classList.toggle('bi-eye-slash');
});

document.addEventListener('DOMContentLoaded', function () {
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

// funções para modo escuro
document.addEventListener('DOMContentLoaded', function () {
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
                themeToggle.classList.remove('bi-brightness-high-fill');
                themeToggle.classList.add('bi-moon-fill');
            } else {
                themeToggle.classList.remove('bi-moon-fill');
                themeToggle.classList.add('bi-brightness-high-fill');
            }
            localStorage.setItem('theme', theme);
        });
    }
});