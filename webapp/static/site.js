function showLoader() {
    let siteIcon = document.querySelector(".navbar-brand");
    let loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    siteIcon.replaceWith(loaderDiv);
    
}

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