const closeBtn = document.querySelector(".btn-close");
closeBtn.addEventListener("click", () => {
    const alertDiv = document.querySelector(".alert");
    alertDiv.remove();
});