document.getElementById("type").addEventListener('change', function (e) {
  if (e.target.value === "0") {
    document.getElementById("type0").style.display = "flex";
    document.getElementById("type1").style.display = "none";
    document.getElementById("type2").style.display = "none";
    document.getElementById("type3").style.display = "none";
  } if (e.target.value === "1") {
    document.getElementById("type0").style.display = "none";
    document.getElementById("type1").style.display = "flex";
    document.getElementById("type2").style.display = "none";
    document.getElementById("type3").style.display = "none";
  } if (e.target.value === "2") {
    document.getElementById("type0").style.display = "none";
    document.getElementById("type1").style.display = "none";
    document.getElementById("type2").style.display = "flex";
    document.getElementById("type3").style.display = "none";
  } if (e.target.value === "3") {
    document.getElementById("type0").style.display = "none";
    document.getElementById("type1").style.display = "none";
    document.getElementById("type2").style.display = "none";
    document.getElementById("type3").style.display = "flex";
    document.getElementById("type3").style.flexDirection = "column";
  }
});

function checkbox(dates) {
    var cb = document.getElementsByName("indefinite");
    var visability = "flex";
      if(cb[0].checked){
       visability = "none";
      }

    document.getElementById(dates).style.display = visability;
}
