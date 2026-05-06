'use client';

import { Terminal as TerminalIcon } from 'lucide-react';
import { useEffect, useState, useRef } from 'react';
import styles from './AgentTerminal.module.css';

interface Log {
  id: string;
  agent: string;
  message: string;
  type: 'log' | 'command' | 'error';
}

export default function AgentTerminal() {
  const [logs, setLogs] = useState<Log[]>([
    { id: '1', agent: 'CEO', message: 'Forge initialized. Waiting for task...', type: 'log' },
  ]);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className={`${styles.terminal} glass`}>
      <div className={styles.header}>
        <TerminalIcon size={14} />
        <span>AGENT TERMINAL</span>
      </div>
      <div className={styles.content}>
        {logs.map((log) => (
          <div key={log.id} className={styles.logLine}>
            <span className={styles.agentTag}>{log.agent}:</span>
            <span className={styles[log.type]}>{log.message}</span>
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
}
