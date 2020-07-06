/*var modal = document.getElementById("deletion");

// Get the button that opens the modal
var btn = document.getElementById("delete");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var options = document.getElementById('{{ e.email }}');
var settings = document.getElementById("settings");
settings.onclick = function() {
  options.style.display = "block";
}

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


function dropdown(val) {
  var options = document.getElementById(val);
  options.style.display = "block";
}*/

var dat = JSON.parse('{{ target | tojson }}');

function setMessage() {
    document.getElementById("message").innerHTML = dat;
}
