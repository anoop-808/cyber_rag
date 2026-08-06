import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CVEInfoCard from '../components/CVEInfoCard';
import Layout from '../components/Layout';

const CVEDetail: React.FC = () => {
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
        return (
            <Layout>
                <div className="error-state">
                    <p>No CVE ID provided.</p>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="cve-detail-page-content">
                <div className="page-header">
                    <h1>CVE Details</h1>
                </div>
                <CVEInfoCard cveId={id} onBack={handleBack} />
            </div>
        </Layout>
    );
};

export default CVEDetail;
