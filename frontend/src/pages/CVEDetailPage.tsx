import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CVEDetail from '../components/CVEDetail';

const CVEDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const handleBack = () => {
        // Navigate back to the previous page in history, or to /search
        if (window.history.length > 2) {
            navigate(-1);
        } else {
            navigate('/search');
        }
    };

    if (!id) {
        return <div className="error">No CVE ID provided.</div>;
    }

    return (
        <div className="cve-detail-page">
            <header>
                <h1>CVE Details</h1>
            </header>
            <main>
                <CVEDetail cveId={id} onBack={handleBack} />
            </main>
        </div>
    );
};

export default CVEDetailPage;
