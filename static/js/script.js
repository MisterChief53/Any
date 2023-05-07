const addButton = document.getElementById("add-button");
const circleContainer = document.getElementById("circle-container");
let clics = 0;
let circles =0;

addButton.addEventListener("click", () => {
  const textInput = document.getElementById("text-input");
  const text = textInput.value;
  textInput.value = "";
  clics = 0 ;
  circles++;
  if(circles > 4){
    document.getElementById("boton").disabled = true;
  }

  const circle = document.createElement("div");
  circle.classList.add("circle");
  circle.innerHTML = text;

  circleContainer.appendChild(circle);
  circle.addEventListener("click", () => {
    clics++;
    if (clics > 3) {
      document.getElementById("boton").disabled = true;
    }
  // Aumenta el tamaño del círculo en un 50%
  const currentSize = circle.offsetWidth;
  const newSize = currentSize * 1.5;
  circle.style.width = `${newSize}px`;
  circle.style.height = `${newSize}px`;
});

});

const colorInput = document.getElementById("color-input");
		const saveButton = document.getElementById("save-button");
		const colorList = document.getElementById("color-list");

		// Cargar colores guardados al iniciar la página
		for (let i = 0; i < localStorage.length; i++) {
			const key = localStorage.key(i);
			const value = localStorage.getItem(key);
			addColorToList(value);
		}

		saveButton.addEventListener("click", () => {
			const color = colorInput.value;
			addColorToList(color);
			saveColorToLocalStorage(color);
		});

		function addColorToList(color) {
			const li = document.createElement("li");
			li.style.backgroundColor = color;
			li.textContent = color;
			colorList.appendChild(li);
		}

		function saveColorToLocalStorage(color) {
			localStorage.setItem(`color-${localStorage.length + 1}`, color);
		}

