import React from 'react';

interface StoryDisplayProps {
  storyText: string;
  imagePrompt: string;
}

const StoryDisplay: React.FC<StoryDisplayProps> = ({ storyText, imagePrompt }) => {
  return (
    <div className="story-display-container">
      <div className="story-text">
        {storyText.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      <div className="image-prompt-area">
        <h4>Let's Imagine!</h4>
        <p>{imagePrompt}</p>
      </div>
    </div>
  );
};

export default StoryDisplay; 