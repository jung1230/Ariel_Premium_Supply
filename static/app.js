/*
static files = things like JS, CSS, images, and fonts.
They're called "static" because:
    They are sent exactly as they are.
    The server doesn't modify or render them.
    They don’t depend on user input before being served.
While dynamic files are generated on the fly by the server, like
HTML, PHP, etc. 
*/

// request access to the live camera(pending)
// navigator.mediaDevices.getUserMedia({video: true }) // this is a promise // this works for windows
navigator.mediaDevices.getUserMedia({video: { facingMode: "environment" }}) // this is a promise // this works for mobile
// fulfilled promise(returns CameraView, and it will be a video stream)
.then(function(CameraView){ //function is like def in python
    const video = document.getElementById('UserView');
    //stream the video
    video.srcObject = CameraView;

    const button = document.getElementById('UserButton');

    //if the button is clicked
    button.addEventListener('click', function(){
        const canvas = document.getElementById('UserPhoto');
        const OutputText = document.getElementById('apiOutput');
        const Instructions = document.getElementById('Instructions');
        const image1 = document.getElementById('1stImg');
        const image2 = document.getElementById('2ndImg');
        const image3 = document.getElementById('3rdImg');

        // draw the video on the canvas and save it
        const context = canvas.getContext('2d');

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        // convert the canvas to a data URL
        const dataURL = canvas.toDataURL('image/png');  //change the image format to png(default is jpeg)
    
        // fetch the data URL and send it to the server
        fetch("/upload", {                  // this is also a promise!!!!
            method: "POST", // POST = send data
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({image: dataURL})
        })
        // get the response from the server
        .then(function(response){
            return response.json() // this is also a promise
        })
        .then(function(data){
            if(data[0].score == -1){
                Instructions.innerHTML = "Although the logo is not found in the database, it may still be a registered trademark. Please verify based on your best judgment.";
                OutputText.innerHTML = "No logos found in the database. Please double check if this logo is registered trademark.";
                image1.src = "";
                image2.src = "";
                image3.src = "";
            }
            else{
                // // loop through the data and get the description and score
                // for (let i = 0; i < data.length; i++){
                //     output.push("Brand:"+data[i].description + "  Probability:" + data[i].score);
                // }
                Instructions.innerHTML = "Below are three reference images of the detected brand logo("+ data[0].description+"). Logos may vary in style, so even if they don't match exactly, they may still represent the same brand. Please verify based on your best judgment.";
                OutputText.innerHTML = "Brand Logo Detected!<br>Brand:"+data[0].description + "<br>Probability:" + (data[0].score * 100).toFixed(2) + "%";
                image1.src = data[0].image[0].link;
                image2.src = data[0].image[1].link;
                image3.src = data[0].image[2].link;
            }

        })
    }, false);
}) 
// rejected promise(returns an error)
.catch(function(error){
    alert(error);
})
