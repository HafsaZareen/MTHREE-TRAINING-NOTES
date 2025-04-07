import React, { useState } from "react";
import axios from "axios";
import "../styles/Components.css";

const CrimeSearch = () => {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) {
            setError("Please enter a search term");
            return;
        }
        setError("");
        setLoading(true);

        try {
            const response = await axios.post("http://127.0.0.1:5000/nlp/search", 
                { query },
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true
                }
            );
            setResults(response.data);
            if (response.data.length === 0) {
                setError("No results found");
            }
        } catch (err) {
            console.error("Search error:", err);
            if (err.code === 'ECONNREFUSED') {
                setError("Search service is not running. Please try again later.");
            } else {
                setError(err.response?.data?.error || "Error fetching data. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    return (
        <div className="search-section">
            <div className="search-box">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Search IPC sections..."
                    className="search-input"
                />
                <button onClick={handleSearch} className="search-button">
                    Search
                </button>
            </div>
            
            {loading && <div className="loading">Searching...</div>}
            {error && <div className="error-message">{error}</div>}

            {results.length > 0 && (
                <div className="results-container">
                    {results.map((result, index) => (
                        <div key={index} className="result-card">
                            <div className="section-number">Section {result.Section}</div>
                            <div className="offense">{result.Offense}</div>
                            <div className="punishment">{result.Punishment}</div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default CrimeSearch;

