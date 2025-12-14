export function htmlStrToDom(htmlStr$){

  var template = document.createElement('template');
    let  html = htmlStr$.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content;

}

export function calcScreenSize() {
  let win = window,
    doc = document,
    docElem = doc.documentElement,
    body = doc.getElementsByTagName('body')[0];

   let width = win.innerWidth || docElem.clientWidth || body.clientWidth;
   let height = win.innerHeight|| docElem.clientHeight|| body.clientHeight;

    return {width, height}
}

/**
 *  a helper function to calculate width height and positions in a single pass
 *  offsetWidth, offsetHeight, clientWidth, clientHeight, rectWidth, rectHeight
 *  top, bottom, left, right
 *  All in pixel
 *
 * */
export function calcElmBox(elm$) {
  let style = elm$.currentStyle || window.getComputedStyle(elm$);
  let domRect = elm$.getBoundingClientRect();
  let pageXOffset = window.scrollX;
  let pageYOffset = window.scrollY;

  return {
    marginTop : parseFloat(style.marginTop),
    marginBottom: parseFloat(style.marginBottom),
    marginLeft : parseFloat(style.marginLeft),
    marginRight : parseFloat(style.marginRight),

    paddingTop: parseFloat(style.paddingTop),
    paddingBottom: parseFloat(style.paddingBottom),
    paddingLeft: parseFloat(style.paddingLeft),
    paddingRight: parseFloat(style.paddingRight),

    borderTop : parseFloat(style.borderTopWidth),
    borderBottom : parseFloat(style.borderBottomWidth),
    borderLeft : parseFloat(style.borderLeftWidth),
    borderRight : parseFloat(style.borderRightWidth),

    offsetWidth : elm$.offsetWidth,
    offsetHeight: elm$.offsetHeight,
    clientWidth: elm$.clientWidth,
    clientHeight: elm$.clientHeight,
    scrollWidth: elm$.scrollWidth,
    scrollHeight: elm$.scrollHeight,
    rectWidth: domRect.width,
    rectHeight: domRect.height,
    compWidth: style.width,
    compHeight: style.height,

    top: domRect.top,
    bottom: domRect.bottom,
    left: domRect.left,
    right: domRect.right,
    docTop: domRect.top + pageYOffset,
    docLeft: domRect.left + pageXOffset

  };

}


