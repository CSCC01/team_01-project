/*                                                  *
*                                                   *
*   JS used in .html to fix invalid post requests   *
*                                                   *
*                                                   */

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
