const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function handleResponse(response) {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail || "Something went wrong with the API request"
    );
  }

  return data;
}

export async function generateStoryAudio(payload) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/story/generate`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  return handleResponse(response);
}

export async function generateStoryImages(payload) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/story/images`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  return handleResponse(response);
}

export function getAudioUrl(filename) {
  return `${API_BASE_URL}/api/v1/story/audio/${encodeURIComponent(
    filename
  )}`;
}

export function getImageUrl(storyName, filename) {
  return `${API_BASE_URL}/api/v1/story/images/${encodeURIComponent(
    storyName
  )}/${encodeURIComponent(filename)}`;
}

export function getGeneratedImageUrl(imagePath) {
  const parts = imagePath.split("/");

  const storyName = parts[1];
  const filename = parts[2];

  return getImageUrl(storyName, filename);
}



export async function analyzeStory(story) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/story/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        story: story,
      }),
    }
  );

  return handleResponse(response);
}