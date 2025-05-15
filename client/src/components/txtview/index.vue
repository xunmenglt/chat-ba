<template>
    <div class="app-container">
      <div class="file-title">{{ file_name }}</div>
      <div class="text-viewer">
        {{ text }}
      </div>
    </div>
  </template>
  
  
  <script>
  import { getTxtContent } from '@/utils/api/file';
  export default {
      props:{
          file_name:{
              type:String,
              default:""
          },
          factory_name:{
              type:String,
              default:""
          }
      },
      data() {
          return {
            text:"暂无内容"
          }
      },
      created(){
          this.initTxTList()
      },
      methods:{
          initTxTList(){
              if(this.file_name){
                console.log('sadljsak')
                  this.$modal.loading("正在加载文件")
                  getTxtContent({
                      file_name:this.file_name,
                      factory_name:this.factory_name
                  }).then(res=>{
                    
                      if(res && res.code && res.code===200){
                          this.text=res.data
                      }
                  }).finally(()=>{
                      this.$modal.closeLoading()
                  })
              }
          }
      },
  
      watch:{
          file_name(newVal){
              this.initTxTList()
          }
      }
  }
  </script>
  
  <style lang="less" scoped>
  .file-title {
  margin-bottom: 5px;
  font-weight: 900;
  font-size: 16px;
}

.text-viewer {
  white-space: pre-wrap;       /* 保留换行符 */
  overflow-wrap: break-word;
  word-break: break-word;
  font-weight: 600;            /* 加粗但不过重 */
  font-size: 14px;
  line-height: 1.6;
  background-color: #f9f9f9;   /* 淡背景提升可读性 */
  padding: 10px;
  border-radius: 6px;
  color: #333;
}

  </style>