console.log("script.js loaded");

function predict() {

    

    let fileInput = document.getElementById("imageInput");

    if (fileInput.files.length === 0) {
        alert("Please select an image first.");
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("image", file);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML = `
            <h3>Disease: ${data.disease}</h3>
            <p>Accuracy: ${data.accuracy}%</p>
            <p>Treatment: ${data.treatment}</p>
        `;
    })
    .catch(err => {
        alert("Fetch error");
        console.log(err);
    });
}