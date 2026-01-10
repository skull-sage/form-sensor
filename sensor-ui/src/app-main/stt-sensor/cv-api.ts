/**
 * Dummy function to analyze audio and return a transcription with a relevance score
 * @param audioBlob - The recorded audio blob
 * @param question - The question being asked
 * @returns Object containing transcribed text and relevance score (0-1)
 */
export async function analyzeAudio(
    audioBlob: Blob,
    question: string
): Promise<{ text: string; score: number }> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Dummy responses based on question keywords
    const dummyResponses = [
        { text: "My day has been great, thank you for asking!", score: 0.85 },
        { text: "I'm a software developer with 5 years of experience in web development.", score: 0.92 },
        { text: "I have worked on several AI projects including machine learning models and natural language processing.", score: 0.88 }
    ];

    // Return a random dummy response
    const randomIndex = Math.floor(Math.random() * dummyResponses.length);
    return dummyResponses[randomIndex];
}
