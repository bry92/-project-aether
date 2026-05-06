'use client';

import { Check, X, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';
import styles from './GhostPreview.module.css';

interface ApprovalData {
  id: string;
  agent: string;
  description: string;
  details: string;
}

export default function GhostPreview() {
  const [approval, setApproval] = useState<ApprovalData | null>(null);

  useEffect(() => {
    const handleApproval = (e: any) => {
      setApproval(e.detail);
    };

    window.addEventListener('aether-approval-required', handleApproval);
    return () => window.removeEventListener('aether-approval-required', handleApproval);
  }, []);

  if (!approval) return null;

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className={`${styles.preview} glass`}
      >
        <div className={styles.header}>
          <div className={styles.titleGroup}>
            <Info size={16} className={styles.icon} />
            <h3>PENDING APPROVAL</h3>
          </div>
          <div className={styles.actions}>
            <button className={styles.reject} onClick={() => setApproval(null)}><X size={16} /></button>
            <button className={styles.approve} onClick={() => setApproval(null)}>
              <Check size={16} /> Approve Plan
            </button>
          </div>
        </div>
        
        <div className={styles.content}>
          <div className={styles.planHeader}>
            <span className={styles.agentTag}>{approval.agent}</span>
            <p>{approval.description}</p>
          </div>
          
          <div className={styles.detailsView}>
            {approval.details}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
