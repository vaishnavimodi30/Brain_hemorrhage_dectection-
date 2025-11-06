function uploadImage() {
    let input = document.getElementById("imageUpload");
    let file = input.files[0];

    if (!file) {
        document.getElementById("result").innerText = "Please select an image!";
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerText = "Error: " + data.error;
        } else {
            document.getElementById("result").innerText = "Prediction: " + data.prediction;
        }
    })
    .catch(error => {
        document.getElementById("result").innerText = "Error: " + error.message;
    });
}
