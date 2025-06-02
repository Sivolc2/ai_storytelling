import { useState, useEffect } from 'react'
import './styles/App.css'
import ThemeInput from './components/ThemeInput'
import StoryDisplay from './components/StoryDisplay'
import ChoiceButtons from './components/ChoiceButtons'

// Define types for story history as expected by Gemini API
interface StoryPart {
  text: string;
}
interface StoryContent {
  role: 'user' | 'model';
  parts: StoryPart[];
}

type GameState = 'initial' | 'story' | 'loading' | 'error';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [gameState, setGameState] = useState<GameState>('initial');
  const [currentStoryText, setCurrentStoryText] = useState<string>('');
  const [currentImagePrompt, setCurrentImagePrompt] = useState<string>('');
  const [currentChoices, setCurrentChoices] = useState<string[]>([]);
  const [storyHistory, setStoryHistory] = useState<StoryContent[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleStartStory = async (theme: string) => {
    setGameState('loading');
    setErrorMessage(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/story/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to start story. Server returned an error.' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCurrentStoryText(data.story_text);
      setCurrentImagePrompt(data.image_prompt);
      setCurrentChoices(data.choices);
      setStoryHistory(data.updated_story_history);
      setGameState('story');
    } catch (err) {
      console.error("Error starting story:", err);
      setErrorMessage(err instanceof Error ? err.message : 'An unknown error occurred.');
      setGameState('error');
    }
  };

  const handleMakeChoice = async (choice: string) => {
    setGameState('loading');
    setErrorMessage(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/story/continue`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_history: storyHistory, choice_text: choice }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to continue story. Server returned an error.' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCurrentStoryText(data.story_text);
      setCurrentImagePrompt(data.image_prompt);
      setCurrentChoices(data.choices);
      setStoryHistory(data.updated_story_history);
      setGameState('story');
    } catch (err) {
      console.error("Error continuing story:", err);
      setErrorMessage(err instanceof Error ? err.message : 'An unknown error occurred.');
      setGameState('error');
    }
  };

  const handleRestart = () => {
    setGameState('initial');
    setCurrentStoryText('');
    setCurrentImagePrompt('');
    setCurrentChoices([]);
    setStoryHistory([]);
    setErrorMessage(null);
  }

  return (
    <div className="container adventure-container">
      <header>
        <h1>My Adventure Tale</h1>
      </header>
      <main>
        {gameState === 'initial' && (
          <ThemeInput onStartStory={handleStartStory} isLoading={false} />
        )}

        {gameState === 'loading' && (
          <div className="loading-message">
            <p>Thinking of a good story...</p>
            <div className="spinner"></div>
          </div>
        )}

        {gameState === 'story' && (
          <>
            <StoryDisplay storyText={currentStoryText} imagePrompt={currentImagePrompt} />
            <ChoiceButtons choices={currentChoices} onMakeChoice={handleMakeChoice} isLoading={false} />
            <button onClick={handleRestart} className="restart-button">Start New Adventure</button>
          </>
        )}

        {gameState === 'error' && (
          <div className="error-message">
            <p>Oh no, something went wrong!</p>
            <p>{errorMessage}</p>
            <button onClick={handleRestart}>Try Again</button>
          </div>
        )}
      </main>
      <footer>
        <p>Powered by AI Storytellers</p>
      </footer>
    </div>
  );
}

export default App;
