'use client';

import { Folder, File, ChevronRight, ChevronDown } from 'lucide-react';
import { useState } from 'react';
import styles from './FileTree.module.css';

interface FileNode {
  name: string;
  type: 'file' | 'folder';
  children?: FileNode[];
}

const mockStructure: FileNode[] = [
  {
    name: 'src',
    type: 'folder',
    children: [
      { name: 'app.py', type: 'file' },
      { name: 'utils.py', type: 'file' },
      {
        name: 'components',
        type: 'folder',
        children: [
          { name: 'Header.tsx', type: 'file' },
          { name: 'Button.tsx', type: 'file' },
        ],
      },
    ],
  },
  { name: 'package.json', type: 'file' },
  { name: 'README.md', type: 'file' },
];

export default function FileTree() {
  return (
    <div className={`${styles.container} glass`}>
      <div className={styles.header}>EXPLORER</div>
      <div className={styles.tree}>
        {mockStructure.map((node) => (
          <TreeNode key={node.name} node={node} depth={0} />
        ))}
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
