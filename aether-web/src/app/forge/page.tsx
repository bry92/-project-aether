'use client';

import FileTree from '@/components/FileTree';
import AgentTerminal from '@/components/AgentTerminal';
import GhostPreview from '@/components/GhostPreview';
import { useState } from 'react';
import styles from './page.module.css';

export default function ForgePage() {
  const [showPreview, setShowPreview] = useState(true);

  return (
    <div className={styles.forgeContainer}>
      <div className={styles.workspace}>
        <FileTree />
        <div className={styles.editorPlaceholder}>
          <AgentTerminal />
        </div>
      </div>
      
      {showPreview && <GhostPreview />}
    </div>
  );
}
