let slideIndex = 0;

function showSlides() {
    let i;
    const slides = document.getElementsByClassName("mySlides");

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slideIndex++;

    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    slides[slideIndex - 1].style.display = "block";
    setTimeout(showSlides, 2000); // Change slide every 2 seconds (adjust as needed)
}

document.addEventListener("DOMContentLoaded", function () {
    const slideshowContainer = document.querySelector(".slideshow-container");

    const imageFilenames = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg", "image6.jpg", "image7.jpg", "image8.jpg", "image9.jpg", "image10.jpg"];

    imageFilenames.forEach((filename) => {
        const slide = document.createElement("div");
        slide.className = "mySlides";
        slide.style.backgroundImage = `url('../static/images/${filename}')`;
        slideshowContainer.appendChild(slide);
    });

    showSlides(); // Start the slideshow
});