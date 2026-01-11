import axios from 'axios';

/**
 * Function to analyze audio and return a transcription
 * @param audioBlob - The recorded audio blob
 * @param question - The question being asked
 * @returns Object containing transcribed text
 */

import { ref } from 'vue';

const dummyQ = [
  {
    id: 0,
    query: "how have you been today ?",
    expected: 'I am fine thank you.',
    lead: 'Great to know! Thank you for applying to this role',
    eval: { ans: undefined, score: 0 }
  },
  {
    id: 1,
    query: "Kindly, introduce yourself",
    expected: 'working as a technical lead helping business with scalable and affordable technolo solutions',
    lead: 'Nice!',
    eval: { ans: undefined, score: 0 }
  },
  { id: 2, query: "Please describe your most recent work experience" },
  { id: 3, query: "Why do you think you are a good fit for this role?" },
]


export default {
  qIdx: ref(0),
  analyzeAudio: async function (audioBlob: Blob) {
    // Create FormData and append the audio file
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    try {
      // Make POST request to the analyze-stt endpoint
      const response = await axios.post('/cv/analyze-stt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      this.currentQ.answer = response.data.text
      // Return the transcribed text from the response
      return { text: response.data.text, score: 1 };
    } catch (error) {
      console.error('Error analyzing audio:', error);
      throw error;
    }
  },
  moveToNext: function () {
    this.qIdx.value++
  },
  currentQ: function () {
    return dummyQ[this.qIdx.value]
  }
}
