const inputs = document.querySelectorAll('input[type=file]');

for(i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("change", (e)=> {
        
        let photoWrap = document.getElementById('photo-wrap');
        const curFiles = e.target.files;

        if (curFiles.length !== 0) {
            for (const file of curFiles) {
                if (validFileType(file)) {
                    while(photoWrap.firstChild) {
                        photoWrap.removeChild(photoWrap.firstChild);
                    }

                    const image = document.createElement('img');
                    image.src = URL.createObjectURL(file);               
                    photoWrap.appendChild(image);
                }                
            }
        }
    });
}

const fileTypes = [
    "image/apng",
    "image/bmp",
    "image/gif",
    "image/jpeg",
    "image/pjpeg",
    "image/png",
    "image/svg+xml",
    "image/tiff",
    "image/webp",
    "image/x-icon"
];
  
function validFileType(file) {
return fileTypes.includes(file.type);
}
