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
navigator.mediaDevices.getUserMedia({ video: true })
// fulfilled promise(returns CameraView, and it will be a video stream)
.then(function(CameraView){ //function is like def in python
    const video = document.getElementById('UserView');
    //stream the video
    video.srcObject = CameraView;

    const button = document.getElementById('UserButton');
    const canvas = document.getElementById('UserPhoto');
    //if the button is clicked
    button.addEventListener('click', function(){
        // draw the video on the canvas and save it
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        // convert the canvas to a data URL
        const dataURL = canvas.toDataURL('image/png');  //change the image format to png(default is jpeg)
    
        // fetch the data URL and send it to the server
        fetch("/upload", {
            method: "POST", // send data
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: dataURL})
        })
    }, false);
}) 
// rejected promise(returns an error)
.catch(function(error){
    alert(error);
})
