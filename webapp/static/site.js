// showLoader function replaces the Twitter bird with the loading icon when a new page needs to load
function showLoader() {
    let siteIcon = document.querySelector(".navbar-brand");
    let loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    siteIcon.replaceWith(loaderDiv);
    
}

// modifyDom function is used by the scan results pagination to replace the tweets displayed when a new page button is pressed
function modifyDom(num, tweets) {
    let tweetElements = document.querySelectorAll(".tweet p");
    let tweetContainers = document.querySelectorAll(".tweet");
    for (let container of tweetContainers) {
        container.style.display = "none"
    }
    let tweetArray = tweets["tweet-" + num.toString()]["array"];
    let arrayLength = tweets["tweet-" + num.toString()]["length"];
    for (i=0; i<arrayLength; i++) {
        tweetContainers[i].style.display = "block";
        tweetElements[i].innerText = tweetArray[i][1];
    }
}