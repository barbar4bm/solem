document.addEventListener("DOMContentLoaded", (event) => {
  const uploadContainer = document.querySelector(".upload-container");
  const jsonFileInput = document.getElementById("jsonFile");
  const submitJsonButton = document.getElementById("submitJson");
  const anversoImage = document.getElementById("anversoImage");
  const reversoImage = document.getElementById("reversoImage");
  const serverResponse = document.getElementById("serverResponse");
  const resultAnverso = document.getElementById("resultAnverso");
  const resultReverso = document.getElementById("resultReverso");
  const ocrImageInput = document.getElementById("ocrImage");
  const uploadedImage = document.getElementById("uploadedImage");
  const startOcrButton = document.getElementById("startOcr");
  const ocrResult = document.getElementById("ocrResult");

  uploadContainer.addEventListener("click", function () {
    jsonFileInput.click();
  });

  jsonFileInput.addEventListener("change", function () {
    const file = jsonFileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const jsonData = JSON.parse(e.target.result);
        if (jsonData.anverso) {
          anversoImage.src = "data:image/png;base64," + jsonData.anverso;
          anversoImage.style.display = "block";
        }
        if (jsonData.reverso) {
          reversoImage.src = "data:image/png;base64," + jsonData.reverso;
          reversoImage.style.display = "block";
        }
      };
      reader.readAsText(file);
    }
  });

  submitJsonButton.addEventListener("click", async function () {
    const file = jsonFileInput.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("archivo_json", file);

      try {
        const response = await fetch("/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          alert("Error al enviar el archivo JSON. Intenta nuevamente.");
          return;
        }

        const jsonResponse = await response.json();

        // Crear una nueva respuesta sin 'ocr_data'
        const verificaciones=jsonResponse;

        serverResponse.style.display = "block";
        serverResponse.textContent = JSON.stringify(verificaciones, null, 2);

        // Mostrar resultados
        if (jsonResponse.resp_Anverso) {
          resultAnverso.textContent = jsonResponse.reconoce_Anverso;
        }
        if (jsonResponse.resp_reverso) {
          resultReverso.textContent = jsonResponse.reconoce_Reverso;
        }

        alert("¡Archivo JSON enviado con éxito!");
      } catch (error) {
        alert("Error al enviar el archivo JSON.");
      }
    } else {
      alert("Por favor, sube un archivo JSON primero.");
    }
  });

  document
    .querySelectorAll(".upload-container")[1]
    .addEventListener("click", function () {
      ocrImageInput.click();
    });

  ocrImageInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        uploadedImage.src = e.target.result;
        uploadedImage.style.display = "block";
      };
      reader.readAsDataURL(file);
    }
  });

  startOcrButton.addEventListener("click", async function () {
    const file = ocrImageInput.files[0];
    if (file) {
      try {
        const formData = new FormData();
        formData.append("image", file);

        const response = await fetch("/ocr", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          alert("Hubo un error al procesar la imagen. Intenta nuevamente.");
          return;
        }

        const result = await response.text();
        ocrResult.style.display = "block";
        ocrResult.textContent = result;
      } catch (error) {
        alert("Hubo un error al procesar la imagen.");
      }
    } else {
      alert("Por favor, sube una imagen primero.");
    }
  });
});
