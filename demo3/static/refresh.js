/*                                                  *
*                                                   *
*   JS used in .html to fix invalid post requests   *
*                                                   *
*                                                   */

/* Source: https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState */
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
