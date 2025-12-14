<template>
  <a-section class="q-py-md">
    <div class="row col-gutter-sm">
          <div class="col-md-8">
            <div>Hello there! Welcome to incident report system</div>
            <div v-if="feedback.data == undefined">What is new ?</div>
            <div v-else class="q-mt-sm">
                <div class="q-mb-md">Logged incident titled as: {{ feedback.title }}</div>
                <TransitionGroup name="list" tag="div"
                      @before-enter="followupVisible = false" @after-enter="followupVisible = true">
                  <div v-for="(change, index) in feedback.changeList" :key="change">
                    <div>New relevant info according to my understanding</div>
                    <ul><li v-for="(val, key) in change" :key="key"><b>{{ key }}</b>: {{ change[key] }}</li></ul>
                  </div>
                </TransitionGroup>

                <Transition appear enter-active-class="animated fadeIn">
                  <div v-if="followupVisible || feedback.changeList.length == 1" class="q-mt-md">{{ feedback.data.followup_question }}</div>
                </Transition>

            </div>
            <div class="full-width q-mt-sm">
              <input type="text-area" v-model="req_data.text"
                @keyup.enter="tryInput"
                class="full-width" style="border: 1px solid lightblue;"
                placeholder="start typing..." />
            </div>
          </div>
          <div class="col-md-4">
            <div></div>
          </div>
        </div>
</a-section>
</template>
<script setup lang="ts">
import axios from 'axios'
import { Session } from 'inspector/promises';
import { onMounted, reactive, ref } from 'vue';


const followupVisible = ref(false)
const feedback = reactive({changeList: [], data: undefined, title: undefined})
const error = ref(null)

const req_data = {
  Session_id: "rashed-"+new Date().toISOString(),
  text: "Server down in EU region"
}


let changeSerial = 0
const onAiResponse = (resData)=>{

  ++changeSerial
  let oldExt = feedback.data ? feedback.data.extracted_fields : {}
  let newExt = resData.extracted_fields
  let changeDelta = {}

  for(const key in newExt) {
      if (oldExt[key] == undefined) {
        changeDelta[key] = newExt[key]
      } else if (oldExt[key] != newExt[key]) {
        changeDelta[key] = newExt[key]
      }
  }

  if (newExt.title != undefined){
    feedback.title = newExt.title
  }

  feedback.changeList.push(changeDelta)
  feedback.data = resData

  req_data.text = ""
}

const tryInput = async ()=> {

      try {
        const response = await axios.post('http://localhost:8000/api/v1/nlp/ai-extract', req_data);
        onAiResponse(response.data)
      } catch (err) {
        error.value = 'Failed to fetch data: ' + err.message;
      }
}
</script>
<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
