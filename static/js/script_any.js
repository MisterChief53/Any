//  2
var numColores = 1;
var txt1 = null;
var txt2 = null;
var txt3 = null;
var txt4 = null;

// 4
var contPCve1 = 0;
var contPCve2 = 0;
var contPCve3 = 0;
var contPCve4 = 0;


class circulo {
    constructor(id, importance) {
        this.id = id;
        this.importance = importance; //esta es la importancia, false es el default, true es relevante
    }

    clic1() {
        const div = document.getElementById(this.id); //obtenemos el div
        // Aumenta el tamaño del círculo en un 50%
        const currentWidth = div.offsetWidth;
        const currentHeight = div.offsetHeight;
        const newWidth = currentWidth * 1.5;
        const newHeight = currentHeight * 1.5;
        div.style.width = `${newWidth}px`;
        div.style.height = `${newHeight}px`;

        this.importance = true;
        /*
        var data = (this.importance, this.id)
        $.ajax({
            type: "POST",
            url: "/importance_endpoint",
            data: {"data": data},
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        */
        const data = { importance: this.importance, id: this.id };
        fetch('/importance_endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error));
    }

    clic2() {
        const div = document.getElementById(this.id); //obtenemos el div
        // Disminuye el tamaño del círculo en un 50%
        const currentWidth = div.offsetWidth;
        const currentHeight = div.offsetHeight;
        const newWidth = currentWidth / 1.5;
        const newHeight = currentHeight / 1.5;
        div.style.width = `${newWidth}px`;
        div.style.height = `${newHeight}px`;

        /*
        this.importance = false;
        var data = (this.importance, this.id)
        $.ajax({
            type: "POST",
            url: "/importance_endpoint",
            data: {"data": data},
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        */
        const data = { importance: this.importance, id: this.id };
        fetch('/importance_endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error));


    }
}

function Inicio() {
    cuentaCaracteres();
    step3();
}

function cuentaCaracteres() {
    const input = document.getElementById('descripcion');
    input.addEventListener('input', function() {
        const texto = input.value;
        const caracteres = texto.length;
        document.getElementById("charCount").innerHTML = `${caracteres}`;

        const maxLength = parseInt(input.getAttribute('maxlength'));
        if (texto.length > 49) {
            input.value = texto.slice(0, 49); // Limita la longitud del texto
        }
    });
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
    // Primero hacemos validaciones para la validación de los círculos
    step_circle_creation('text-input1', 'c1');
    step_circle_creation('text-input2', 'c2');
    step_circle_creation('text-input3', 'c3');
    step_circle_creation('text-input4', 'c4');

    // PALABRA 1
    const input1 = document.getElementById('text-input1'); //guardamos lo de text-input

    const resultado1 = document.getElementById('c_op1'); //guardamos lo de c_op1

    input1.addEventListener('input', function() { //cuando escriban algo
        step_circle_creation('text-input1', 'c1'); //validamos para crear el circulo

        const txt1 = input1.value; //asignamos el valor del input
        resultado1.textContent = txt1; //se lo ponemos al circulo
    });
    // PALABRA 2
    const input2 = document.getElementById('text-input2');
    const resultado2 = document.getElementById('c_op2');

    input2.addEventListener('input', function() {
        step_circle_creation('text-input2', 'c2');

        const txt2 = input2.value;
        resultado2.textContent = txt2;
    });
    // PALABRA 3
    const input3 = document.getElementById('text-input3');
    const resultado3 = document.getElementById('c_op3');

    input3.addEventListener('input', function() {
        step_circle_creation('text-input3', 'c3');

        const txt3 = input3.value;
        resultado3.textContent = txt3;
    });
    // PALABRA 4
    const input4 = document.getElementById('text-input4');
    const resultado4 = document.getElementById('c_op4');

    input4.addEventListener('input', function() {
        step_circle_creation('text-input4', 'c4');

        const txt4 = input4.value;
        resultado4.textContent = txt4;
    });

    // step4();
}

function step_circle_creation(inputId, cId) {
    // var clics_c1 = 0
    const inputTxt = document.getElementById(inputId);

    if (inputTxt.value.trim() !== '') { //si no está vacío el input, es decir, si ya escribieron
        document.getElementById(cId).style.display = "flex"; //poner a la vista
        if (document.getElementById("sinPalabrasCve").style.display !== "none") {
            document.getElementById("sinPalabrasCve").style.display = "none";
        }

    } else { //si está vacío
        document.getElementById(cId).style.display = "none"; //desaparecer
    }

    // Poner texto "no pusiste palabras clave"
    var input1 = document.getElementById('text-input1');
    var input2 = document.getElementById('text-input2');
    var input3 = document.getElementById('text-input3');
    var input4 = document.getElementById('text-input4');

    if (input1.value.trim() === '' && input2.value.trim() === '' && input3.value.trim() === '' && input4.value.trim() === '') { //si no hay ninguna palabra escrita
        document.getElementById("sinPalabrasCve").style.display = "flex"; //se habilita la frase
    }

}

function step4_clicPalabra(id) {
    var contPCve;
    var circulo1;
    circulo1 = new circulo(id, false);

    if (id == 'c1') {
        contPCve1++;
        contPCve = contPCve1;
    } else {
        if (id == 'c2') {
            contPCve2++;
            contPCve = contPCve2;
        } else {
            if (id == 'c3') {
                contPCve3++;
                contPCve = contPCve3;
            } else {
                if (id == 'c4') {
                    contPCve4++;
                    contPCve = contPCve4;
                }
            }
        }
    }

    if (contPCve % 2 == 0) { //si el clic es par
        circulo1.clic2(); //se hace pequeño

    } else { //si no es par
        circulo1.clic1();
    }
}

// if (id == 'c1') {
//     contPCve1++;
//     if (contPCve1 % 2 !== 0) { //si no se han dado num par de clic entonces
//         palabraCve1.clic2(); //se hace importante
//         auxCrece = false
//     } else { //sino
//         palabraCve1.clic1(); //se pone default otra vez
//     }
// }
// if (id == 'c2') {
//     contPCve2++;
//     if (contPCve2 % 2 !== 0) { //si no se han dado num par de clic entonces
//         palabraCve2.clic2(); //se hace importante
//         auxCrece = false
//     } else { //sino
//         palabraCve2.clic1(); //se pone default otra vez
//     }
// }
// if (id == 'c3') {
//     contPCve3++;
//     if (contPCve3 % 2 !== 0) { //si no se han dado num par de clic entonces
//         palabraCve3.clic2(); //se hace importante
//         auxCrece = false
//     } else { //sino
//         palabraCve3.clic1(); //se pone default otra vez
//     }
// }
// if (id == 'c4') {
//     contPCve4++;
//     if (contPCve4 % 2 !== 0) { //si no se han dado num par de clic entonces
//         palabraCve4.clic2(); //se hace importante
//         auxCrece = false
//     } else { //sino
//         palabraCve4.clic1(); //se pone default otra vez
//     }
// }