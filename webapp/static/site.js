function showLoader() {
    let siteIcon = document.querySelector(".navbar-brand");
    let loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    siteIcon.replaceWith(loaderDiv);
    
}

function modifyDom(num, tweets) {
    let tweetElements = document.querySelectorAll(".tweet p");
    let tweetArray = tweets["tweet-" + num.toString()]["array"];
    let arrayLength = tweets["tweet-" + num.toString()]["length"];
    for (i=0; i<arrayLength; i++) {
        tweetElements[i].innerText = tweetArray[i][1][1];
    }
}