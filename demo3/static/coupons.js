function checkbox(dates) {
    var cb = document.getElementsByName("indefinite");
    var visability = "flex";
      if(cb[0].checked){
       visability = "none";
      }

    document.getElementById(dates).style.display = visability;
}
