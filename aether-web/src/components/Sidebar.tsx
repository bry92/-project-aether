'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { LayoutDashboard, Zap, Code2, Database, Rocket, Settings, Hexagon } from 'lucide-react';
import styles from './Sidebar.module.css';

export default function Sidebar() {
  const pathname = usePathname();
  
  const navItems = [
    { icon: <LayoutDashboard size={20} />, label: 'Dashboard', href: '/' },
    { icon: <Zap size={20} />, label: 'Live Pulse', href: '/pulse' },
    { icon: <Code2 size={20} />, label: 'The Forge', href: '/forge' },
    { icon: <Database size={20} />, label: 'Neural Memory', href: '/memory' },
    { icon: <Rocket size={20} />, label: 'Deployments', href: '/deploy' },
  ];

  return (
    <aside className={`${styles.sidebar} glass`}>
      <div className={styles.logo}>
        <div className={styles.logoIcon}>
          <Hexagon className={styles.hexagon} fill="currentColor" />
          <span className={styles.logoInitial}>A</span>
        </div>
        <span className={styles.logoText}>AETHER</span>
      </div>
      
      <nav className={styles.nav}>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link key={item.label} href={item.href} className={`${styles.navItem} ${isActive ? styles.active : ''}`}>
              {isActive && (
                <motion.div 
                  layoutId="sidebar-active"
                  className={styles.activePill}
                  transition={{ type: "spring", stiffness: 380, damping: 30 }}
                />
              )}
              <span className={styles.icon}>{item.icon}</span>
              <span className={styles.label}>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className={styles.footer}>
        <Link href="/settings" className={styles.navItem}>
          <Settings size={20} />
          <span className={styles.label}>Settings</span>
        </Link>
      </div>
    </aside>
  );
}
