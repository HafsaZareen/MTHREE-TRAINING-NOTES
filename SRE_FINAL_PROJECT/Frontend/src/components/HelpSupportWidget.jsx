import { useState, useRef, useEffect } from 'react';
import { Card, Form, Button, ListGroup, Modal } from 'react-bootstrap';
import { FaQuestionCircle, FaTimes, FaSearch, FaPaperPlane } from 'react-icons/fa';
import '../styles/Components.css';

const HelpSupportWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showNewQuestionModal, setShowNewQuestionModal] = useState(false);
  const [newQuestion, setNewQuestion] = useState('');
  const [filteredQuestions, setFilteredQuestions] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const widgetRef = useRef(null);



  const handleSubmitQuestion = async (e) => {
    e.preventDefault();
    setMessage('');
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/support', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: newQuestion })
      });

      const data = await response.json();
      setMessage(data.message || 'Question submitted successfully!');
      setNewQuestion('');
      setShowNewQuestionModal(false);
    } catch (error) {
      setMessage(error.message || 'Error submitting question');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
};

  // Sample FAQ data - you can replace this with your actual FAQ data
  const faqData = [
    {
      question: "What is IPC Nexus?",
      answer: "IPC Nexus is a comprehensive platform for exploring and understanding the Indian Penal Code sections, filing complaints, and accessing legal information."
    },
    {
      question: "How do I search for IPC sections?",
      answer: "You can search for IPC sections using the search bar in the Learn IPC section. You can search by section number or keywords related to the offense."
    },
    {
      question: "How do I file a complaint?",
      answer: "You can file a complaint by navigating to the File Complaint section and filling out the complaint form with the required details."
    },
    {
      question: "Can I track my complaint status?",
      answer: "Yes, you can track your complaint status in the Complaint History section after filing a complaint."
    }
  ];

  // Law data from law_data.json
  const lawData = {
    "How can I register a complaint?": "You can register a complaint at the nearest police station or through the online FIR portal.",
    "What is IPC and CRPC?": "IPC (Indian Penal Code) defines criminal laws, while CRPC (Code of Criminal Procedure) provides the procedures for criminal trials.",
    "Where can I find laws related to theft?": "You can refer to Sections 378 to 404 of the IPC, which cover theft and related offenses. Check the 'Laws Section' for more details.",
    "How can this site help a police officer?": "It provides a step-by-step guide for filing FIRs, recommending applicable laws based on the nature of the complaint.",
    "What is an FIR?": "An FIR (First Information Report) is a formal document filed by the police when they receive information about a cognizable offense.",
    "How can I learn about case laws?": "Explore the 'Learn About Case Laws' section to access summaries and analyses of landmark judgments.",
    "Can I practice law using this site?": "Law students can practice by analyzing case laws, understanding legal scenarios, and drafting FIR reports using the simulator.",
    "What are my rights if I am arrested?": "You have the right to remain silent, the right to legal counsel, and the right to be informed of the charges against you.",
    "What is a cognizable and non-cognizable offense?": "In a cognizable offense, the police can arrest without prior approval. For non-cognizable offenses, they need permission from a magistrate.",
    "How can I check which law applies to my complaint?": "Use the 'Register Complaint' feature to receive suggestions for applicable IPC or CRPC sections.",
    "What should I do if I witness a crime?": "Report it immediately to the nearest police station or call 112 for emergency assistance.",
    "Can I get legal advice here?": "This site provides legal information, not legal advice. For legal representation, consult a licensed advocate.",
    "How do I know my constitutional rights?": "Explore the 'Know Your Rights' section to understand your fundamental and legal rights.",
    "Where can I find legal resources for case studies?": "Check the 'Learn About Case Laws' section to access real-life judgments and case studies.",
    "Can I report a cybercrime using this site?": "While this site offers guidance on cyber laws, you need to report cybercrimes through the official Cyber Crime Portal.",
    "What is a bailable and non-bailable offense?": "In a bailable offense, bail is granted as a matter of right. In non-bailable offenses, the court decides whether to grant bail.",
    "Can I report corruption?": "You can report corruption to the Central Vigilance Commission (CVC) or the Anti-Corruption Bureau (ACB).",
    "How can I stay updated on legal news?": "Visit legal news portals like Live Law or Bar & Bench for updates on judgments and amendments.",
    "What are the rights of a victim in a criminal case?": "Victims have the right to legal aid, protection, and compensation under victim protection laws.",
    "What happens after an FIR is filed?": "The police investigate the case, collect evidence, and file a charge sheet in court if necessary.",
    "How can I connect with legal experts?": "You can contact legal professionals through the Bar Council directory or legal aid organizations.",
    "Can I download legal documents from this site?": "The site provides legal information, summaries, and sample documents, but official documents must be obtained through e-Courts or legal portals.",
    "How do I report a missing person?": "File a missing person report at the nearest police station. Provide recent photographs and any other relevant details.",
    "What is the punishment for theft?": "Theft is punishable under Section 378 of the IPC, with imprisonment or fine depending on the severity.",
    "How can I know if a law is applicable in my case?": "Use the 'Register Complaint' feature for a personalized suggestion of applicable laws.",
    "How can I report domestic violence?": "You can report domestic violence to the police or contact the National Domestic Violence Helpline at 181.",
    "What is a charge sheet?": "A charge sheet is a formal document submitted by the police to the court after completing their investigation.",
    "How can I suggest improvements to this site?": "You can submit your feedback through the 'Contact Us' section.",
    "Can I get updates on famous case judgments?": "Yes, check the 'Learn About Case Laws' section for recent and landmark case updates.",
    "What is the purpose of this website?": "The site assists police officers in filing FIRs, helps students study legal cases, and educates the public about laws and rights.",
    "How can I apply for bail?": "To apply for bail, file a bail application in the appropriate court through your legal representative.",
    "Can I access court judgments through this site?": "This site provides case summaries. For complete judgments, visit the official e-Courts portal.",
    "Can I register an anonymous complaint?": "While FIRs generally require personal details, you can submit anonymous complaints through helpline numbers for specific crimes like corruption or trafficking.",
    "How long does it take to investigate a case?": "The time for investigation varies based on the complexity of the case and evidence collection.",
    "What is a non-cognizable report (NCR)?": "An NCR is filed for minor offenses where the police cannot investigate without the magistrate's approval.",
    "What is the difference between a summons case and a warrant case?": "Summons cases involve less severe offenses, while warrant cases are for more serious crimes requiring stricter legal procedures.",
    "How can I report child abuse?": "Report child abuse to the police or contact the Childline Helpline at 1098.",
    "What are fundamental rights?": "Fundamental rights include the right to equality, freedom, protection against discrimination, and protection of life and liberty.",
    "What is anticipatory bail?": "Anticipatory bail is a pre-arrest legal provision that allows a person to apply for bail in anticipation of arrest.",
    "Can I report financial fraud?": "Yes, financial fraud can be reported to the nearest cybercrime police station or through the Cyber Crime Portal.",
    "What is a plea bargain?": "Plea bargaining is a legal provision where the accused pleads guilty for a lesser sentence or reduced charges.",
    "How can I contact legal aid services?": "You can reach out to the Legal Services Authority in your district for free legal assistance if eligible.",
    "How can I track my complaint status?": "You can track your complaint status using the FIR number on the online portal or by visiting the concerned police station.",
    "Where can I learn about my legal rights?": "You can learn about your rights in the 'Know Your Rights' section. It provides clear and simplified explanations of your legal rights.",
    "How can police officers file an FIR using this site?": "Police officers can navigate to the 'Register Complaint' section for guided assistance in filing an FIR with the applicable laws.",
    "Where can I find information about case laws?": "You can explore the 'Learn About Case Laws' section, which contains information on important legal case studies and judgments.",
    "How do I contact support?": "Visit the 'Contact Us' section for support. You can write to us via email or reach out through our social media handles.",
    "Can I search for laws by category?": "Yes, the 'Laws Section' categorizes laws based on their nature, such as crime, robbery, theft, and more. Simply select a category to find relevant information.",
    "How can I track the status of a registered complaint?": "Currently, complaint tracking is not available directly on the site. Please contact the respective authorities for updates on your complaint.",
    "Where can students practice and study laws?": "Students can access the 'Learn About Case Laws' section for case studies and practical learning materials.",
    "What resources are available for legal awareness?": "You can visit the 'Know Your Rights' section for legal resources that explain your rights and responsibilities in simple terms.",
    "How can I navigate back to the homepage?": "You can return to the homepage by clicking on the 'IPC Nexus' logo at the top left corner of any page."
  };

  // Convert law data to the same format as faqData
  const lawDataFormatted = Object.entries(lawData).map(([question, answer]) => ({
    question,
    answer
  }));

  // Combine both FAQ and law data
  const allQuestions = [...faqData, ...lawDataFormatted];

  useEffect(() => {
    setFilteredQuestions(allQuestions);
  }, []);

  useEffect(() => {
    const filtered = allQuestions.filter(q => 
      q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.answer.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredQuestions(filtered);
  }, [searchQuery]);



  return (
    <>
      <div 
        ref={widgetRef}
        className="help-support-widget"
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1000
        }}
      >
        <Button
          variant="primary"
          className="rounded-circle p-3 shadow-sm"
          onClick={() => setIsOpen(!isOpen)}
          style={{
            width: '60px',
            height: '60px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <FaQuestionCircle size={24} />
        </Button>
      </div>

      {isOpen && (
        <Card 
          className="help-support-card shadow-lg"
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '350px',
            maxHeight: '500px',
            zIndex: 1000
          }}
        >
          <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center">
            <h5 className="mb-0">Help & Support</h5>
            <Button 
              variant="link" 
              className="text-white p-0"
              onClick={() => setIsOpen(false)}
            >
              <FaTimes />
            </Button>
          </Card.Header>
          <Card.Body className="p-0">
            <div className="p-3 border-bottom">
              <Form.Control
                type="text"
                placeholder="Search for help..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="mb-2"
              />
              <Button 
                variant="outline-primary" 
                className="w-100"
                onClick={() => setShowNewQuestionModal(true)}
              >
                Ask a New Question
              </Button>
            </div>
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              <ListGroup variant="flush">
                {filteredQuestions.map((faq, index) => (
                  <ListGroup.Item key={index} className="border-bottom">
                    <div className="fw-semibold mb-1">{faq.question}</div>
                    <div className="text-muted small">{faq.answer}</div>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </div>
          </Card.Body>
        </Card>
      )}

      <Modal show={showNewQuestionModal} onHide={() => setShowNewQuestionModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Ask a New Question</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Your Question</Form.Label>
              <Form.Control
                as="textarea"
                rows={4}
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
                placeholder="Type your question here..."
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowNewQuestionModal(false)}>
            Cancel
          </Button>
          <Button 
            variant="primary" 
            onClick={handleSubmitQuestion}
            disabled={!newQuestion.trim()}
          >
            <FaPaperPlane className="me-2" />
            Submit
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default HelpSupportWidget; 