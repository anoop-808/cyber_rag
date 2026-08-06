import React, { useState } from 'react';
import AskForm from '../components/AskForm';
import AnswerCard from '../components/AnswerCard';
import Layout from '../components/Layout';
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
                errorMessage = 'Unable to contact the server.';
            }

            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="ask-page-content">
                <div className="page-header">
                    <h1>Ask CyberRAG</h1>
                    <p className="page-description">Get AI-powered answers about cybersecurity vulnerabilities.</p>
                </div>

                <AskForm onAsk={handleAsk} loading={loading} />

                {loading && (
                    <div className="loading-state">
                        <p>Generating answer...</p>
                    </div>
                )}

                {error && (
                    <div className="error-state">
                        <p>{error}</p>
                    </div>
                )}

                {!loading && !error && !answerData && (
                    <div className="empty-state">
                        <p>Ask a cybersecurity question.</p>
                    </div>
                )}

                {answerData && !loading && (
                    <AnswerCard
                        answer={answerData.answer}
                        sources={answerData.sources || []}
                        confidence={answerData.confidence}
                    />
                )}
            </div>
        </Layout>
    );
};

export default Ask;
