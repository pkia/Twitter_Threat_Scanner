
form = document.getElementById("form").addEventListener("submit", function (event) {
    event.preventDefault();
    unfollowUser();
})

function unfollowUser() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            button = document.getElementById("bttn").innerHTML = xhttp.responseText;
        }
    }

    xhttp.open("POST", "/unfollow_user", true);
    xhttp.send();
}

function showLoader() {
    let siteIcon = document.querySelector(".navbar-brand");
    let loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    siteIcon.replaceWith(loaderDiv);
    
}

