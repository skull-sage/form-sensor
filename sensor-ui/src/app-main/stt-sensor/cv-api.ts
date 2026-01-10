import axios from 'axios';

/**
 * Function to analyze audio and return a transcription
 * @param audioBlob - The recorded audio blob
 * @param question - The question being asked
 * @returns Object containing transcribed text
 */


const dummyQ = [
  { id: 1, query: "how have you been today ?", lead: 'Thank you for applying to this role' },
  { id: 2, query: "Kindly, introduce yourself" },
  { id: 3, query: "Please describe your most recent work experience" },
  { id: 4, query: "Why do you think you are a good fit for this role?" },
]


export default {
  qIdx: 0,
  analyzeAudio: async function (audioBlob: Blob, question: string) {
    // Create FormData and append the audio file
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    try {
      // Make POST request to the analyze-stt endpoint
      const response = await axios.post('/cv/analyze-stt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      this.qIdx++
      // Return the transcribed text from the response
      return response.data;
    } catch (error) {
      console.error('Error analyzing audio:', error);
      throw error;
    }
  },
  currentQ: function () {
    return dummyQ[this.qIdx]
  }
}
