import {applicationContext} from '@/utils/resources.js'

let server_url = applicationContext.protocol+"://"+applicationContext.host+':'+applicationContext.port+applicationContext.prefix

export async function readChatbotReply(
  url,
  data = {},
  readCallback=(first, text)=>{},
  endCallback=()=>{},
  onStart=(controller)=>{},
  onError=(e)=>{}
) {
  const controller = new AbortController()
  const { signal } = controller
  try{
    const fetch_url = server_url + url
    // fetch操作内容
    const fetchOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify(data),
      signal: controller.signal
    }
    // 开始fetch请求
    const response = await fetch(fetch_url, fetchOptions)
    // 判断是否成功建立连接
    if (!response.ok) {
      throw new Error(`Server responded with status code: ${response.status}`)
    }
    // 判断是否有可读流
    if (!response.body) {
      throw new Error('Failed to get a ReadableStream from the response')
    }
    onStart(controller)
    let buffer = ''
    let first = true;
    const readableStream = response.body
          .pipeThrough(new TextDecoderStream())
          .pipeThrough(new TransformStream({
            start() {
              buffer = ''
            },
            // 运输流
            transform(chunk) {
              buffer += chunk
              let position
              while ((position = buffer.indexOf('\r\n\r\n')) !== -1) {
                const line = buffer.substring(0, position)
                buffer = buffer.substring(position + 4)
                readCallback(first, line);
              }
              first=false
            },
            flush() {
              if (buffer) {
                try {
                  readCallback(first, buffer);
                } catch (e) {
                  onError(new Error('Error parsing JSON data from event'))
                }
              }
            }
          }))
    const reader = readableStream.getReader();
    while (true) {
      if (signal.aborted) break
      const { done } = await reader.read()
      if (done) break
    }
    controller.abort()
    reader.releaseLock()
  }catch(error){
    controller.abort()
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        endCallback()
      } else {
        console.error('Fetch error:', error)
      }
    }
  }finally{
    endCallback()
  }
}
