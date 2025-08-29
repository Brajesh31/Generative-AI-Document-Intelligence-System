document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const fileNameDisplay = document.getElementById("fileName");
  const dropZone = document.querySelector(".custom-dropzone");

  // Display selected file name
  if (fileInput && fileNameDisplay) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file) {
        fileNameDisplay.textContent = `Selected: ${file.name}`;
      } else {
        fileNameDisplay.textContent = "";
      }
    });
  }

  // Drag and drop events
  if (dropZone) {
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.style.backgroundColor = "#ebf9ff";
    });

    dropZone.addEventListener("dragleave", (e) => {
      e.preventDefault();
      dropZone.style.backgroundColor = "#f9fdff";
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.style.backgroundColor = "#f9fdff";
      const files = e.dataTransfer.files;

      if (files.length > 0 && fileInput) {
        fileInput.files = files;
        fileNameDisplay.textContent = `Selected: ${files[0].name}`;
      }
    });

    // Optional click-to-open file dialog
    dropZone.addEventListener("click", () => {
      if (fileInput) fileInput.click();
    });
  }
});
