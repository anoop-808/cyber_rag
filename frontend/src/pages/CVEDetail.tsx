import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CVEInfoCard from '../components/CVEInfoCard';
import Layout from '../components/Layout';
import { PageHeader, ErrorState } from '../components/ui';

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
                <ErrorState title="Invalid request" message="No CVE ID provided." />
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="cve-detail-page-content">
                <PageHeader title="CVE Details" />
                <CVEInfoCard cveId={id} onBack={handleBack} />
            </div>
        </Layout>
    );
};

export default CVEDetail;
