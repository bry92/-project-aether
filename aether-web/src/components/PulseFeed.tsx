'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, Code, Globe, MessageSquare } from 'lucide-react';
import styles from './PulseFeed.module.css';

interface PulseItem {
  id: string;
  agent: string;
  action: string;
  timestamp: string;
  type?: 'engineering' | 'ops' | 'marketing' | 'system';
}

export default function PulseFeed() {
  const [pulseItems, setPulseItems] = useState<PulseItem[]>([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/pulse');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'pulse') {
        const newItem: PulseItem = {
          id: Math.random().toString(36).substr(2, 9),
          agent: data.agent,
          action: data.action,
          timestamp: data.timestamp,
        };
        setPulseItems((prev) => [newItem, ...prev].slice(0, 20));
      }
    };

    return () => socket.close();
  }, []);

  return (
    <div className={`${styles.pulse} glass`}>
      <div className={styles.header}>
        <span className={styles.statusDot}></span>
        <h3 className={styles.title}>LIVE PULSE</h3>
      </div>
      
      <div className={styles.feed}>
        <AnimatePresence initial={false}>
          {pulseItems.map((item) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className={styles.item}
            >
              <div className={styles.agentInfo}>
                <span className={styles.agentName}>{item.agent}</span>
                <span className={styles.timestamp}>{item.timestamp}</span>
              </div>
              <p className={styles.action}>{item.action}</p>
            </motion.div>
          ))}
        </AnimatePresence>
        {pulseItems.length === 0 && (
          <div className={styles.emptyState}>
            Waiting for signal...
          </div>
        )}
      </div>
    </div>
  );
}
