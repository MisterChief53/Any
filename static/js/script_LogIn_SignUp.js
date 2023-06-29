function Inicio() {
}

function cuentaCaracteres(id) {
    const input = document.getElementById(id);
    input.addEventListener('input', function() {
        const texto = input.value;
        const caracteres = texto.length;
        if (id === 'signup-name') {
            document.getElementById("charCountName").innerHTML = `${caracteres}`;
        } else if (id === 'signup-email') {
            document.getElementById("charCountEmail").innerHTML = `${caracteres}`;
        } else if (id === 'signup-password') {
            document.getElementById("charCountPassword").innerHTML = `${caracteres}`;
        }

        const maxLength = parseInt(input.getAttribute('maxlength'));
        if (texto.length > maxLength) {
            input.value = texto.slice(0, maxLength); // Limita la longitud del texto
        }
    });
}

