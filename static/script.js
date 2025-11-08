document.getElementById("imageUpload").addEventListener("change", function (event) {
  const file = event.target.files[0];
  const preview = document.getElementById("previewImg");

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    preview.style.display = "none";
  }
});

document.getElementById("predictBtn").addEventListener("click", async function () {
  const dataset = document.getElementById("dataset").value;
  const fileInput = document.getElementById("imageUpload").files[0];

  if (!fileInput) {
    alert("Please upload an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput);
  formData.append("dataset", dataset);

  try {
    const response = await fetch("/predict", {  // 👈 changed to relative URL
      method: "POST",
      body: formData
    });

    const data = await response.json();
    document.getElementById("output").innerText = 
      data.prediction 
        ? `Prediction: ${data.prediction}` 
        : `Prediction: ${data.class} (Confidence: ${(data.confidence * 100).toFixed(2)}%)`;
  } catch (err) {
    console.error(err);
    document.getElementById("output").innerText = "Error: Could not get prediction.";
  }
});
