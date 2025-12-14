import {computed, reactive, ref} from 'vue'
import {format} from 'quasar'
import { RecorderCallbacks, RecorderState, RuntimeState } from './screen-recorder'
import ScreenRecorder from './screen-recorder'
import RecordingStore from '@/app-main/playbook/snap-jots/a-recording/recording-store'
import { useRouter } from 'vue-router'

export default function useRecorder(stream:MediaStream){
  const state:RecorderState = reactive({
    runtimeState: RuntimeState.NOT_STARTED,
    totalWatchTime: 0, // this is according to video object
    chunkList: [],
    totalRecordedBytes: 0,
  })


  const router = useRouter()
  const callbacks:RecorderCallbacks = {
    onStart(){
      state.runtimeState = RuntimeState.RECORDING;

    },
    async onStop(){
      state.runtimeState = RuntimeState.STOPPED;
      const newId = RecordingStore.insert(state.chunkList, undefined);
      //route to recorded video playback
      await router.push({ name: 'playbook.a-recording', params: {'recordingId':newId} });

    },
    onPause(){
      state.runtimeState = RuntimeState.PAUSED;
    },
    onResume(){
      state.runtimeState = RuntimeState.RECORDING;
    },
    onNextChunk(blob:Blob){
      state.chunkList.push(blob);
      state.totalRecordedBytes += blob.size;
    }
  }

  const recorder = new ScreenRecorder(stream, 10,  callbacks);

  return {
    state,
    recorder
  }

}
