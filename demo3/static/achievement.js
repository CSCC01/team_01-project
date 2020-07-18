function checkbox(requireFee, requireItem) {
    var cb = document.getElementsByName("Item");
    var visability = "flex";
    var countervisability = "none";
      if(cb[0].checked){
        countervisability = visability;
        visability = "none";
      }
    document.getElementById(requireFee).style.display = visability;
    document.getElementById(requireItem).style.display = countervisability;
}
