// Example: Log a message when the page loads
document.addEventListener("DOMContentLoaded", () => {
    console.log("Page loaded successfully!");

    // Example: Highlight the active navigation link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });
});