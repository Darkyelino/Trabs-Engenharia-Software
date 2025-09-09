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
    const closeButton = document.querySelector('.close-button');
    const calendarHeader = document.querySelector('.calendar-header h2');
    const calendarContainer = document.querySelector('.calendar-container');

    if (!calendarContainer || !calendarContainer.dataset.apiUrl) {
        console.error("ERRO: O atributo 'data-api-url' não foi encontrado na div .calendar-container do HTML. A interatividade não funcionará.");
        return;
    }

    const apiUrlBase = calendarContainer.dataset.apiUrl.replace('/0/0/0/', '');

    const [mesNome, ano] = calendarHeader.textContent.trim().split(' ');
    const meses = {'Janeiro':1, 'Fevereiro':2, 'Março':3, 'Abril':4, 'Maio':5, 'Junho':6, 'Julho':7, 'Agosto':8, 'Setembro':9, 'Outubro':10, 'Novembro':11, 'Dezembro':12};
    const mes = meses[mesNome];

    if (calendarTable) {
        calendarTable.addEventListener('click', function(event) {
            const target = event.target;

            // --- LÓGICA DO CLIQUE ---
            // Esta é a verificação crucial. Se as classes CSS no HTML não baterem com estas, nada acontece.
            const isClickableDay = target.tagName === 'TD' && target.classList.contains('day') && (
                target.classList.contains('with-event') ||
                target.classList.contains('with-activity-start') ||
                target.classList.contains('with-activity-middle') ||
                target.classList.contains('with-activity-end')
            );

            if (isClickableDay) {
                const dia = target.textContent;
                console.log(`Dia clicado: ${dia}/${mes}/${ano}`);

                const apiUrl = `${apiUrlBase}/${ano}/${mes}/${dia}/`;
                console.log("Chamando API:", apiUrl);

                fetch(apiUrl)
                    .then(response => {
                        if (!response.ok) { throw new Error('Erro na rede ou na API: ' + response.statusText); }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Dados recebidos da API:", data);

                        modalTitle.textContent = `Compromissos para ${dia}/${mes}/${ano}`;
                        
                        let contentHtml = '';
                        if (data.eventos && data.eventos.length > 0) {
                            contentHtml += '<h3>Eventos</h3><ul>';
                            data.eventos.forEach(evento => {
                                contentHtml += `<li><strong>${evento.titulo}</strong><p>${evento.descricao}</p></li>`;
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
                        modal.style.display = 'block';
                    })
                    .catch(error => {
                        console.error("Falha ao buscar dados da API:", error);
                        alert("Não foi possível buscar os detalhes para este dia. Verifique o console para mais informações.");
                    });
            }
        });
    }

    // Lógica para fechar o modal
    if(closeButton) { closeButton.onclick = function() { modal.style.display = "none"; } }
    window.onclick = function(event) { if (event.target == modal) { modal.style.display = "none"; } }
});