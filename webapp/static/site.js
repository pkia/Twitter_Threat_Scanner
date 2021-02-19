function showLoader() {
    let siteIcon = document.querySelector(".navbar-brand");
    let loaderDiv = document.createElement("div");
    loaderDiv.className = "loader";
    siteIcon.replaceWith(loaderDiv);
    
}