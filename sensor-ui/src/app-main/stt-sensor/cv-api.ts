
import { ref } from 'vue';
import axios from 'axios';


/**
 * Function to analyze audio and return a transcription
 * @param audioBlob - The recorded audio blob
 * @returns {transcribed, score}
 */


const api = axios.create({ baseURL: 'http://localhost:8000' });

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
    query: "Kindly, introduce yourself.",
    expected: 'With 10+years of experience, working as a technical lead helping business with scalable and affordable solutions',
    lead: 'Nice!',
    eval: { ans: undefined, score: 0 }
  },
  {
    id: 2,
    query: "Please describe your most recent work experience relevant to this role",
    eval: { ans: undefined, score: 0 },
    expected: 'developed enterprise knowledge hub with RAG pipeline and LLM',
    lead: 'Great! Thank you so much for your time. Our HR will be in contact with you soon, preferabely within a week or so.',
  },
]


export default {
  qIdx: ref(0),
  analyzeAudio: async function (audioBlob: Blob) {
    // Create FormData and append the audio file and expected text
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    // Get expected text from current question
    const currentQuestion = this.currentQ();
    const expectedText = currentQuestion?.expected || '';
    formData.append('expected', expectedText);

    try {
      // Make POST request to the analyze-stt endpoint
      const response = await api.post('/cv/analyze-stt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Update current question's eval with response data
      if (currentQuestion?.eval) {
        currentQuestion.eval.ans = response.data.transcribed;
        currentQuestion.eval.score = response.data.similarity;
      }

      if (!this.isLastQ()) {
        setTimeout(() => this.qIdx.value++, 2000);
      }


    } catch (error) {
      console.error('Error analyzing audio:', error);
      throw error;
    }
  },
  currentQ: function () {
    return dummyQ[this.qIdx.value]
  },
  isLastQ: function () {
    return this.qIdx.value === dummyQ.length - 1
  }
}
