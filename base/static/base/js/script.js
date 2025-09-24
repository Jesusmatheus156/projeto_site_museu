document.addEventListener("DOMContentLoaded", () => {
    const menuBtn = document.querySelector(".menu-btn");
    const menuLinks = document.querySelector(".navbar-nav");

    menuBtn.addEventListener("click", () => {
        menuLinks.classList.toggle("active");
    });
});

let slideIndex = 0;
const slides = document.querySelectorAll('.carrossel-seta img');

function showSlide() {
    slides.forEach(slide => slide.style.display = 'none');
    slides[slideIndex].style.display = 'block';
}

function moveSlide(n) {
    slideIndex += n;

    if (slideIndex >= slides.length) slideIndex = 0;
    if (slideIndex < 0) slideIndex = slides.length - 1;

    showSlide();
}

document.addEventListener('DOMContentLoaded', () => {
    showSlide();
});