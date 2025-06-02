import React, { useState, FormEvent } from 'react';

interface ThemeInputProps {
  onStartStory: (theme: string) => void;
  isLoading: boolean;
}

const ThemeInput: React.FC<ThemeInputProps> = ({ onStartStory, isLoading }) => {
  const [theme, setTheme] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (theme.trim()) {
      onStartStory(theme.trim());
    }
  };

  return (
    <div className="theme-input-container">
      <h2>What kind of adventure do you want?</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          placeholder="e.g., a friendly dragon, a magic forest"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !theme.trim()}>
          {isLoading ? 'Starting...' : 'Start Adventure!'}
        </button>
      </form>
      <p className="example-themes">Examples: a brave puppy, a talking squirrel, a journey to the stars, a hidden treasure</p>
    </div>
  );
};

export default ThemeInput; 