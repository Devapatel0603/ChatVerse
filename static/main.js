let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};  

var form = document.getElementById('sheetdb-form');	  
form.addEventListener('submit', e => {
  e.preventDefault();
  fetch(form.action, { 
    method: 'POST',
    body: new FormData(document.getElementById("sheetdb-form")),
}).then(
    response => alert("Thank you! your message send successfully." )
    ).then((html) => {  
        window.location.reload(); 
    })
})
