import React from 'react';

interface FormProps {
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
  children: React.ReactNode;
  className?: string;
}

const Form: React.FC<FormProps> = ({ onSubmit, children, className }) => {
  return (
    <form onSubmit={onSubmit} className={`space-y-4 ${className || ''}`}>
      {children}
    </form>
  );
};

export default Form;
