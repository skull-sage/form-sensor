import JotsIndex from "./jots/index.vue"
import HomeIndex from "./home/index.vue"
import RecordingIndex from "./snap-jots/index.vue"
import ARecording from "./snap-jots/a-recording/index.vue"
import PlayBookIndex from "./index.vue"
import {RouteRecordRaw} from "vue-router";


const routeConfig: RouteRecordRaw =  {
  path: '/playbook',
  name: 'playbook',
  component: PlayBookIndex,
  children: [
    {
      path: '',
      component: HomeIndex,
      name: 'playbook.index',
    },
    {
      path: 'jots',
      name: 'playbook.jots',
      component: JotsIndex,
    },
    {
      path: 'recording-list',
      name: 'playbook.recording-list',
      component: RecordingIndex,
    },
    {
      path: 'a-recording/:recordingId',
      name: 'playbook.a-recording',
      component: ARecording,
      props: true,
    },



  ]
}

export  default  routeConfig;
