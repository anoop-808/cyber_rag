import React, { useState } from 'react';
import AskForm from '../components/AskForm';
import AnswerCard from '../components/AnswerCard';
import { askCyberRAG } from '../services/api';

const Ask: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [answerData, setAnswerData] = useState<any>(null);

    const handleAsk = async (query: string) => {
        setLoading(true);
        setError(null);
        setAnswerData(null); // Clear previous answer

        try {
            const data = await askCyberRAG(query);
            setAnswerData(data);
        } catch (err: any) {
            // Handle errors gracefully as per requirements
            let errorMessage = 'An unexpected error occurred. Please try again.';
            if (err.response) {
                if (err.response.status === 422) {
                    errorMessage = 'Validation error: Please ensure your question is formatted correctly.';
                } else if (err.response.status >= 500) {
                    errorMessage = 'Backend error: The server encountered an issue while processing your request.';
                } else {
                    errorMessage = `Error: ${err.response.data?.detail || err.message}`;
                }
            } else if (err.request) {
                errorMessage = 'Network error: Unable to contact the server. Please check your connection.';
            }

            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="ask-page" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h1>Ask CyberRAG</h1>
            </header>

            <main>
                <AskForm onAsk={handleAsk} loading={loading} />

                {loading && (
                    <div className="loading" style={{ marginTop: '1rem' }}>
                        Generating answer...
                    </div>
                )}

                {error && (
                    <div className="error" style={{ color: 'red', marginTop: '1rem' }}>
                        {error}
                    </div>
                )}

                {!loading && !error && !answerData && (
                    <div className="empty-state" style={{ marginTop: '2rem', fontStyle: 'italic', color: '#666' }}>
                        Ask CyberRAG anything about CVEs.
                    </div>
                )}

                {answerData && !loading && (
                    <AnswerCard
                        answer={answerData.answer}
                        sources={answerData.sources || []}
                        confidence={answerData.confidence}
                    />
                )}
            </main>
        </div>
    );
};

export default Ask;
