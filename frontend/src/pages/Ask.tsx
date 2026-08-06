import React, { useState } from 'react';
import AskForm from '../components/AskForm';
import AnswerCard from '../components/AnswerCard';
import Layout from '../components/Layout';
import { PageHeader, LoadingState, ErrorState, EmptyState } from '../components/ui';
import { useToast } from '../components/ui/toast-context';
import { QuestionIcon } from '../components/icons';
import { askCyberRAG } from '../services/api';

const Ask: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [answerData, setAnswerData] = useState<any>(null);
    const [lastQuery, setLastQuery] = useState('');
    const { showToast } = useToast();

    const handleAsk = async (query: string) => {
        setLastQuery(query);
        setLoading(true);
        setError(null);
        setAnswerData(null); // Clear previous answer

        try {
            const data = await askCyberRAG(query);
            setAnswerData(data);
            showToast('Answer generated');
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
            showToast('Request failed', 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div className="ask-page-content">
                <PageHeader
                    title="Ask CyberRAG"
                    subtitle="Get AI-powered answers about cybersecurity vulnerabilities."
                />

                <AskForm onAsk={handleAsk} loading={loading} />

                {loading && (
                    <LoadingState label="Generating answer..." />
                )}

                {error && (
                    <ErrorState
                        message={error}
                        onRetry={() => lastQuery && handleAsk(lastQuery)}
                    />
                )}

                {!loading && !error && !answerData && (
                    <EmptyState
                        title="Ready when you are"
                        message="Ask a cybersecurity question to get a grounded, source-backed answer."
                        icon={<QuestionIcon />}
                    />
                )}

                {answerData && !loading && (
                    <AnswerCard
                        answer={answerData.answer}
                        sources={answerData.sources || []}
                        metadata={answerData.metadata || []}
                        confidence={answerData.confidence}
                    />
                )}
            </div>
        </Layout>
    );
};

export default Ask;
