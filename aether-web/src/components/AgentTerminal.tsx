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
  const [logs, setLogs] = useState<Log[]>([]);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'localhost:8000';
    const protocol = backendUrl.includes('localhost') ? 'ws' : 'wss';
    const socket = new WebSocket(`${protocol}://${backendUrl}/ws/pulse`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'pulse') {
        const newLog: Log = {
          id: Math.random().toString(36).substr(2, 9),
          agent: data.agent,
          message: data.action,
          type: data.agent === 'SYSTEM' ? 'error' : 'log',
        };
        setLogs((prev) => [...prev, newLog].slice(-50));
      }
    };

    return () => socket.close();
  }, []);

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
        {logs.length === 0 && (
          <div className={styles.empty}>System online. Waiting for agent telemetry...</div>
        )}
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
