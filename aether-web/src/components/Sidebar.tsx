import Link from 'next/link';
import { LayoutDashboard, Zap, Code2, Database, Rocket, Settings } from 'lucide-react';
import styles from './Sidebar.module.css';

export default function Sidebar() {
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
        <div className={styles.logoIcon}>A</div>
        <span className={styles.logoText}>AETHER</span>
      </div>
      
      <nav className={styles.nav}>
        {navItems.map((item) => (
          <Link key={item.label} href={item.href} className={styles.navItem}>
            <span className={styles.icon}>{item.icon}</span>
            <span className={styles.label}>{item.label}</span>
          </Link>
        ))}
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
