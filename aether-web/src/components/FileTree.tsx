'use client';

import { Folder, File, ChevronRight, ChevronDown, RefreshCw } from 'lucide-react';
import { useState, useEffect } from 'react';
import styles from './FileTree.module.css';

interface FileNode {
  name: string;
  type: 'file' | 'folder';
  children?: FileNode[];
}

export default function FileTree() {
  const [structure, setStructure] = useState<FileNode[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchStructure = async () => {
    setLoading(true);
    try {
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/files/list`);
      const data = await response.json();
      if (data.children) {
        setStructure(data.children);
      } else {
        setStructure([data]);
      }
    } catch (error) {
      console.error('Failed to fetch file structure:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStructure();
  }, []);

  return (
    <div className={`${styles.container} glass`}>
      <div className={styles.header}>
        <span>EXPLORER</span>
        <button onClick={fetchStructure} className={styles.refreshButton}>
          <RefreshCw size={12} className={loading ? styles.spinning : ''} />
        </button>
      </div>
      <div className={styles.tree}>
        {loading ? (
          <div className={styles.loading}>Scanning workspace...</div>
        ) : (
          structure.map((node) => (
            <TreeNode key={node.name} node={node} depth={0} />
          ))
        )}
      </div>
    </div>
  );
}

function TreeNode({ node, depth }: { node: FileNode; depth: number }) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div>
      <div 
        className={styles.node} 
        style={{ paddingLeft: `${depth * 1.2}rem` }}
        onClick={() => node.type === 'folder' && setIsOpen(!isOpen)}
      >
        {node.type === 'folder' ? (
          <>
            {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            <Folder size={16} className={styles.folderIcon} />
          </>
        ) : (
          <File size={16} className={styles.fileIcon} />
        )}
        <span className={styles.name}>{node.name}</span>
      </div>
      {node.type === 'folder' && isOpen && node.children && (
        <div>
          {node.children.map((child) => (
            <TreeNode key={child.name} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}
