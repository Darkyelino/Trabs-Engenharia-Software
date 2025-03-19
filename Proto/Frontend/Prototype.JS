document.addEventListener("DOMContentLoaded", () => {
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
        let anoInicio = anoAtual - 50;
        let anoFim = anoAtual + 10;
        for (let ano = anoInicio; ano <= anoFim; ano++) {
            let opcao = document.createElement("option");
            opcao.value = ano;
            opcao.textContent = ano;
            if (ano === anoAtual) opcao.selected = true;
            anoSeletor.appendChild(opcao);
        }
    }

    function gerarCalendario(mes, ano) {
        corpoCalendario.innerHTML = "";
        mesAtualTexto.textContent = `${nomesMeses[mes]} de ${ano}`;

        let primeiroDia = new Date(ano, mes, 1).getDay();
        let ultimoDia = new Date(ano, mes + 1, 0).getDate();

        let linha = document.createElement("tr");
        for (let i = 0; i < primeiroDia; i++) {
            linha.appendChild(document.createElement("td"));
        }

        for (let dia = 1; dia <= ultimoDia; dia++) {
            let celula = document.createElement("td");
            celula.textContent = dia;
            linha.appendChild(celula);

            if ((primeiroDia + dia) % 7 === 0) {
                corpoCalendario.appendChild(linha);
                linha = document.createElement("tr");
            }
        }

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

    preencherAnos();
    gerarCalendario(mesAtual, anoAtual);
});
