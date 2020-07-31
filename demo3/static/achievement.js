document.getElementById("type").addEventListener('change', function (e) {
  if (e.target.value === "0") {
    document.getElementById("type0").style.display = "flex";
    document.getElementById("type1").style.display = "none";
    document.getElementById("type2").style.display = "none";
  } if (e.target.value === "1") {
    document.getElementById("type0").style.display = "none";
    document.getElementById("type1").style.display = "flex";
    document.getElementById("type2").style.display = "none";
  } if (e.target.value === "2") {
    document.getElementById("type0").style.display = "none";
    document.getElementById("type1").style.display = "none";
    document.getElementById("type2").style.display = "flex";
  }
});
