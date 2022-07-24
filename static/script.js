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