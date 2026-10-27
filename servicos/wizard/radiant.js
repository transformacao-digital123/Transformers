// // Criou as 2 contantesuma é o optimus que receberá quem tiver id = "optimus" e formulario, que procura e captura o 1º formulário que encontrar na página, no caso as partes de preenchimento eo botão, e o oultimo captura o container,a caixa onde ocorrerá a animação
//     const formulario = document.querySelector("form");
//     const optimus = document.getElementById("optimus");
//     const areaAnimacao = document.getElementById("animacao-transformers");
//     const mensagemErro = document.getElementById("mensagem-erro");

//     let intervaloProgresso;
//     let falhasConsultasProgresso = 0;        
//     let posicaoInicialOptimus;

//     function mostrarErro(){
//         optimus.style.transition = "none";

//         optimus.style.left = "0px";

//         optimus.src = "static/assets/Optimus-erro.png";
//         optimus.style.width = "230px";

//         optimus.style.opacity = "1";
//     }

//     function finalizarAnimacao(){
//         optimus.style.transition = "none";
//         optimus.style.opacity = "0";
//         optimus.style.left = "0px";

//         setTimeout(function(){

//             optimus.style.opacity = "1";
//             optimus.src = "static/assets/optimus_voltando_a_ser_robo.gif";
//             optimus.style.width = "170px";
//         }, 200);

//         setTimeout(function(){

//             optimus.src = "static/assets/Optimus-Run.gif";
//             optimus.style.width = "";
//         }, 1000);
//     }

//     function acompanharProgresso(){
//         console.log("ACOMPANHAMENTO INICIADO");

//         posicaoInicialOptimus = optimus.offsetLeft;
//         larguraAreaMovimento = areaAnimacao.offsetWidth; // Calcula a área total,desde a largura total do conteúdo até os paddings internos de ambos os lados
//         larguraOptimusMovimento = optimus.offsetWidth;

// // O setInterval executa a função a cada 500ms,como especificado mais a baixo na função e o resultado guardado em intervaloProgresso
//         intervaloProgresso = setInterval(function(){
//             console.log("CONSULTANDO PROGRESSO...");

// // O querySelector serve localizar o campo está oculto do formulário que contém o id_conversão, enquanto o value lê o valor contido nesse campo
//             const idConversao = document.querySelector(
//                 'input[name="id_conversao"]'
//             ).value;

// // Pede a rota progresso os dados mais atuais do andamento da tarefa
// // No caso o encodeURIComponent(idConversao) coloca o valor de cada id_conversão depois do = na url pra ser visualizada pelo args
//             fetch(`/progresso?id_conversao=${encodeURIComponent(idConversao)}`)

// // Assim que receber os dados do servidor ele transformará json que é uma forma mais fácil do javascrpt trabalhar com os dados
//                 .then(function(resposta){
//                     console.log("RESPOSTA DO PROGRESSO:", resposta.status);

//                     if (!resposta.ok){
//                         throw new Error("Não foi possível consultar o progresso") // O  throw new Error para o fluxo do programa e encaminha para o .catch()
//                     }
//                     return resposta.json();
//                 })

// // Quando os dados forem transformados em json, ele executará a função que está dentro do .then, e o resultado será guardado na variável dados, que é o que será mostrado no console.log como um print
//                 .then(function(dados){

// // Aqui devemos manter 0 pois não ocorreu nenhum erro ainda
//                     falhasConsultasProgresso = 0;

//                     console.log("progresso:", dados.progresso);
//                     console.log("status:", dados.status);

// // Se status for igual a erro, dará erro
//                     if (dados.status === "erro"){

//                         pararAcompanhamentoProgresso();

// // Aqui não usamos throw new Error porque o tipo de erro não é falha na comunicação com o servidor, mas sim falha na conversão
//                         mensagemErro.innerHTML = "❌ " + (dados.erro || "A conversão falhou");
//                         mensagemErro.style.display = "inline-block";
//                         mostrarErro();
//                         return;
//                     }

// // Se status for igual a concluído, chamará a função pararAcompanhamentoProgresso
//                     if (dados.status === "concluido"){
//                         pararAcompanhamentoProgresso();
//                     }

//                     let progresso = dados.progresso; // Guarda o valor que estiver em dados.progresso em progresso

//                     let larguraArea = areaAnimacao.offsetWidth; // Calcula a área total,desde a largura total do conteúdo até os paddings internos de ambos os lados
//                     let larguraMovimento = larguraArea - larguraOptimusMovimento - posicaoInicialOptimus; // A subtração disso é o valor que ele terá de andar

//                     let posicao = posicaoInicialOptimus + (progresso / 100) * larguraMovimento;

// // Esse limite final será responsável por impedir que o optimus passe da parede
//                     let limiteFinal = posicaoInicialOptimus + larguraMovimento;

// // Ele pega entre os 2 valores oferecidos a ele e escolhe o menor. Por exemplo, se posicao está em 760 (um valor que já passa da parede) e limiteFinal é 750, o valor de posicao será o do limiteFinal
//                     posicao = Math.min(posicao,limiteFinal);

//                     optimus.style.transition = "left 0.5s linear";
//                     optimus.style.left = posicao + "px";
//                     console.log("POSIÇÃO DO OPTIMUS:", posicao);
//                 })

// // Só será usado quando o tipo de erro for falta de comunicação com o servidor
//                 .catch(function(erro){
//                     console.log("Erro ao consultar o progresso: ", erro);

// // Aqui ele vai aumentando o valor da falha de 1 em 1, ou seja, se o valor inicial é 0, toda vez que o .catch for chamado ele vai aumentar 1
//                     falhasConsultasProgresso++;

// // Se ele chegar em um Nº igual ou maior que 10 ele irá acionar a função de pra parar o progresso
//                     if (falhasConsultasProgresso >= 10){
//                         pararAcompanhamentoProgresso();
                    

//                         mensagemErro.innerHTML = "❌" + erro.message;
//                         mensagemErro.style.display = "inline-block";
//                         mostrarErro();
//                     }
//                 });

//         }, 500); // Númmero de milissegundos que a função levará para fazer cada atualização, nesse caso a cada 0.5s ele fará uma nova requisição para a rota /progresso
//     }

//     function pararAcompanhamentoProgresso(){
//         clearInterval(intervaloProgresso);
//     }

//     let ultimoLinkConvertido = null;

// // O .addEventListener fica vigiando,quando formulario disparar o evento "submit" ele iniciará a função
// // Aqui o atributo de origem src substituirá o que estiver em optimus pelo caminho descrito
//     formulario.addEventListener("submit", function(event){
//         console.log("SUBMIT FOI EXECUTADO");

// // Impede o comportamento padrão do formulário do navegador, é como se ele dissesse ao navegador: "Navegador, não envie esse formulário do jeito tradicional. Eu, JavaScript, vou cuidar disso."
//         event.preventDefault();

//         const linkAtual = document.getElementById("link").value.trim();

//         if (linkAtual == ultimoLinkConvertido){
//             const confirmar = confirm(
//                 "Este link já foi convertido anteriormente, tem Certeza que quer convertê-lo novamente?"
//             );
//             if (!confirmar){
//                 return;
//             }
//         }

//         const dados = new FormData(formulario);
        
//         let ocorreuErro = false;

//         acompanharProgresso();

//         mensagemErro.style.display = "none";

// // Estado inicial
//         optimus.src = "static/assets/Optimus-Run.gif";
//         optimus.style.transition = "none";
//         optimus.style.opacity = "1";

// // Após 0.1s ele inicia a transformação
//         setTimeout(function(){
//             if (ocorreuErro) return; // Se ocorreu err  o aqui,segue seu rumo

//             optimus.src = "static/assets/optimus_transformando_em_caminhao.gif";
//             optimus.style.width = "170px";
//             },100); //Esse 100 representa linha de largada,é a partir do momento 0.1s que ele iniciará

// // 1000 - 100 = 900ms de tempo que a transformação terá para ser executada e então se iniciará o gif luaria_caminhao
// // Destino calcula a área que será percorrida, e essa variável é usada pra arrastar da esquerda pra direita em forma linear em 3s, considerando o valor do destino em px,pra ser mais fácil do programa contabilizar
//         setTimeout(function(){
//             if (ocorreuErro) return;
//             optimus.src = "static/assets/luari_caminhao.gif";

//             optimus.style.width = "210px";

//         },500); // Esse 500 repreenta os milissegundos, 500ms = 0.5s

//         fetch("/",{
//             method: "POST",
//             headers: {
//                 "X-Requested-With": "XMLHttpRequest" // Esse cabeçalho é usado para indicar que a requisição está sendo feita via AJAX, permitindo que o servidor diferencie entre requisições normais e requisições assíncronas, pense nele como uma etiqueta do 2º pedido de 2, ele serve para que possa diferenciar quando quer executá-lo ou deixar de executá-lo, pois o 1º pedido é o normal, que é o GET, e o 2º pedido é o AJAX, que é o POST
//             },
//             body: dados
//         })

//         .then(function(resposta){
//             console.log("STATUS:", resposta.status);
//             console.log("RESPOSTA OK:", resposta.ok);

// // O ! torna tudo inverso, então caso a resposta esteja errada, o ! considerará veradadeira e a levará ao próximo comando que é o indicador de erro,mas caso esteja correta, o ! considerará falsa e então pulará aquele comando indo direto ao return
// // Os dados obtidos será transformado em texto pois o javascript não sabe que tipo de arquivo é,se ele é .img,.pdf ou json, então ao especificar pra ele, a resposta é retornada para a próxima função
//             if(!resposta.ok){
//                 return resposta.json().then(function(erro){
//                     throw new Error(erro.erro);
//                 });
//             }
//             return resposta.json()

//                 .then(function(resultado){
//                     console.log("Resposta do Flask:", resultado);

// // Se o resultado for falso, o ! inverterá pra verdadeiro e então ele irá para o próximo comando que é o indicador de erro, mas caso seja verdadeiro, o ! inverterá para falso e então ele pulará aquele comando indo direto ao console.log
//                     if(!resultado.sucesso){
//                         throw new Error("A conversão não foi concluída");
//                     }

//                     ultimoLinkConvertido = linkAtual;

//                     const botaoImprimir = document.getElementById("btn-imprimir-etiquetas");

//                     if (botaoImprimir){
//                         botaoImprimir.style.display = "block";
//                     }
                    
//                     const idConversao = document.querySelector(
//                         'input[name = "id_conversao"]'
//                     ).value;

//                     pararAcompanhamentoProgresso();

//                     console.log("JSON RECEBIDO:", resultado);
//                     console.log("SUCESSO:", resultado.sucesso);

//                     finalizarAnimacao();
                    
// // No caso o encodeURIComponent(idConversao) coloca o valor de cada id_conversão depois do = na url pra ser visualizada pelo args
//                     window.location.href = `/baixar-arquivo?id_conversao=${encodeURIComponent(idConversao)}`

//                     console.log("Processamento concluído com sucesso");
//                 });
//         })

//         .catch(function(erro){
//             console.error("Erro:",erro);
//             ocorreuErro = true;
//             if (erro.message === "Ocorreu um erro inesperado"){
//                 mensagemErro.innerHTML = "⚠ " + erro.message;
//             }else{
//                 mensagemErro.innerHTML = "❌ " + erro.message;
//             }
//             mensagemErro.style.display = "inline-block";
//             mostrarErro();

//             pararAcompanhamentoProgresso();
//         })
        

//     const botaoImprimir =document.getElementById("btn-imprimir-etiquetas");

//     if (botaoImprimir){

//         botaoImprimir.addEventListener("click", function(){

//             fetch("/imprimir-etiquetas", {
//                 method: "POST",
//                 headers: {
//                     "X-Requested-With": "XMLHttpRequest"
//                 }
//             })
//             .then(function(resposta){
//                 return resposta.json();
//             })
//             .then(function(resultado){

//                 if(resultado.sucesso){
//                     alert("Etiquetas enviadas para impressão!");
//                 } else {
//                     alert(resultado.erro);
//                 }
//             })

//             .catch(function(erro){
//                 console.error("Erro ao imprimir etiquetas:", erro);
//                 alert("Não foi possível imprimir as etiquetas.");      
//             })
//         });
//     }
    
// });