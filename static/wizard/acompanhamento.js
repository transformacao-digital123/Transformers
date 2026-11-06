let arquivoAtual = "";

function formatarData(campo) {

// Aqui removerá tudo que não for Nº, em que \D significa qualquer caractere que não seja Nº e g significa global, para que possa ser aplicado em todo o texto, e tnão será substituído por ""
    let valor = campo.value.replace(/\D/g,"");

// Se o texto possuir mais que 8 caracteres ele o corta o limitando apenas aos 8 primeiros
    if (valor.length > 8) {
        valor = valor.slice(0,8);
    }

// Se o texto possuir mais que 4 caracteres...
    if (valor.length > 4) {

// Será feito a substituição, em que ^(\d{2}) captura os 2 primeiros digitos e os gurda no grupo 1, ^(\d{2}), dia, e assim sucessivamente, aqui siginifica que ele digitou o dia e mês, então já são exibidos as 2 barras de separação da data. Lembrando que o .* ignora qualquer outra coisa no final
        valor = valor.replace(/^(\d{2})(\d{2})(\d{1,4}).*/,"$1/$2/$3");

// Se não, caso o valor possua mais que 2 caracteres pelo menos...
    } else if (valor.length > 2) {

// Será feito a substituição, em que ^(\d{2}) captura os 2 primeiros digitos e os gurda no grupo 1, ^(\d{2}), dia, e assim sucessivamente, aqui significa que ele já escreveu o dia e começou a escrever o mês,então surge a 1º barra. Vale ressaltar que ^ obriga o javascript a analisar desde o começo do texto
        valor = valor.replace(/^(\d{2})(\d{1,2})/, "$1/$2");
    }

// Dá o valor formatado a tela do usuário
    campo.value = valor;
}

function converterDataParaISO(data) {

// Aqui match procurará uma correspondência usando uma Expressão Regular (Regex). Os ^ e $ indicam que o texto devem terminar exatamente com esse padrão pré estabelecido, sem espaço ou letras extras
// Cada \d{2} representa o uma parte da data, em seuência, dia-mês-ano
    const correspondencia = data.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);

// Se o usuário digitar algo que não seja Nº ou exceder o Nº de digitos permitidos o resultado será null
    if (!correspondencia) {
        return null;
    }

    const [, dia, mes, ano] = correspondencia;

    const diasNoMes = new Date(
        Number(ano),
        Number(mes),
        0
    ).getDate();

    if (
        Number(mes) < 1 ||
        Number(mes) > 12 ||
        Number(dia) < 1 ||
        Number(dia) > diasNoMes
    ) {
        return null;
    }

    return `${ano}-${mes}-${dia}`;
}

function carregarDados() {

    const dataDigitada = document.getElementById("data").value;
    const data = converterDataParaISO(dataDigitada);
    const turno = document.getElementById("turno").value;

// Se o usuário não escolher nem turno nem data aparecerá essa mensagem
    if (!data || !turno){
    alert("Selecione uma data e turno");
    return;
    }
    
    const botaoAtualizar = document.getElementById("btn-atualizar");
    botaoAtualizar.disabled = true;
    botaoAtualizar.textContent = "Carregando...";

// Aqui o .find irá vasculhar o arquivosDisponíveis buscando um valor condizente ao requerido, no caso, tanto a data quanto o turno devem ser correspondentes
    const arquivoSelecionados = arquivosDisponiveis.find(arquivo => arquivo.data === data && arquivo.turno === turno)

// Se o .find não encontra um valor correspondente ele mandará essa mensagem
    if (!arquivoSelecionados) {
    document.getElementById("tabela-dados").innerHTML = "";
    arquivoAtual = null;

    alert("Não foi encontrada uma planilha para essa data e/ou turno");
    restaurarBotaoAtualizar();
    return;
    }

// Se achar ele guardará o nome físico do arquivo aqui
    arquivoAtual = arquivoSelecionados.nome;

    fetch("/dados-acompanhamento?arquivo=" +
        encodeURIComponent(arquivoAtual)
    )

// Transforma a resposta que vier em uma linguagem que o javascript entenda, json
    .then(function(resposta) {
        return resposta.json();
    })

    .then(resultado => {

// Se ocorrer um erro nessa parte será enviada uma mensagem de erro para ambos
        if (resultado.erro || resultado.Erro) {

            restaurarBotaoAtualizar();
            alert(resultado.erro || resultado.Erro);
            return;
        }

        const tabela =
            document.getElementById("tabela-dados");

// Pega a página HTML e apaga o conteúdo dele, isso serve para quando formos mudar de data ou turno
        tabela.innerHTML = "";

// Aqui ele recebeu uma lista das linhas em que ele passará linha por linha num loop (serve para criar uma linha "tr" para cada linha do Excel)
        resultado.dados.forEach(item => {

// É criada uma linha de tabela em branco
            const tr = document.createElement("tr");

// O tr é a linha inteira, enquanto cada td é uma célula dessa linha

// Aqui ele irá criar uma célula vazia que irá conter o nome da aba  do excel e então será posto dentro da aba que criamos (tr (table row (linha da tabela)))
// O appendChild() significa, neste contexto, adicionara célula com texto a linha HTML
            const tdAba = document.createElement("td");
            tdAba.textContent = item.aba;
            tr.appendChild(tdAba);

// Aqui ele irá criar uma célula (td (table data(dado da tabela))) vazia que irá conter o nome da do Nº linha do excel e então será posto dentro da linha que criamos (tr) só que dessa vez é posto o Nº da linha física do Excel na 2ª coluna da tabela
// O appendChild() significa, neste contexto, adicionar a célula com Nº da linha na linha HTML
            const tdLinha = document.createElement("td");
            tdLinha.textContent = item.linha;
            tr.appendChild(tdLinha);

// O valores já visualizou quais são as colunas desde app.py, então é criada uma célula para cada um dos valores de cada linha
// O ?? serve para, caso a célula esteja vazia ao invés de pôr null, põe o valor especificado, no caso ""
            item.valores.forEach(valor =>{

                const td = document.createElement("td");

                td.textContent =
                    valor ?? "" ;

// 
                tr.appendChild(td);

            });

            tabela.appendChild(tr);

        });

        restaurarBotaoAtualizar();

    })

    .catch(erro => {
        console.error(erro);
        restaurarBotaoAtualizar();
        alert("Erro ao carregar os dados.");
    });
}

function restaurarBotaoAtualizar(){
    const botaoAtualizar = document.getElementById("btn-atualizar");

    botaoAtualizar.disabled = false;
    botaoAtualizar.textContent = "🔄 Atualizar";
}

function baixarExcel() {

// Serve para, caso arquivoatual esteja vazio, mandar essa mensagem
    if (!arquivoAtual) {
        alert("Selecione um arquivo.");
        return;
    }

// Navega até a rota de download
    window.location.href =

// substirui a palavra que tiver depois do = pelo valor de arquivoAtual
        "/baixar-acompanhamento?arquivo=" +
        encodeURIComponent(arquivoAtual);
}

let arquivosDisponiveis = [];

function carregarOpcoes(){
    fetch("/opcoes-acompanhamento")

// Aqui pegamos o valor que for recebido e transformamos em json
    .then(resposta => resposta.json())

    .then(resultado => {

// Aqui guardaremos o valor recebido dentro de arquivosDisponiveis
        arquivosDisponiveis = resultado.arquivos;

        const campoTurno = document.getElementById("turno");

// Guardará em data arquivosDisponíveis, que, através do .map, pegará da lista que receber só as turnos e porá em arquivos (graças ao new set() nenhuma das turnos pegas será duplicada e o ... transforma o Set em uma lista normal de volta que poderemos usar, isso por que o Set transforma a lista em um objeto conjunto)
        const turnos = ["Manhã","Noite"];

// ForEach é "para cada", ou seja, para cada turno única recebida, adicione em campoData, mas para isso foi criada uma opção visual para põr no menu (o 1° é o texto que o usuário lê e o 2° é o que é enviado ao servidor)
        turnos.forEach(turno => {
            campoTurno.add(new Option(turno,turno))
        });
    })

// Se der qualquer problema com o servidor ou relacionado aparece a mensagem de erro
    .catch(erro => {
        console.error(erro);
        alert("Erro ao carregar as opções")
    });
}

// Essa função serve para quando selecionar data e turno a página mostrar a planilha na mesma hora ao invés de 
function carregarSeletorCompleto(){
    const data = document.getElementById("data").value;
    const turno = document.getElementById("turno").value;

    if (data && turno){
        carregarDados();
    }
}

document.getElementById("data").addEventListener("change", carregarSeletorCompleto);
document.getElementById("data").addEventListener("input", function() {formatarData(this);})

document.getElementById("turno").addEventListener("change", carregarSeletorCompleto);


// Assim que a página web carregar essa função será ativada
carregarOpcoes();