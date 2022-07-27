const closeBtn = document.querySelector(".alert .btn-close");

if (closeBtn) {
    closeBtn.addEventListener("click", () => {
        const alertDiv = document.querySelector(".alert");
        alertDiv.remove();
    });
}

const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

const pageTitle = document.querySelector("title").textContent;
const homeLink = document.querySelector(".nav-link[href='/']");
const aboutLink = document.querySelector(".nav-link[href='/about']");

if (pageTitle === "Homepage") {
  aboutLink.classList.remove("active");
  homeLink.classList.add("active");
} else if (pageTitle === "About") {
  homeLink.classList.remove("active");
  aboutLink.classList.add("active");
}