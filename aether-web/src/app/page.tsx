'use client';

import { motion } from 'framer-motion';
import { Rocket, ShieldCheck, Activity } from 'lucide-react';
import styles from './page.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className={styles.title}
        >
          Welcome to the <span className={styles.accent}>Aether</span>
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className={styles.subtitle}
        >
          Your autonomous startup engine is active and monitoring all systems.
        </motion.p>
      </header>

      <div className={styles.grid}>
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className={`${styles.card} glass`}
        >
          <div className={styles.cardHeader}>
            <Activity className={styles.cardIcon} />
            <h3>System Status</h3>
          </div>
          <div className={styles.cardContent}>
            <div className={styles.stat}>
              <span>Agents Online</span>
              <span className={styles.statValue}>5/5</span>
            </div>
            <div className={styles.stat}>
              <span>Active Threads</span>
              <span className={styles.statValue}>12</span>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className={`${styles.card} glass`}
        >
          <div className={styles.cardHeader}>
            <ShieldCheck className={styles.cardIcon} />
            <h3>Recent Approvals</h3>
          </div>
          <div className={styles.cardContent}>
            <p className={styles.cardText}>No pending approvals. Your agents are operating within established boundaries.</p>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className={`${styles.card} glass`}
        >
          <div className={styles.cardHeader}>
            <Rocket className={styles.cardIcon} />
            <h3>Quick Actions</h3>
          </div>
          <div className={styles.cardContent}>
            <button className={styles.button}>Deploy New Feature</button>
            <button className={styles.buttonSecondary}>Request Market Report</button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
