/*                                                  *
*                                                   *
*              JS used in base.html                 *
*                                                   *
*                                                   */

function dropdown_menu(show, hide) {
  document.getElementById(hide).classList.toggle("show", false);
  document.getElementById(show).classList.toggle("show");
}

function dropdown_mobile_menu(show) {
  document.getElementById(show).classList.toggle("show");
}
