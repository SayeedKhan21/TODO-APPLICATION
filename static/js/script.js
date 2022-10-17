rem_button = document.getElementsByClassName("remove")[0]
successdiv = document.getElementsByClassName("success-message")[0]
rem_button.addEventListener("click" ,myfunction)
window.addEventListener("load" ,myfunction)


function myfunction(){
    successdiv.style.display = none ;
}