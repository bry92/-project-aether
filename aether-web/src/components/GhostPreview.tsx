'use client';

import { Check, X, Info } from 'lucide-react';
import { motion } from 'framer-motion';
import styles from './GhostPreview.module.css';

export default function GhostPreview() {
  return (
    <div className={`${styles.preview} glass`}>
      <div className={styles.header}>
        <div className={styles.titleGroup}>
          <Info size={16} className={styles.icon} />
          <h3>PENDING APPROVAL</h3>
        </div>
        <div className={styles.actions}>
          <button className={styles.reject}><X size={16} /></button>
          <button className={styles.approve}><Check size={16} /> Approve Plan</button>
        </div>
      </div>
      
      <div className={styles.content}>
        <div className={styles.planHeader}>
          <span className={styles.agentTag}>Architect</span>
          <p>Proposed Change: Implement user authentication flow with NextAuth.js</p>
        </div>
        
        <div className={styles.diffView}>
          <div className={styles.diffLineAdded}>+ import NextAuth from "next-auth"</div>
          <div className={styles.diffLineAdded}>+ import GithubProvider from "next-auth/providers/github"</div>
          <div className={styles.diffLine}>  export const authOptions = &#123;</div>
          <div className={styles.diffLineAdded}>+   providers: [ GithubProvider(&#123; clientId: ..., clientSecret: ... &#125;) ]</div>
          <div className={styles.diffLine}>  &#125;</div>
        </div>
      </div>
    </div>
  );
}
