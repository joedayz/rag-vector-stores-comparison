import { useState } from "react";
import axios from "axios";
import "./App.css";

interface AFPResponse {
  answer: string;
  question: string;
}

function App() {
  const [question, setQuestion] = useState<string>("");
  const [response, setResponse] = useState<AFPResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const result = await axios.post<AFPResponse>("http://localhost:8000/afp-query", {
        question: question.trim()
      });
      setResponse(result.data);
    } catch (err) {
      setError("Error al procesar la consulta. Por favor, inténtalo de nuevo.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const exampleQuestions = [
    "¿Cuál es el procedimiento para el cuarto retiro de AFP?",
    "¿Hasta cuándo tengo para retirar mi cuarto retiro?",
    "¿Qué documentos necesito para el cuarto retiro?",
    "¿Cuánto dinero puedo retirar en el cuarto retiro?",
    "¿Cómo solicito mi cuarto retiro de AFP?"
  ];

  return (
    <div className="app">
      <header className="header">
        <h1>🏦 Consultas AFP - Cuarto Retiro</h1>
        <p>Obtén información sobre el procedimiento y plazos del cuarto retiro de AFP</p>
      </header>

      <main className="main">
        <div className="chat-container">
          <form onSubmit={handleSubmit} className="question-form">
            <div className="input-group">
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Escribe tu pregunta sobre el cuarto retiro de AFP..."
                className="question-input"
                rows={3}
                disabled={loading}
              />
              <button 
                type="submit" 
                className="submit-button"
                disabled={loading || !question.trim()}
              >
                {loading ? "Consultando..." : "Consultar"}
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          {response && (
            <div className="response-container">
              <div className="question-display">
                <strong>Tu pregunta:</strong> {response.question}
              </div>
              <div className="answer-display">
                <strong>Respuesta:</strong>
                <div className="answer-content">
                  {response.answer.split('\n').map((line, index) => (
                    <p key={index}>{line}</p>
                  ))}
                </div>
              </div>
            </div>
          )}

          <div className="examples">
            <h3>💡 Preguntas de ejemplo:</h3>
            <div className="example-questions">
              {exampleQuestions.map((example, index) => (
                <button
                  key={index}
                  className="example-button"
                  onClick={() => setQuestion(example)}
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>
          ℹ️ Esta información es de carácter general. Para consultas específicas, 
          contacta directamente con tu AFP o la Superintendencia de Pensiones.
        </p>
      </footer>
    </div>
  );
}

export default App;
