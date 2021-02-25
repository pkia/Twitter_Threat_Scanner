form = document.getElementById("unfollow_form").addEventListener("submit", function (event) {
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

form1 = document.getElementById("mute_form").addEventListener("submit", function (event) {
    event.preventDefault();
    muteUser();
})

function muteUser() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            button = document.getElementById("bttn").innerHTML = xhttp.responseText;
        }
    }

    xhttp.open("POST", "/mute_user", true);
    xhttp.send();
}

form2 = document.getElementById("block_form").addEventListener("submit", function (event) {
    event.preventDefault();
    blockUser();
})

function blockUser() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            button = document.getElementById("bttn").innerHTML = xhttp.responseText;
        }
    }

    xhttp.open("POST", "/block_user", true);
    xhttp.send();
}

function showLoader() {
    let siteIcon = document.querySelector(".navbar-brand");
    let loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    siteIcon.replaceWith(loaderDiv);
    
}
