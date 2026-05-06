'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import styles from './CommandCenter.module.css';

export default function CommandCenter() {
  const [command, setCommand] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;

    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:8000/tasks/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: command }),
      });
      
      if (response.ok) {
        setCommand('');
      }
    } catch (error) {
      console.error('Failed to execute task:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className={`${styles.commandCenter} glass`}>
      <div className={styles.header}>
        <Sparkles size={16} className={styles.icon} />
        <span>COMMAND CENTER</span>
      </div>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder="What shall we build today?"
          className={styles.input}
          disabled={isProcessing}
        />
        <button type="submit" className={styles.submitButton} disabled={isProcessing}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
