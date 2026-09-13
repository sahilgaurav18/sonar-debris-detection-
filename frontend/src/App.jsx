import { useState } from "react";
import { uploadSonarImage, detectSonarImage } from "./api/api";

const BACKEND_URL = "http://127.0.0.1:8000";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [annotatedUrl, setAnnotatedUrl] = useState(null);
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setAnnotatedUrl(null);
    setDetections([]);
    setError(null);
  };

  const handleUploadAndDetect = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      console.log("BUTTON CLICKED");

      const uploadRes = await uploadSonarImage(selectedFile);
      console.log("UPLOAD RESPONSE:", uploadRes);

      const fileId = uploadRes.file_id;

      const detectRes = await detectSonarImage(fileId);
      console.log("FULL DETECTION RESPONSE:", detectRes);

      setDetections(detectRes.detections || []);

      if (detectRes.annotated_image) {
        setAnnotatedUrl(
          `${BACKEND_URL}${detectRes.annotated_image}?t=${Date.now()}`
        );
      } else {
        setError("Annotated image was not returned by the backend.");
      }

    } catch (err) {
      console.error("API ERROR:", err);

      setError(
        err.response?.data?.detail ||
        err.message ||
        "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <h1 className="text-3xl font-bold mb-6">
        Sonar Debris Detection
      </h1>

      <div className="max-w-5xl">

        <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 mb-6">

          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="block mb-4"
          />

          <button
            onClick={handleUploadAndDetect}
            disabled={!selectedFile || loading}
            className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 px-5 py-2 rounded-lg font-medium"
          >
            {loading ? "Processing..." : "Upload & Detect"}
          </button>

          {error && (
            <p className="text-red-400 mt-4">
              {error}
            </p>
          )}

        </div>

        {previewUrl && !annotatedUrl && (
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-4 mb-6">

            <h2 className="text-xl font-semibold mb-4">
              Sonar Image
            </h2>

            <img
              src={previewUrl}
              alt="Original sonar"
              className="w-full h-auto rounded-lg block"
            />

          </div>
        )}

        {annotatedUrl && (
          <div className="bg-slate-900 border border-cyan-700 rounded-xl p-4 mb-6">

            <h2 className="text-xl font-semibold mb-4">
              Detection Analysis
            </h2>

            <img
              src={annotatedUrl}
              alt="YOLO detection result"
              className="w-full h-auto rounded-lg block"
            />

            <p className="text-slate-400 text-sm mt-3">
              Bounding boxes are generated directly by the YOLO model.
            </p>

          </div>
        )}

        {detections.length > 0 && (
          <div className="bg-slate-900 border border-slate-700 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-4">
              Detection Results
            </h2>

            <p className="text-slate-300 mb-4">
              Objects detected: {detections.length}
            </p>

            {detections.map((detection, index) => (
              <div
                key={index}
                className="bg-slate-800 rounded-lg p-4 mb-3"
              >

                <div>
                  <strong>Object:</strong>{" "}
                  {detection.object_type}
                </div>

                <div>
                  <strong>Confidence:</strong>{" "}
                  {(detection.confidence * 100).toFixed(1)}%
                </div>

                <div className="text-slate-300 mt-2">

                  <strong>Bounding Box:</strong>

                  <br />

                  X1: {detection.bbox.x1.toFixed(1)}
                  {" | "}
                  Y1: {detection.bbox.y1.toFixed(1)}
                  {" | "}
                  X2: {detection.bbox.x2.toFixed(1)}
                  {" | "}
                  Y2: {detection.bbox.y2.toFixed(1)}

                </div>

              </div>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default App;
