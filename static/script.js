const closeBtn = document.querySelector(".alert .btn-close");

if (closeBtn) {
    closeBtn.addEventListener("click", () => {
        const alertDiv = document.querySelector(".alert");
        alertDiv.remove();
    });
}
