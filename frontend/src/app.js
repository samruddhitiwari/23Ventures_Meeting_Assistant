import { useState } from 'react';

function App() {
  const [text, setText] = useState('');
  const [summary, setSummary] = useState('');

  const handleSummarize = async () => {
    const res = await fetch('https://your-backend-url/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    setSummary(data.summary || 'No summary returned.');
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Summarizer</h1>
      <textarea
        className="w-full p-2 border rounded"
        rows={6}
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Paste your text here..."
      />
      <button
        onClick={handleSummarize}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
      >
        Summarize
      </button>
      {summary && (
        <div className="mt-4 bg-gray-100 p-4 rounded">
          <h2 className="font-semibold">Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
