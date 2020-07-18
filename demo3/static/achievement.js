function checkbox(Item) {
    var cb = document.getElementsByName("Item");
    var visability = "flex";
      if(cb[0].checked){
       visability = "none";
      }

    document.getElementById(Item).style.display = visability;
}
