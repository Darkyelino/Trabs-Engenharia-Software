document.addEventListener("DOMContentLoaded", () => {
    // Todas as suas variáveis aqui
    const corpoCalendario = document.getElementById("corpo-calendario");
    const anoSeletor = document.getElementById("ano-seletor");
    const botaoAnterior = document.getElementById("mes-anterior");
    const botaoProximo = document.getElementById("mes-proximo");
    const mesAtualTexto = document.getElementById("mes-atual");

    let dataAtual = new Date();
    let mesAtual = dataAtual.getMonth();
    let anoAtual = dataAtual.getFullYear();

    const nomesMeses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];

    function preencherAnos() {
        let anoInicio = anoAtual - 10;
        let anoFim = anoAtual + 50;
        for (let ano = anoInicio; ano <= anoFim; ano++) {
            let opcao = document.createElement("option");
            opcao.value = ano;
            opcao.textContent = ano;
            if (ano === anoAtual) opcao.selected = true;
            anoSeletor.appendChild(opcao);
        }
    }

    function gerarCalendario(mes, ano) {
        corpoCalendario.innerHTML = ""; // Limpar o calendário existente
        mesAtualTexto.textContent = `${nomesMeses[mes]} de ${ano}`;

        let primeiroDia = new Date(ano, mes, 1).getDay();
        let ultimoDia = new Date(ano, mes + 1, 0).getDate();

        let linha = document.createElement("tr");
        // Preenche os dias em branco antes do primeiro dia do mês
        for (let i = 0; i < primeiroDia; i++) {
            linha.appendChild(document.createElement("td"));
        }

        // Preenche os dias do mês
        for (let dia = 1; dia <= ultimoDia; dia++) {
            let celula = document.createElement("td");
            celula.textContent = dia;
            celula.classList.add("dia");
            const diaFormatado = String(dia).padStart(2, '0');
            const mesFormatado = String(mes + 1).padStart(2, '0');
            celula.dataset.date = `${ano}-${mesFormatado}-${diaFormatado}`;

            // Evento de clique no dia
            celula.addEventListener("click", () => {
                dataInput.value = celula.dataset.date;
                modal.classList.remove("hidden");  // Exibe o modal
            });

            linha.appendChild(celula);

            // Nova linha a cada final de semana
            if ((primeiroDia + dia) % 7 === 0) {
                corpoCalendario.appendChild(linha);
                linha = document.createElement("tr");
            }
        }

        // Adiciona a última linha de dias
        corpoCalendario.appendChild(linha);
    }

    botaoAnterior.addEventListener("click", () => {
        mesAtual--;
        if (mesAtual < 0) {
            mesAtual = 11;
            anoAtual--;
            anoSeletor.value = anoAtual;
        }
        gerarCalendario(mesAtual, anoAtual);
    });

    botaoProximo.addEventListener("click", () => {
        mesAtual++;
        if (mesAtual > 11) {
            mesAtual = 0;
            anoAtual++;
            anoSeletor.value = anoAtual;
        }
        gerarCalendario(mesAtual, anoAtual);
    });

    anoSeletor.addEventListener("change", (event) => {
        anoAtual = parseInt(event.target.value);
        gerarCalendario(mesAtual, anoAtual);
    });

});
