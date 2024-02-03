//Menu Toggle
let toggle = document.querySelector('.stf-toggle');
let navigation = document.querySelector('.stf-navigation');
let main = document.querySelector('.stf-main');

toggle.onclick = function() {
    navigation.classList.toggle('active');
    main.classList.toggle('active');
}

let list = document.querySelectorAll('.stf-navigation li');
function activeLink(){
    list.forEach((item) =>
    item.classList.remove('hovered'));
}
list.forEach((item) =>
item.addEventListener('mouseover', activeLink));

let arrow = document.querySelectorAll(".arrow");
  for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e)=>{
   let arrowParent = e.target.parentElement.parentElement;//selecting main parent of arrow
   arrowParent.classList.toggle("showMenu");
    });
  }

var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("drop_active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}