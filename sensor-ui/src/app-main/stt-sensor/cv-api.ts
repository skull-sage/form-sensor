import axios from 'axios';

/**
 * Function to analyze audio and return a transcription
 * @param audioBlob - The recorded audio blob
 * @param question - The question being asked
 * @returns Object containing transcribed text
 */

import { ref } from 'vue';

const dummyQ = [
  { id: 0, query: "how have you been today ?", lead: 'Thank you for applying to this role' },
  { id: 1, query: "Kindly, introduce yourself" },
  { id: 2, query: "Please describe your most recent work experience" },
  { id: 3, query: "Why do you think you are a good fit for this role?" },
]


export default {
  qIdx: ref(0),
  analyzeAudio: async function (audioBlob: Blob, question: string) {
    // Create FormData and append the audio file
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    try {
      // Make POST request to the analyze-stt endpoint
      // const response = await axios.post('/cv/analyze-stt', formData, {
      //   headers: {
      //     'Content-Type': 'multipart/form-data',
      //   },
      // });

      this.qIdx.value++
      return { text: 'Hello', score: 1 }
      // Return the transcribed text from the response
      //return response.data;
    } catch (error) {
      console.error('Error analyzing audio:', error);
      throw error;
    }
  },
  currentQ: function () {
    return dummyQ[this.qIdx.value]
  }
}
