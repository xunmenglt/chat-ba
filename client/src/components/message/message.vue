<template>
  <div v-highlight>
    <mavon-editor
    class="md"
    boxShadowStyle="0px"
    :value="value"
    :subfield="false"
    :defaultOpen="'preview'"
    :toolbarsFlag="false"
    :editable="false"
    :scrollStyle="true"
    :ishljs="true"
    />
  </div>
</template>

<script>
import {mavonEditor} from 'mavon-editor'
export default {
    components:{mavonEditor},
    props:{
        value:{
            type:String,
            default:"",
        }
    },
}
</script>

<style lang="less" scoped>
/deep/ .v-note-wrapper{
    min-width: 0 !important;
    min-height: 0 !important;
   
    z-index: 0;
}
/deep/ .v-show-content{
    padding: 0 !important;
    background-color: #e0f2ff !important;
    word-break: break-word;
    p{
        margin: 0 !important;
    }
}
</style>