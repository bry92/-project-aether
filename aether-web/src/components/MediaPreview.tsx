'use client';

import { FileText, Play, Image as ImageIcon, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import styles from './MediaPreview.module.css';
import { supabase } from '@/lib/supabase';

interface MediaAsset {
  id: string;
  type: 'script' | 'video' | 'image';
  title: string;
  content: string;
  timestamp: string;
}

export default function MediaPreview() {
  const [assets, setAssets] = useState<MediaAsset[]>([]);

  useEffect(() => {
    const fetchAssets = async () => {
      const { data, error } = await supabase
        .from('assets')
        .select('*')
        .order('created_at', { ascending: false });

      if (data) {
        setAssets(data.map((a: any) => ({
          id: a.id,
          type: a.type,
          title: a.title,
          content: a.content,
          timestamp: new Date(a.created_at).toLocaleTimeString()
        })));
      }
    };

    fetchAssets();

    // Real-time subscription for new assets
    const channel = supabase
      .channel('assets_changes')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'assets' }, (payload) => {
        const newAsset = payload.new as any;
        setAssets((prev) => [{
          id: newAsset.id,
          type: newAsset.type,
          title: newAsset.title,
          content: newAsset.content,
          timestamp: new Date(newAsset.created_at).toLocaleTimeString()
        }, ...prev]);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return (
    <div className={`${styles.container} glass`}>
      <div className={styles.header}>
        <Play size={14} />
        <span>MEDIA PREVIEWER</span>
      </div>
      
      <div className={styles.content}>
        {assets.map((asset) => (
          <motion.div 
            key={asset.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={styles.assetCard}
          >
            <div className={styles.assetHeader}>
              <div className={styles.typeIcon}>
                {asset.type === 'script' && <FileText size={16} />}
                {asset.type === 'video' && <Play size={16} />}
                {asset.type === 'image' && <ImageIcon size={16} />}
              </div>
              <div className={styles.assetMeta}>
                <h4>{asset.title}</h4>
                <span>{asset.timestamp}</span>
              </div>
              <button className={styles.downloadBtn}><Download size={14} /></button>
            </div>
            
            <div className={styles.previewBox}>
              <pre>{asset.content}</pre>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
