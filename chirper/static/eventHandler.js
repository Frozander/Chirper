let deleteButton = document.getElementById("delete");
deleteButton.addEventListener("click", (e) => {
    if (!confirm("Are you sure?")) {
        e.preventDefault();
    }
})