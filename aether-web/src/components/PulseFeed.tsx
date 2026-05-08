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
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'localhost:8000';
    const protocol = backendUrl.includes('localhost') ? 'ws' : 'wss';
    const socket = new WebSocket(`${protocol}://${backendUrl}/ws/pulse`);

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
      } else if (data.type === 'approval_required') {
        // We will trigger the GhostPreview visibility here
        window.dispatchEvent(new CustomEvent('aether-approval-required', { detail: data.approval }));
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
              className={`${styles.item} glass-hover`}
            >
              <div className={styles.agentInfo}>
                <span className={`${styles.agentName} ${styles[item.agent.toLowerCase()] || ''}`}>{item.agent}</span>
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
