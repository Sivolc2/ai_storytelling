import React from 'react';

interface ChoiceButtonsProps {
  choices: string[];
  onMakeChoice: (choice: string) => void;
  isLoading: boolean;
}

const ChoiceButtons: React.FC<ChoiceButtonsProps> = ({ choices, onMakeChoice, isLoading }) => {
  return (
    <div className="choice-buttons-container">
      <h3>What do you do next?</h3>
      {choices.map((choice, index) => (
        <button
          key={index}
          onClick={() => onMakeChoice(choice)}
          disabled={isLoading}
          className="choice-button"
        >
          {choice}
        </button>
      ))}
    </div>
  );
};

export default ChoiceButtons; 