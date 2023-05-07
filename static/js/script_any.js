//  2
var numColores = 1;
var txt1 = null;
var txt2 = null;
var txt3 = null;
var txt4 = null;
// 3
var clic
var clic
var clic
var clic

class circulo {
    constructor(numPalabra, valor) {
        this.numPalabra = numPalabra;
        this.valor = valor;
        this.porcentaje = 30;
    }

    clic1() {
        this.porcentaje = 50;
    }

    // clic2() {
    //     this.porcentaje = ;
    // }

    // clic3() {
    //     this.porcentaje = 30;
    // }
}

function Inicio() {
    step3();
}

function addColor() {
    numColores++;
    document.getElementById("menos").style.display = "flex";
    if (numColores == 2) {
        document.getElementById("color2").style.display = "block";
    } else {
        if (numColores == 3) {
            document.getElementById("color3").style.display = "block";
            document.getElementById("mas").style.display = "none";

        }
    }
}

function deleteColor() {
    numColores--;
    document.getElementById("mas").style.display = "flex";
    if (numColores == 2) {
        document.getElementById("color3").style.display = "none";
    } else {
        if (numColores == 1) {
            document.getElementById("color2").style.display = "none";
            document.getElementById("menos").style.display = "none";
        }
    }
}

function step3() {
    // PALABRA 1
    // const textInput = document.getElementById("text-input1");
    // const text = textInput.value;

    // const circle = document.createElement("div");
    // const circle = document.getElementById("c_op1");
    // circle.classList.add("circle");
    // circle.innerHTML = text;


    // console.log(numColores);
    const input1 = document.getElementById('text-input1');

    const resultado1 = document.getElementById('c_op1');

    input1.addEventListener('input', function() {
        const txt1 = input1.value;
        // console.log(texto);
        resultado1.textContent = txt1;
    });
    // PALABRA 1
    const input2 = document.getElementById('text-input2');
    const resultado2 = document.getElementById('c_op2');

    input2.addEventListener('input', function() {
        const txt2 = input2.value;
        resultado2.textContent = txt2;
    });
    // PALABRA 1
    const input3 = document.getElementById('text-input3');
    const resultado3 = document.getElementById('c_op3');

    input3.addEventListener('input', function() {
        const txt3 = input3.value;
        resultado3.textContent = txt3;
    });
    // PALABRA 1
    const input4 = document.getElementById('text-input4');
    const resultado4 = document.getElementById('c_op4');

    input4.addEventListener('input', function() {
        const txt4 = input4.value;
        resultado4.textContent = txt4;
    });
}