const select = document.getElementById("numero-pallet");

for (let i = 1; i <= 100; i++) {
    const opcao = document.createElement("option");

// Aqui é a parte de como o programara guardará pára si o valor inserido, no caso se inserirem 1, ele guardará 01
// Essa parte é importante porque, caso a resposta de opcao.value fosse só i,caso fosse o 1º pallet ele guardaria só 1, quando na v erdade ele deve guardar o valor 01 pois esse é o valor que será mandado ao flask, mais especificamente no arquivo odp.py em str(pallet_linha) == str(numero_pallet).strip(), onde será feito uma comparação, se não fosse por isso daria 1 = 01, mas com isso dá certo ficando 01 = 01
    opcao.value = String(i).padStart(2, "0");

// E aqui é como será exibido para o acompanhamento, exibindo Pallet 01, com o padStart determinando que deve ter no mínimo 2 digitos o valor do pallet, e se não houver Nº o suficiente ele completa com 0
    opcao.textContent = `Pallet ${String(i).padStart(2, "0")}`;

    if (i === 1) {
        opcao.selected = true;
    }

    select.appendChild(opcao);
}

let identificadorAtual = null;

function quandoLerQR(texto){

    identificadorAtual = texto;

    const numeroPallet = document.getElementById("numero-pallet").value;

    document.getElementById("resultado").textContent = "QR encontrado: " + texto;

    console.log("QR: ", texto);

    console.log("ENVIANDO IDENTIFICADOR PARA O BACKEND: ", identificadorAtual);

    console.log("ANTES DO FETCH");

    fetch("/registrar-despacho", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(
            {identificador: identificadorAtual,
            numero_pallet: numeroPallet,
            cancelar: document.getElementById("cancelar").checked
            })
    })
    .then(function(resposta){

        console.log("RESPOSTA HTTP: ", resposta);
        return resposta.json();
    })

    .then(function(resposta){
        console.log("RESPOSTA DO FLASK: ", resposta);

        if (!resposta.sucesso){
            document.getElementById("resultado").innerHTML = `
            <h2>⚠️ Não foi possível realizar a operação</h2>
            <p>${resposta.erro || "Ocorreu um erro inesperado"}</p>`;

            return;
        }

        if (resposta.cancelado){
            document.getElementById("resultado").innerHTML = `
            <h2>❌ Despache cancelado</h2>
            <p>Pallet Nº <stong>${resposta.numeroPallet}</strong> cujo o identificador é <strong>${resposta.identificadorAtual}</strong> foi cancelado</p>`;
            
            return; 
        }

        if (resposta.ja_despachado){
            document.getElementById("resultado").innerHTML = `
            <h2>⚠️ Pallet já despachado</h2>
            <p><strong>Horário da 1º bipagem: </strong> ${resposta.hora_despacho}</p>`;

            return;
        }

        document.getElementById("resultado").innerHTML = `
        <h2>✅ Despacho Registrado</h2>
        <p>ODP despachada às <strong>${resposta.hora_despacho}</strong></p>`;
    })

    .catch(function(erro){
        console.error("ERRO AO ENVIAR O IDENTIFICADOR: ", erro)
    })
}

const leitor = new Html5QrcodeScanner(
    "leitor",
    {
        fps: 10,
        qrbox: {
            width: 250,
            height: 250
        }
    }
);

leitor.render(
    quandoLerQR
);