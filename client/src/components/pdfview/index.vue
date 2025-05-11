<template>
    <div class="pdf-wrap">
      <!-- pdf控制按钮区域 -->
      <div class="pdf-control">
        <button @click="prev">上一页</button>
        <input
          type="number"
          class="page-number-input"
          v-model="pageNum"
          min="1"
          :max="pageCount"
          @blur="queueRenderPage(pageNum)"
        />
        <span class="page-num"> / {{ pageCount }}页</span>
        <button @click="next">下一页</button>
        <button @click="minus">缩小</button>
        <button @click="addscale">放大</button>
        <input class="pdf-choose" type="file" name="选择pdf文件" id="pdfChoose" @change="pdfChange">
      </div>
      <!-- pdf文件内容渲染区域 -->
      <div class="pdf-content" id="pdfContent"></div>
    </div>
  </template>
  <script>
  export default {
    data() {
      return {
        pdfJs: null, // 加载的pdfjs
        pdfDoc: null, // pdfjs读取的页面信息
        pageNum: 0, // 当前页数
        pageCount: 0, // 总页数
        pageRendering: false, // 当前页面是否在渲染中
        pageNumPending: null, // 将要进行渲染的页面页数
        scale: 1, // 放大倍数
        maxscale: 5, // 最大放大倍数
        minscale: 0.3, // 最小放大倍数
        domWaterMarkCanvas: document.createElement('canvas'), // 水印canvas元素
        waterInfo: {
          enable: true,
          name: 'hero',
          userAccount: 'company',
          time: '2021-10-25',
        }, // 水印信息
      };
    },
    created() {
      // 若开启，则创建水印模板
      if (this.waterInfo.enable) this.createWatermarkTemplate();
    },
    methods: {
      pdfChange(e) {
        /**
         * 上传pdf文件，并转为pdfjs可用的文件数据格式
         */
        const fileReader = new FileReader()
        fileReader.readAsDataURL(e.target.files[0])
        fileReader.onload = fileLoaded => this.loadPdfJs(fileLoaded.target.result);
      },
      loadPdfJs(pdfResource) {
        /**
         * pdfjs加载
         */
        if (this.pdfJs) {
          this.getDocument(pdfResource)
        } else {
          // 引入pdfjs，或以同步方式const pdfJs = require('pdfjs-dist')
          import('pdfjs-dist')
            .then((pdfJs) => {
              this.pdfJs = pdfJs
              // 注意：应该始终设置`workerSrc`选项，以防止发生操作使PDF.js库出现问题，该选项为一个包含工作文件的路径和文件名的字符串
              pdfJs.GlobalWorkerOptions.workerSrc = `${process.env.PATH_PREFIX}/js/pdf.worker.min.js`;
              this.getDocument(pdfResource)
            });
        }
      },
      getDocument(pdfResource) {
        /**
         * 读取pdf文件资源
         */
        this.pdfJs.getDocument(pdfResource)
          .promise.then((pdfDoc) => {
            this.pageNum = 1;
            this.pdfDoc = pdfDoc;
            this.pageCount = pdfDoc.numPages;
            this.renderPage(this.pageNum);
          });
      },
      renderPage(num) {
        /**
         * 渲染pdf指定页面
         */
        this.pageRendering = true;
        this.pdfDoc.getPage(num)
          .then((page) => {
            // 获取当前pdf页面信息
            const viewport = page.getViewport({ scale: this.scale });
            // 创建供当前pdf页面渲染的canvas元素
            const canvas = document.createElement('canvas');
            // 使用获取到的pdf信息，给canvas元素设定宽高
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            // 设定canvas元素样式信息
            canvas.setAttribute('style', 'margin: 0 auto;')
            const ctx = canvas.getContext('2d');
            // 若不使用水印，则需加上这段代码
            // ctx.fillStyle = 'rgba(255, 255, 255, 0)';
            // 进行水印的重复渲染
            ctx.fillStyle = ctx.createPattern(this.domWaterMarkCanvas, 'repeat');
            // 将pdf信息和水印信息渲染到canvas画布上
            page.render({ canvasContext: ctx, viewport })
              .promise.then(() => {
                // 画布进行实际的绘制
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                // 若当前页面已经存在已渲染的pdf画布dom，则移除
                const domCanvas = document.querySelector('canvas')
                const domPdfContent = document.querySelector('#pdfContent')
                if (domCanvas) domPdfContent.removeChild(domCanvas)
                // 将绘制好的canvas插入到页面dom中
                domPdfContent.appendChild(canvas)
                this.pageRendering = false;
                // 若当前有还未渲染的下一页，则渲染下一页
                if (this.pageNumPending !== null) {
                  this.renderPage(this.pageNumPending);
                  this.pageNumPending = null;
                }
              });
          });
      },
      createWatermarkTemplate() {
        /**
         * 创建水印模板
         */
        // 水印宽高，与pdf缩放比例同步变化
        const width = 250 * this.scale;
        const height = 250 * this.scale;
        this.domWaterMarkCanvas.width = width;
        this.domWaterMarkCanvas.height = height;
        const ctx = this.domWaterMarkCanvas.getContext('2d'); // 返回一个用于在画布上绘图的环境
        ctx.scale(this.scale, this.scale);
        // 绘制之前画布清除
        ctx.clearRect(0, 0, width, height);
        // 逆时针旋转30度
        ctx.rotate((-30 * Math.PI) / 180);
        // 设置canvas画布样式
        ctx.fillStyle = 'rgba(100,100,100,0.1)';
        ctx.font = '24px 黑体';
        // 设置canvas画布文字
        ctx.fillText(`${this.waterInfo.name} ${this.waterInfo.userAccount}`, -10, 130);
        ctx.fillText(this.waterInfo.time, -10, 160);
        // 坐标系还原
        ctx.rotate((30*Math.PI) / 180);
      },
      addscale() {
        /**
         * 放大
         */
        if (this.scale >= this.maxscale) {
          return;
        }
        this.scale += 0.1;
        this.queueRenderPage(this.pageNum);
      },
      minus() {
        /**
         * 缩小
         */
        if (this.scale <= this.minscale) {
          return;
        }
        this.scale -= 0.1;
        this.queueRenderPage(this.pageNum);
      },
      prev() {
        /**
         * 上一页
         */
        if (this.pageNum <= 1) {
          return;
        }
        this.pageNum--;
        this.queueRenderPage(this.pageNum);
      },
      next() {
        /**
         * 下一页
         */
        if (this.pageNum >= this.pageCount) {
          return;
        }
        this.pageNum++;
        this.queueRenderPage(this.pageNum);
      },
      queueRenderPage(num) {
        /**
         * 渲染页面队列
         */
        if (this.waterInfo.enable) this.createWatermarkTemplate();
        const number = Number(num);
        if (this.pageRendering) {
          this.pageNumPending = number;
        } else {
          this.renderPage(number);
        }
      },
    },
  };
</script>
<style lang="less" scoped>
.pdf-wrap {
  height: 100vh;
  .pdf-control {
    height: 50px;
    padding: 0px 16px;
    background: rgba(103, 103, 103, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    .page-number-input {
      width: 50px;
      border: none;
      border-radius: 2px;
      padding: 2px 4px;
    }
    .page-num {
      color: white;
    }
    button {
      margin: 0 10px;
      cursor: pointer;
    }
    .pdf-choose {
      margin-left: 100px  ;
      color: white;
    }
  }
  .pdf-content {
    height: calc(100vh - 50px);
    overflow-y: auto;
    background-color: rgba(0, 0, 0, 0.2);
  }
}
</style>
  