import Vue from 'vue'

export const showTextMessage=(type,content)=>{
    const option= {
        position: "top-center",
        timeout: 2000,
        closeOnClick: true,
        pauseOnFocusLoss: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: true,
        hideProgressBar: true,
        closeButton: false,
        icon: true,
        rtl: false
    }
    if(type==='success'){
        Vue.$toast.success(content,option)
    }else if(type==='info'){
        Vue.$toast.info(content,option)
    }else if(type==='warning'){
        Vue.$toast.warning(content,option)
    }else if(type==='error'){
        Vue.$toast.error(content,option)
    }else{
        Vue.$toast(content,option)
    }
}