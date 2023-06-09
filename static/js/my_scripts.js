//To select a calendar period and call the New Event Form


// To manage the Select All button in events list
document.addEventListener("DOMContentLoaded", function() {
    var checkAllButton = document.getElementById("checkallbtn");
    var isChecked = false;
    var deleteAllButton = document.getElementById("deleteallbtn");

    checkAllButton.addEventListener("click", function() {
        var checkboxes = document.getElementsByName("event_check");
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = !isChecked;
        }

        if (isChecked) {
            checkAllButton.classList.remove("btn-secondary");
            checkAllButton.classList.add("btn-outline-secondary");
        } else {
            checkAllButton.classList.remove("btn-outline-secondary");
            checkAllButton.classList.add("btn-secondary");
        }

        isChecked = !isChecked;
    });

    deleteAllButton.addEventListener("click", function() {
        checkAllButton.classList.remove("btn-secondary");
        checkAllButton.classList.add("btn-outline-secondary");
    })
});
