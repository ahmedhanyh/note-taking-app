const closeBtn = document.querySelector(".alert .btn-close");
closeBtn.addEventListener("click", () => {
    const alertDiv = document.querySelector(".alert");
    alertDiv.remove();
});