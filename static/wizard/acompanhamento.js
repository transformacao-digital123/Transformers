        let arquivoAtual = "";

        function carregarDados() {

           const data = document.getElementById("data").value;
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

                const campoData = document.getElementById("data");
                const campoTurno = document.getElementById("turno");

// Guardará em data arquivosDisponíveis, que, através do .map, pegará da lista que receber só as datas e porá em arquivos (graças ao new set() nenhuma das datas pegas será duplicada e o ... transforma o Set em uma lista normal de volta que poderemos usar, isso por que o Set transforma a lista em um objeto conjunto)
                const datas = [...new Set(
                    arquivosDisponiveis.map(arquivo => arquivo.data)
                )];

// Guardará em data arquivosDisponíveis, que, através do .map, pegará da lista que receber só as turnos e porá em arquivos (graças ao new set() nenhuma das turnos pegas será duplicada e o ... transforma o Set em uma lista normal de volta que poderemos usar, isso por que o Set transforma a lista em um objeto conjunto)
                const turnos = ["Manhã","Noite"];

// ForEach é "para cada", ou seja, para cada data única recebida, adicione em campoData, mas para isso foi criada uma opção visual para põr no menu (o 1° é o texto que o usuário lê e o 2° é o que é enviado ao servidor)
                datas.forEach(data => {
                    campoData.add(new Option(data,data))
                });

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
        document.getElementById("turno").addEventListener("change", carregarSeletorCompleto);
        

// Assim que a página web carregar essa função será ativada
        carregarOpcoes();