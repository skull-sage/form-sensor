import katex from "katex";

export const inlineMathHtml = (mathLatex) => {
  return katex.renderToString(mathLatex, {
    throwOnError: false
  });
}
export const blockMathHtml = (mathLatex) =>{

  return katex.renderToString(mathLatex, {
    fleqn: true,
    strict: "ignore",
    displayMode : true,
    throwOnError: false
  });
}
