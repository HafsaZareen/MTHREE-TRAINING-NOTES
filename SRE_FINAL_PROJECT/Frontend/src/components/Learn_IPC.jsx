import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Components.css';

const Learn_IPC = () => {
    const [searchTerm, setSearchTerm] = useState('');
  const [sections, setSections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

  useEffect(() => {
        fetchSections();
  }, []);

    const fetchSections = async () => {
        try {
            setLoading(true);
            const response = await axios.post('http://localhost:5000/nlp/search', {
                query: ''
            });
            setSections(response.data);
            setError(null);
        } catch (err) {
            console.error('Error fetching IPC sections:', err);
            setError('Failed to load IPC sections. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!searchTerm.trim()) {
            fetchSections();
            return;
        }

        try {
            setLoading(true);
            const response = await axios.post('http://localhost:5000/nlp/search', {
                query: searchTerm
            });
            setSections(response.data);
            setError(null);
        } catch (err) {
            console.error('Error searching IPC sections:', err);
            setError('Failed to search IPC sections. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    const filteredSections = sections.filter(section =>
        section.Section.toLowerCase().includes(searchTerm.toLowerCase()) ||
        section.Offense.toLowerCase().includes(searchTerm.toLowerCase()) ||
        section.Punishment.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
        <div className="ipc-learn-container">
            <h1 className="ipc-learn-title">Learn About IPC Sections</h1>
            <div className="ipc-search-box">
      <input
        type="text"
                    className="ipc-search-input"
                    placeholder="Search by section number, offense, or punishment..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
            </div>
            {loading ? (
                <div className="ipc-loading">Loading IPC sections...</div>
            ) : error ? (
                <div className="ipc-no-results">{error}</div>
            ) : (
                <div className="ipc-table-container">
                    <table className="ipc-table">
        <thead>
                            <tr>
                                <th>Section</th>
                                <th>Offense</th>
                                <th>Punishment</th>
          </tr>
        </thead>
        <tbody>
                            {filteredSections.map((section, index) => (
                                <tr key={index} className="ipc-table-row">
                                    <td className="section-cell">
                                        <span className="section-badge">Section {section.Section}</span>
              </td>
                                    <td className="offense-cell">{section.Offense}</td>
                                    <td className="punishment-cell">{section.Punishment}</td>
            </tr>
          ))}
        </tbody>
      </table>
                </div>
            )}
            {!loading && !error && filteredSections.length === 0 && (
                <div className="ipc-no-results">
                    No sections found matching your search.
                </div>
            )}
    </div>
  );
};

export default Learn_IPC;
