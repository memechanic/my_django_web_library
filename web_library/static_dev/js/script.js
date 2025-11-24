document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".clickable-row").forEach(row => {
        row.style.cursor = "pointer";
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href;
        });
    });
    const toast = document.getElementById("myToast")
    const bToast = bootstrap.Toast.getOrCreateInstance(toast)
    bToast.show()
});