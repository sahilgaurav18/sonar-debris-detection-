import { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [detections, setDetections] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (!file) return
    setSelectedFile(file)
    setPreviewUrl(URL.createObjectURL(file))
    setDetections(null)
    setError(null)
  }

  const handleUploadAndDetect = async () => {
    if (!selectedFile) return
    setLoading(true)
    setError(null)

    try {
      // Step 1: upload the image
      const formData = new FormData()
      formData.append('file', selectedFile)
      const uploadRes = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      const fileId = uploadRes.data.file_id

      // Step 2: run detection (currently returns dummy data from backend)
      const detectRes = await axios.get(`${API_BASE}/detect/${fileId}`)
      setDetections(detectRes.data.detections)
    } catch (err) {
      setError('Something went wrong. Is the backend running on port 8000?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
      <h1 className="text-2xl font-bold mb-6">Sonar Debris Detection</h1>

      <div className="bg-slate-800 rounded-lg p-6 max-w-xl">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="block mb-4 text-sm"
        />

        {previewUrl && (
          <img
            src={previewUrl}
            alt="Sonar preview"
            className="max-w-full rounded mb-4 border border-slate-600"
          />
        )}

        <button
          onClick={handleUploadAndDetect}
          disabled={!selectedFile || loading}
          className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 px-4 py-2 rounded font-medium"
        >
          {loading ? 'Processing...' : 'Upload & Detect'}
        </button>

        {error && <p className="text-red-400 mt-4">{error}</p>}

        {detections && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Detections</h2>
            <ul className="space-y-2">
              {detections.map((d) => (
                <li
                  key={d.object_id}
                  className="bg-slate-700 rounded p-3 text-sm"
                >
                  <span className="font-medium capitalize">{d.type.replace('_', ' ')}</span>
                  {' — '}
                  {(d.confidence * 100).toFixed(0)}% confidence, size {d.estimated_size_m}m
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
