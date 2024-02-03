// Get the navbar
var topnav = document.getElementById("topnav");

//// Get the offset position of the navbar
//var sticky = topnav.offsetTop;
//
//// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
//function myFunction() {
//  if (window.pageYOffset >= sticky) {
//    topnav.classList.add("sticky")
//  } else {
//    topnav.classList.remove("sticky");
//  }
//}
window.onscroll = function() {myFunction()};

let navbar = document.querySelector('.navbar');
document.querySelector('#menu-bar').onclick = () =>{
    navbar.classList.toggle('active');
}
document.querySelector('#close').onclick = () =>{
    navbar.classList.remove('active');
}

let navbar2 = document.querySelector('.navbar2');
document.querySelector('#menu-bar2').onclick = () =>{
    navbar2.classList.toggle('active');
}
document.querySelector('#close2').onclick = () =>{
    navbar2.classList.remove('active');
}



