import { useState } from "react";

import {
  analyzeStory,
  generateStoryAudio,
  generateStoryImages,
  getAudioUrl,
  getImageUrl,
} from "./api/storyApi";

import "./index.css";

const LANGUAGE_CONFIG = {
  en: {
    name: "English (American)",
    voices: [
      { id: "af_heart", name: "Heart", gender: "Female" },
      { id: "af_bella", name: "Bella", gender: "Female" },
      { id: "af_sarah", name: "Sarah", gender: "Female" },
      { id: "af_nicole", name: "Nicole", gender: "Female" },
      { id: "af_sky", name: "Sky", gender: "Female" },
      { id: "am_adam", name: "Adam", gender: "Male" },
    ],
  },

  hi: {
    name: "Hindi",
    voices: [
      { id: "hf_alpha", name: "Alpha", gender: "Female" },
      { id: "hf_beta", name: "Beta", gender: "Female" },
      { id: "hm_omega", name: "Omega", gender: "Male" },
      { id: "hm_psi", name: "Psi", gender: "Male" },
    ],
  },

  fr: {
    name: "French",
    voices: [
      { id: "ff_siwis", name: "Siwis", gender: "Female" },
    ],
  },
};

function App() {
  const [story, setStory] = useState("");

  // Story analysis
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  // Audio
  const [language, setLanguage] = useState("en");
  const [voice, setVoice] = useState("af_heart");
  const [speed, setSpeed] = useState(1);
  const [duration, setDuration] = useState(5);

  const [audioLoading, setAudioLoading] = useState(false);
  const [audioFile, setAudioFile] = useState(null);

  // Images
  const [imageCount, setImageCount] = useState(2);
  const [images, setImages] = useState([]);
  const [imageStoryName, setImageStoryName] = useState(null);
  const [imagesLoading, setImagesLoading] = useState(false);

  // General error
  const [error, setError] = useState("");

  const selectedLanguage = LANGUAGE_CONFIG[language];

  // ----------------------------------------
  // Language change
  // ----------------------------------------

  const handleLanguageChange = (event) => {
    const newLanguage = event.target.value;

    setLanguage(newLanguage);

    // Automatically select the first valid voice
    // for the selected language.
    const firstVoice =
      LANGUAGE_CONFIG[newLanguage].voices[0];

    setVoice(firstVoice.id);
  };

  // ----------------------------------------
  // Analyze Story
  // ----------------------------------------

  const handleAnalyzeStory = async () => {
    if (!story.trim()) {
      setError("Please enter a story.");
      return;
    }

    setAnalyzing(true);
    setError("");
    setAnalysis(null);

    try {
      const result = await analyzeStory(story);

      setAnalysis(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  // ----------------------------------------
  // Generate Audio
  // ----------------------------------------

  const handleGenerateAudio = async () => {
    if (!story.trim()) {
      setError("Please enter a story.");
      return;
    }

    setAudioLoading(true);
    setError("");
    setAudioFile(null);

    try {
      const result = await generateStoryAudio({
        mode: "provided",
        prompt: null,
        story: story,
        duration_minutes: Number(duration),
        language: language,
        voice: voice,
        speed: Number(speed),
      });

      setAudioFile(result.filename);
    } catch (err) {
      setError(err.message);
    } finally {
      setAudioLoading(false);
    }
  };

  // ----------------------------------------
  // Generate Images
  // ----------------------------------------

  const handleGenerateImages = async () => {
    if (!story.trim()) {
      setError("Please enter a story.");
      return;
    }

    setImagesLoading(true);
    setError("");
    setImages([]);
    setImageStoryName(null);

    try {
      const result = await generateStoryImages({
        story: story,
        image_count: Number(imageCount),
      });

      setImages(result.images || []);

      if (result.images?.length > 0) {
        const firstImage = result.images[0];

        const parts = firstImage.split("/");

        // images/{story_name}/{filename}
        if (parts.length >= 3) {
          setImageStoryName(parts[1]);
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setImagesLoading(false);
    }
  };

  return (
    <div className="app">

      {/* -------------------------------- */}
      {/* Header */}
      {/* -------------------------------- */}

      <header className="header">
        <h1>Voice Story AI</h1>

        <p>
          Turn your stories into narration and
          visual content.
        </p>
      </header>

      <main className="workspace">

        {/* -------------------------------- */}
        {/* Story */}
        {/* -------------------------------- */}

        <section className="card">

          <h2>📖 Story</h2>

          <textarea
            value={story}
            onChange={(event) =>
              setStory(event.target.value)
            }
            placeholder="Write or paste your story here..."
            rows={12}
          />

          <button
            onClick={handleAnalyzeStory}
            disabled={analyzing}
          >
            {analyzing
              ? "Analyzing Story..."
              : "Analyze Story"}
          </button>

        </section>

        {/* -------------------------------- */}
        {/* Error */}
        {/* -------------------------------- */}

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {/* -------------------------------- */}
        {/* Story Analysis */}
        {/* -------------------------------- */}

        {analysis && (
          <section className="card">

            <h2>🔍 Story Analysis</h2>

            <div className="analysis-summary">

              <h3>{analysis.title}</h3>

              <p>
                <strong>Genre:</strong>{" "}
                {analysis.genre}
              </p>

              <p>
                <strong>Theme:</strong>{" "}
                {analysis.theme}
              </p>

              <p>
                <strong>Protagonist:</strong>{" "}
                {analysis.protagonist}
              </p>

              <p>
                <strong>Setting:</strong>{" "}
                {analysis.setting}
              </p>

            </div>

            {/* Characters */}

            {analysis.characters?.length > 0 && (
              <div className="analysis-section">

                <h3>Characters</h3>

                {analysis.characters.map(
                  (character, index) => (
                    <div
                      className="character"
                      key={index}
                    >
                      <strong>
                        {character.name}
                      </strong>

                      <p>
                        {character.description}
                      </p>

                      {character.role && (
                        <small>
                          Role: {character.role}
                        </small>
                      )}
                    </div>
                  )
                )}

              </div>
            )}

            {/* Emotional Arc */}

            {analysis.emotional_arc?.length > 0 && (
              <div className="analysis-section">

                <h3>Emotional Arc</h3>

                <p>
                  {analysis.emotional_arc.join(
                    " → "
                  )}
                </p>

              </div>
            )}

            {/* Key Events */}

            {analysis.key_events?.length > 0 && (
              <div className="analysis-section">

                <h3>Key Events</h3>

                <ul>
                  {analysis.key_events.map(
                    (event, index) => (
                      <li key={index}>
                        {event}
                      </li>
                    )
                  )}
                </ul>

              </div>
            )}

            {/* Scenes */}

            {analysis.scenes?.length > 0 && (
              <div className="analysis-section">

                <h3>🎬 Scenes</h3>

                <div className="scenes">

                  {analysis.scenes.map(
                    (scene) => (
                      <div
                        className="scene"
                        key={scene.scene_number}
                      >

                        <h4>
                          Scene{" "}
                          {scene.scene_number}
                        </h4>

                        <p>
                          {scene.description}
                        </p>

                        <p>
                          <strong>
                            Location:
                          </strong>{" "}
                          {scene.location}
                        </p>

                        <p>
                          <strong>
                            Time:
                          </strong>{" "}
                          {scene.time}
                        </p>

                        <p>
                          <strong>
                            Mood:
                          </strong>{" "}
                          {scene.mood}
                        </p>

                        {scene.characters
                          ?.length > 0 && (
                          <p>
                            <strong>
                              Characters:
                            </strong>{" "}
                            {scene.characters.join(
                              ", "
                            )}
                          </p>
                        )}

                        {scene.visual_elements
                          ?.length > 0 && (
                          <div>
                            <strong>
                              Visual Elements:
                            </strong>

                            <ul>
                              {scene.visual_elements.map(
                                (
                                  element,
                                  index
                                ) => (
                                  <li key={index}>
                                    {element}
                                  </li>
                                )
                              )}
                            </ul>
                          </div>
                        )}

                      </div>
                    )
                  )}

                </div>

              </div>
            )}

          </section>
        )}

        {/* -------------------------------- */}
        {/* Audio Generation */}
        {/* -------------------------------- */}

        <section className="card">

          <h2>🎙 Audio Generation</h2>

          <div className="controls">

            {/* Language */}

            <label>
              Language

              <select
                value={language}
                onChange={
                  handleLanguageChange
                }
              >
                {Object.entries(
                  LANGUAGE_CONFIG
                ).map(
                  ([code, config]) => (
                    <option
                      key={code}
                      value={code}
                    >
                      {config.name}
                    </option>
                  )
                )}
              </select>
            </label>

            {/* Voice */}

            <label>
              Voice

              <select
                value={voice}
                onChange={(event) =>
                  setVoice(event.target.value)
                }
              >
                {selectedLanguage.voices.map(
                  (voiceOption) => (
                    <option
                      key={voiceOption.id}
                      value={voiceOption.id}
                    >
                      {voiceOption.gender} —{" "}
                      {voiceOption.name}
                    </option>
                  )
                )}
              </select>
            </label>

            {/* Duration */}

            <label>
              Duration

              <input
                type="number"
                min="1"
                max="30"
                step="1"
                value={duration}
                onChange={(event) =>
                  setDuration(
                    event.target.value
                  )
                }
              />
            </label>

            {/* Speed */}

            <label>
              Speed

              <input
                type="number"
                min="0.7"
                max="1.3"
                step="0.1"
                value={speed}
                onChange={(event) =>
                  setSpeed(
                    event.target.value
                  )
                }
              />
            </label>

          </div>

          <button
            onClick={handleGenerateAudio}
            disabled={audioLoading}
          >
            {audioLoading
              ? "Generating Audio..."
              : "Generate Audio"}
          </button>

          {audioFile && (
            <div className="result">

              <h3>
                Generated Narration
              </h3>

              <audio
                controls
                src={getAudioUrl(audioFile)}
              />

              <p>
                {audioFile}
              </p>

            </div>
          )}

        </section>

        {/* -------------------------------- */}
        {/* Image Generation */}
        {/* -------------------------------- */}

        <section className="card">

          <h2>🖼 Image Generation</h2>

          <div className="controls">

            <label>
              Number of Images

              <input
                type="number"
                min="1"
                max="20"
                value={imageCount}
                onChange={(event) =>
                  setImageCount(
                    event.target.value
                  )
                }
              />
            </label>

          </div>

          <button
            onClick={handleGenerateImages}
            disabled={imagesLoading}
          >
            {imagesLoading
              ? "Generating Images..."
              : "Generate Images"}
          </button>

          {images.length > 0 && (
            <div className="image-grid">

              {images.map(
                (imagePath, index) => {

                  const filename =
                    imagePath.split(
                      "/"
                    ).pop();

                  return (
                    <div
                      className="image-card"
                      key={imagePath}
                    >

                      {imageStoryName && (
                        <img
                          src={getImageUrl(
                            imageStoryName,
                            filename
                          )}
                          alt={`Story scene ${
                            index + 1
                          }`}
                        />
                      )}

                      <p>
                        Scene {index + 1}
                      </p>

                    </div>
                  );
                }
              )}

            </div>
          )}

        </section>

      </main>
    </div>
  );
}

export default App;
