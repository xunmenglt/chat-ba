import html2Canvas from "html2canvas";
import { jsPDF } from "jspdf";

// pdfDom 页面dom , intervalHeight 留白间距  fileName 文件名
export function html2Pdf(pdfDom, intervalHeight, fileName) {
  // 获取元素的高度
  function getElementHeight(element) {
    return element.offsetHeight;
  }

  // A4 纸宽高
  const A4_WIDTH = 592.28,
    A4_HEIGHT = 841.89;
  // 获取元素去除滚动条的高度
  const domScrollHeight = pdfDom.scrollHeight;
  const domScrollWidth = pdfDom.scrollWidth;

  // 保存当前页的已使用高度
  let currentPageHeight = 0;
  // 获取所有的元素  我这儿是手动给页面添加class 用于计算高度 你也可以动态添加 这个不重要，主要是看逻辑
  let elements = pdfDom.querySelectorAll(".element");
  // 代表不可被分页
  let newPage = "new-page";

  // 遍历所有内容的高度
  for (let element of elements) {
    let elementHeight = getElementHeight(element);
    console.log(elementHeight, "我是页面上的elementHeight"); // 检查
    // 检查添加这个元素后的总高度是否超过 A4 纸的高度
    if (currentPageHeight + elementHeight > A4_HEIGHT) {
      // 如果超过了，创建一个新的页面，并将这个元素添加到新的页面上
      currentPageHeight = elementHeight;
      element.classList.add(newPage);
      console.log(element, "我是相加高度大于A4纸的元素");
    }
    currentPageHeight += elementHeight;
  }
  // 根据 A4 的宽高等比计算 dom 页面对应的高度
  const pageWidth = pdfDom.offsetWidth;
  const pageHeight = (pageWidth / A4_WIDTH) * A4_HEIGHT;
  // 将所有不允许被截断的子元素进行处理
  const wholeNodes = pdfDom.querySelectorAll(`.${newPage}`);
  console.log(wholeNodes, "将所有不允许被截断的子元素进行处理");
  // 插入空白块的总高度
  let allEmptyNodeHeight = 0;
  for (let i = 0; i < wholeNodes.length; i++) {
    // 判断当前的不可分页元素是否在两页显示
    const topPageNum = Math.ceil(wholeNodes[i].offsetTop / pageHeight);
    const bottomPageNum = Math.ceil(
      (wholeNodes[i].offsetTop + wholeNodes[i].offsetHeight) / pageHeight
    );

    // 是否被截断
    if (topPageNum !== bottomPageNum) {
      // 创建间距
      const newBlock = document.createElement("div");
      newBlock.className = "empty-node";
      newBlock.style.background = "#fff";

      // 计算空白块的高度，可以适当留出空间，根据自己需求而定
      const _H = topPageNum * pageHeight - wholeNodes[i].offsetTop;
      newBlock.style.height = _H + intervalHeight + "px";

      // 插入空白块
      wholeNodes[i].parentNode.insertBefore(newBlock, wholeNodes[i]);

      // 更新插入空白块的总高度
      allEmptyNodeHeight = allEmptyNodeHeight + _H + intervalHeight;
    }
  }
  pdfDom.setAttribute(
    "style",
    `height: ${
      domScrollHeight + allEmptyNodeHeight
    }px; width: ${domScrollWidth}px;`
  );
  return html2Canvas(pdfDom, {
    width: pdfDom.offsetWidth,
    height: pdfDom.offsetHeight,
    useCORS: true,
    allowTaint: true,
    scale: 3,
   }).then(canvas => {
     
     
     // dom 已经转换为 canvas 对象，可以将插入的空白块删除了
    const emptyNodes = pdfDom.querySelectorAll('.empty-node');
    
      for (let i = 0; i < emptyNodes.length; i++) {
      emptyNodes[i].style.height = 0;
      emptyNodes[i].parentNode.removeChild(emptyNodes[i]);
    }
    
     const canvasWidth = canvas.width,canvasHeight = canvas.height;
     // html 页面实际高度
     let htmlHeight = canvasHeight;
     // 页面偏移量
    let position = 0;
   
    // 根据 A4 的宽高等比计算 pdf 页面对应的高度
    const pageHeight = (canvasWidth / A4_WIDTH) * A4_HEIGHT;
   
    // html 页面生成的 canvas 在 pdf 中图片的宽高
    const imgWidth = A4_WIDTH;
    const imgHeight = 592.28 / canvasWidth * canvasHeight
    // 将图片转为 base64 格式
    const imageData = canvas.toDataURL('image/jpeg', 1.0);
    
    // 生成 pdf 实例
    
     const PDF = new jsPDF('', 'pt', 'a4', true) 
    
     // html 页面的实际高度小于生成 pdf 的页面高度时，即内容未超过 pdf 一页显示的范围，无需分页
    if (htmlHeight <= pageHeight) {
    
      PDF.addImage(imageData, 'JPEG', 0, 0, imgWidth, imgHeight);
      
    } else {
        
      while (htmlHeight > 0) {
      PDF.addImage(imageData, 'JPEG', 0, position, imgWidth, imgHeight);
   
      // 更新高度与偏移量
      htmlHeight -= pageHeight;
      position -= A4_HEIGHT;
   
      if (htmlHeight > 0) {
       // 在 PDF 文档中添加新页面
       PDF.addPage();
       }
     }
    
    }
     // 保存 pdf 文件
    PDF.save(`${fileName}.pdf`);
   }).catch(err => {
    console.log(err);
   }
   );
    
    
   })
}

   
   
   