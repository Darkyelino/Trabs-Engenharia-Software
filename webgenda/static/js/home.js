document.addEventListener("DOMContentLoaded", () => {
    const corpoCalendario = document.getElementById("corpo-calendario");
    const anoSeletor = document.getElementById("ano-seletor");
    const botaoAnterior = document.getElementById("mes-anterior");
    const botaoProximo = document.getElementById("mes-proximo");
    const mesAtualTexto = document.getElementById("mes-atual");
    const formEvento = document.getElementById("form-evento");
    const inputDataEvento = document.getElementById("data-evento");
    const fecharFormBtn = document.getElementById("fechar-form");

    const modalDetalhes = document.getElementById("detalhes-evento");
    const fecharDetalhesBtn = document.getElementById("fechar-detalhes");
    const detalheData = document.getElementById("detalhe-data");
    const detalheTitulo = document.getElementById("detalhe-titulo");
    const detalheDescricao = document.getElementById("detalhe-descricao");

    // Pega os eventos do atributo data-eventos no body
    const eventosDataAttr = document.body.getAttribute("data-eventos");
    const eventosSalvos = eventosDataAttr ? eventosDataAttr.split("|").map(eventoStr => {
        const [data, titulo, descricao] = eventoStr.split(";");
        return { data, titulo, descricao };
    }) : [];

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
            celula.classList.add("dia");

            const diaFormatado = String(dia).padStart(2, '0');
            const mesFormatado = String(mes + 1).padStart(2, '0');
            const dataCompleta = `${ano}-${mesFormatado}-${diaFormatado}`;
            celula.dataset.date = dataCompleta;

            // Verifica se a data tem evento
            const eventoDoDia = eventosSalvos.find(ev => ev.data === dataCompleta);
            if (eventoDoDia) {
                celula.classList.add("tem-evento");

                // Clicando em dia com evento mostra detalhes
                celula.addEventListener("click", () => {
                    detalheData.textContent = eventoDoDia.data;
                    detalheTitulo.textContent = eventoDoDia.titulo;
                    detalheDescricao.textContent = eventoDoDia.descricao;
                    modalDetalhes.style.display = "flex";
                });
            } else {
                // Clicando em dia sem evento abre o form
                celula.addEventListener("click", () => {
                    inputDataEvento.value = celula.dataset.date;
                    formEvento.style.display = "flex";
                });
            }

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

    fecharFormBtn.addEventListener("click", () => {
        formEvento.style.display = "none";
    });

    fecharDetalhesBtn.addEventListener("click", () => {
        modalDetalhes.style.display = "none";
    });

    // Inicialização
    preencherAnos();
    gerarCalendario(mesAtual, anoAtual);
});
