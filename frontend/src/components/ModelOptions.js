/**
 * 🧠 MODEL OPTIONS - BRUTALNE CHECKBOX OPCIJE 🧠
 * Kompletna kontrola nad svim AI mogućnostima
 * Trenutne i buduće funkcionalnosti
 */

import React, { useState, useEffect } from 'react';
import './ModelOptions.css';
import axios from 'axios';

const ModelOptions = ({ modelConfig, onConfigChange, apiUrl, onModelReload }) => {
  const [localConfig, setLocalConfig] = useState(modelConfig || {});
  const [isExpanded, setIsExpanded] = useState(false);
  const [activeTab, setActiveTab] = useState('current');
  const [showReloadPrompt, setShowReloadPrompt] = useState(false);
  const [expandedSettings, setExpandedSettings] = useState({}); // Track which capability settings are expanded
  
  // 🎯 TRENUTNE MOGUĆNOSTI - dostupne sada
  const currentCapabilities = [
    {
      id: 'thinking',
      label: '🧠 Extended Thinking',
      description: 'Enable step-by-step reasoning and complex problem solving',
      category: 'reasoning',
      enabled: true,
      settings: {
        complexity_threshold: 0.7,
        max_thinking_steps: 10,
        show_thinking_process: true
      }
    },
    {
      id: 'memory',
      label: '💾 Long-term Memory',
      description: 'Remember conversations, preferences, and context across sessions',
      category: 'memory',
      enabled: true,
      settings: {
        memory_retention_days: 365,
        auto_summarize: true,
        importance_threshold: 0.6
      }
    },
    {
      id: 'web_search',
      label: '🌐 Web Search',
      description: 'Search internet for real-time information and knowledge',
      category: 'knowledge',
      enabled: true,
      settings: {
        auto_search: false,
        search_engine: 'google',
        max_results: 10
      }
    },
    {
      id: 'code_execution',
      label: '⚡ Code Execution',
      description: 'Run and test code directly in secure environment',
      category: 'development',
      enabled: true,
      settings: {
        timeout_seconds: 30,
        allow_file_access: false,
        languages: ['python', 'javascript', 'bash']
      }
    },
    {
      id: 'file_operations',
      label: '📁 File Management',
      description: 'Create, edit, analyze files and manage workspace',
      category: 'productivity',
      enabled: true,
      settings: {
        auto_backup: true,
        file_size_limit_mb: 100,
        allowed_extensions: 'all'
      }
    },
    {
      id: 'email_integration',
      label: '📧 Email Agent',
      description: 'Send emails, schedule meetings, manage inbox',
      category: 'communication',
      enabled: true,
      settings: {
        auto_reply: false,
        meeting_scheduling: true,
        email_templates: true
      }
    },
    {
      id: 'viber_integration',
      label: '💬 Viber Integration',
      description: 'Read and respond to Viber messages automatically',
      category: 'communication',
      enabled: true,
      settings: {
        auto_response: false,
        sentiment_analysis: true,
        message_history: true
      }
    },
    {
      id: 'calendar_management',
      label: '📅 Calendar Agent',
      description: 'Manage schedule, create events, set reminders',
      category: 'productivity',
      enabled: true,
      settings: {
        conflict_detection: true,
        auto_reminders: true,
        calendar_sync: true
      }
    },
    {
      id: 'task_management',
      label: '✅ Task Manager',
      description: 'Create, track, and manage tasks and projects',
      category: 'productivity',
      enabled: true,
      settings: {
        priority_scoring: true,
        deadline_tracking: true,
        progress_analytics: true
      }
    },
    {
      id: 'voice_interaction',
      label: '🎤 Voice Commands',
      description: 'Voice input and text-to-speech responses',
      category: 'interaction',
      enabled: true,
      settings: {
        voice_recognition: 'google',
        tts_voice: 'neural',
        noise_cancellation: true
      }
    },
    {
      id: 'image_analysis',
      label: '🖼️ Image Understanding',
      description: 'Analyze, describe, and process images',
      category: 'multimodal',
      enabled: false,
      settings: {
        ocr_enabled: true,
        face_detection: false,
        image_generation: false
      }
    },
    {
      id: 'document_processing',
      label: '📄 Document AI',
      description: 'Extract, summarize, and analyze documents',
      category: 'knowledge',
      enabled: true,
      settings: {
        pdf_parsing: true,
        table_extraction: true,
        document_summarization: true
      }
    }
  ];
  
  // 🚀 BUDUĆE MOGUĆNOSTI - Coming Soon (2025-2045)
  const futureCapabilities = [
    {
      id: 'video_analysis',
      label: '🎥 Video Understanding',
      description: 'Analyze video content, extract information, generate summaries',
      category: 'multimodal',
      enabled: false,
      eta: '2025 Q2',
      settings: {
        real_time_processing: false,
        motion_detection: true,
        audio_transcription: true
      }
    },
    {
      id: 'autonomous_research',
      label: '🔬 Autonomous Research',
      description: 'Conduct deep research projects independently',
      category: 'reasoning',
      enabled: false,
      eta: '2025 Q3',
      settings: {
        multi_source_verification: true,
        citation_generation: true,
        hypothesis_testing: true
      }
    },
    {
      id: 'code_generation',
      label: '🤖 Advanced Code Gen',
      description: 'Generate complete applications from descriptions',
      category: 'development',
      enabled: false,
      eta: '2025 Q4',
      settings: {
        full_stack_apps: true,
        architecture_design: true,
        testing_generation: true
      }
    },
    {
      id: 'real_time_collaboration',
      label: '👥 Real-time Collaboration',
      description: 'Work simultaneously with multiple users',
      category: 'collaboration',
      enabled: false,
      eta: '2026 Q1',
      settings: {
        concurrent_editing: true,
        conflict_resolution: true,
        role_based_access: true
      }
    },
    {
      id: 'predictive_analytics',
      label: '📈 Predictive AI',
      description: 'Predict trends, outcomes, and future scenarios',
      category: 'analytics',
      enabled: false,
      eta: '2026 Q2',
      settings: {
        market_analysis: true,
        risk_assessment: true,
        scenario_modeling: true
      }
    },
    {
      id: 'emotional_intelligence',
      label: '💝 Emotional AI',
      description: 'Advanced emotion recognition and empathetic responses',
      category: 'interaction',
      enabled: false,
      eta: '2026 Q3',
      settings: {
        mood_tracking: true,
        empathy_modeling: true,
        therapeutic_support: false
      }
    },
    {
      id: 'quantum_computing',
      label: '⚛️ Quantum Integration',
      description: 'Leverage quantum computing for complex calculations',
      category: 'computing',
      enabled: false,
      eta: '2027 Q1',
      settings: {
        quantum_simulation: true,
        cryptography_enhanced: true,
        optimization_problems: true
      }
    },
    {
      id: 'neural_interface',
      label: '🧠 Brain-Computer Interface',
      description: 'Direct neural communication and thought reading',
      category: 'interface',
      enabled: false,
      eta: '2030+',
      settings: {
        thought_recognition: false,
        neural_feedback: false,
        memory_enhancement: false
      }
    },
    {
      id: 'holographic_projection',
      label: '🎭 Holographic Display',
      description: '3D holographic visualization and interaction',
      category: 'display',
      enabled: false,
      eta: '2032+',
      settings: {
        spatial_computing: false,
        gesture_control: false,
        haptic_feedback: false
      }
    },
    {
      id: 'time_prediction',
      label: '⏰ Temporal Analysis',
      description: 'Advanced time series analysis and future prediction',
      category: 'prediction',
      enabled: false,
      eta: '2035+',
      settings: {
        timeline_modeling: false,
        causality_analysis: false,
        butterfly_effect_calc: false
      }
    },
    {
      id: 'consciousness_simulation',
      label: '🤯 Consciousness Sim',
      description: 'Simulate consciousness and self-awareness',
      category: 'consciousness',
      enabled: false,
      eta: '2040+',
      settings: {
        self_reflection: false,
        existential_reasoning: false,
        meta_cognition: false
      }
    },
    {
      id: 'reality_synthesis',
      label: '🌌 Reality Generation',
      description: 'Create and manipulate virtual realities',
      category: 'reality',
      enabled: false,
      eta: '2045+',
      settings: {
        physics_simulation: false,
        world_generation: false,
        reality_merging: false
      }
    }
  ];
  
  const categories = {
    reasoning: { icon: '🧠', name: 'Reasoning', color: '#4F46E5' },
    memory: { icon: '💾', name: 'Memory', color: '#059669' },
    knowledge: { icon: '📚', name: 'Knowledge', color: '#DC2626' },
    development: { icon: '⚡', name: 'Development', color: '#7C2D12' },
    productivity: { icon: '📋', name: 'Productivity', color: '#1D4ED8' },
    communication: { icon: '💬', name: 'Communication', color: '#0891B2' },
    interaction: { icon: '🎭', name: 'Interaction', color: '#9333EA' },
    multimodal: { icon: '🎨', name: 'Multimodal', color: '#EA580C' },
    collaboration: { icon: '👥', name: 'Collaboration', color: '#16A34A' },
    analytics: { icon: '📊', name: 'Analytics', color: '#BE123C' },
    computing: { icon: '💻', name: 'Computing', color: '#4338CA' },
    interface: { icon: '🔌', name: 'Interface', color: '#7E22CE' },
    display: { icon: '📺', name: 'Display', color: '#0EA5E9' },
    prediction: { icon: '🔮', name: 'Prediction', color: '#DB2777' },
    consciousness: { icon: '🧘', name: 'Consciousness', color: '#8B5CF6' },
    reality: { icon: '🌈', name: 'Reality', color: '#F59E0B' }
  };
  
  useEffect(() => {
    setLocalConfig(modelConfig || {});
  }, [modelConfig]);
  
  const handleCapabilityToggle = (capabilityId) => {
    const newConfig = {
      ...localConfig,
      capabilities: {
        ...localConfig.capabilities,
        [capabilityId]: !localConfig.capabilities?.[capabilityId]
      }
    };
    setLocalConfig(newConfig);
    onConfigChange?.(newConfig);
  };
  
  const handleSettingChange = (capabilityId, settingKey, value) => {
    const newConfig = {
      ...localConfig,
      capabilitySettings: {
        ...localConfig.capabilitySettings,
        [capabilityId]: {
          ...localConfig.capabilitySettings?.[capabilityId],
          [settingKey]: value
        }
      }
    };
    setLocalConfig(newConfig);
    onConfigChange?.(newConfig);
  };
  
  const getConfig = () => {
    const token = localStorage.getItem('token');
    return { headers: { Authorization: `Bearer ${token}` } };
  };

  const saveAllSettings = async () => {
    try {
      // STEP 1: Save config to database
      const response = await axios.post(
        `${apiUrl}/user/model-config`,
        { config: localConfig },
        getConfig()
      );
      
      if (response.status === 200) {
        console.log('✅ Config saved to database');
        
        // STEP 2: Apply config to active runtime
        try {
          const applyResponse = await axios.post(
            `${apiUrl}/ai/apply-model-config`,
            {},
            getConfig()
          );
          
          if (applyResponse.status === 200) {
            console.log('✅ Config applied to runtime:', applyResponse.data);
            console.log('🔧 Changes:', applyResponse.data.changes);
          }
        } catch (applyError) {
          console.warn('⚠️ Could not apply config immediately:', applyError);
        }
        
        // Show reload prompt
        setShowReloadPrompt(true);
      }
    } catch (error) {
      console.error('Save error:', error);
      alert('❌ Error saving settings: ' + (error.response?.data?.detail || error.message));
    }
  };
  
  const reloadModel = async () => {
    try {
      if (onModelReload) {
        await onModelReload();
      }
      setShowReloadPrompt(false);
      alert('✅ Model reloaded with new settings!');
    } catch (error) {
      console.error('Reload error:', error);
      alert('❌ Error reloading model: ' + (error.response?.data?.detail || error.message));
    }
  };
  
  const renderCapability = (capability) => {
    const isEnabled = localConfig.capabilities?.[capability.id] || capability.enabled;
    const category = categories[capability.category] || categories.reasoning;
    const settings = capability.settings || {};
    const isSettingsExpanded = expandedSettings[capability.id] || false;
    
    return (
      <div key={capability.id} className={`capability-card ${isEnabled ? 'enabled' : 'disabled'}`}>
        <div className="capability-header">
          <div className="capability-info">
            <span className="category-icon" style={{ color: category.color }}>
              {category.icon}
            </span>
            <div className="capability-text">
              <h4>{capability.label}</h4>
              <p>{capability.description}</p>
              {capability.eta && (
                <span className="eta-badge">Coming: {capability.eta}</span>
              )}
            </div>
          </div>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            {isEnabled && Object.keys(settings).length > 0 && (
              <button
                onClick={() => setExpandedSettings(prev => ({ ...prev, [capability.id]: !prev[capability.id] }))}
                style={{
                  background: 'rgba(255,255,255,0.1)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  color: '#fff',
                  cursor: 'pointer',
                  fontSize: '0.9rem'
                }}
              >
                {isSettingsExpanded ? '▼' : '▶'} Advanced
              </button>
            )}
            <label className="capability-toggle">
              <input
                type="checkbox"
                checked={isEnabled}
                onChange={() => handleCapabilityToggle(capability.id)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>
        
        {isEnabled && isSettingsExpanded && Object.keys(settings).length > 0 && (
          <div className="capability-settings">
            <h5>⚙️ Advanced Settings</h5>
            {Object.entries(settings).map(([key, value]) => (
              <div key={key} className="setting-item">
                <label>{key.replace(/_/g, ' ').toUpperCase()}</label>
                {typeof value === 'boolean' ? (
                  <input
                    type="checkbox"
                    checked={localConfig.capabilitySettings?.[capability.id]?.[key] ?? value}
                    onChange={(e) => handleSettingChange(capability.id, key, e.target.checked)}
                  />
                ) : typeof value === 'number' ? (
                  <input
                    type="number"
                    value={localConfig.capabilitySettings?.[capability.id]?.[key] ?? value}
                    onChange={(e) => handleSettingChange(capability.id, key, parseFloat(e.target.value))}
                  />
                ) : Array.isArray(value) ? (
                  <input
                    type="text"
                    value={(localConfig.capabilitySettings?.[capability.id]?.[key] || value).join(', ')}
                    onChange={(e) => handleSettingChange(capability.id, key, e.target.value.split(',').map(s => s.trim()))}
                    placeholder="Comma-separated values"
                  />
                ) : (
                  <input
                    type="text"
                    value={localConfig.capabilitySettings?.[capability.id]?.[key] ?? value}
                    onChange={(e) => handleSettingChange(capability.id, key, e.target.value)}
                  />
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };
  
  const groupCapabilitiesByCategory = (capabilities) => {
    const grouped = {};
    capabilities.forEach(capability => {
      const category = capability.category;
      if (!grouped[category]) {
        grouped[category] = [];
      }
      grouped[category].push(capability);
    });
    return grouped;
  };
  
  const currentGrouped = groupCapabilitiesByCategory(currentCapabilities);
  const futureGrouped = groupCapabilitiesByCategory(futureCapabilities);
  
  const enabledCount = currentCapabilities.filter(cap => 
    localConfig.capabilities?.[cap.id] || cap.enabled
  ).length;
  
  return (
    <div className="model-options">
      <div className="options-header">
        <div className="header-info">
          <h3>🧠 AI Model Configuration</h3>
          <p>Configure all AI capabilities and future features</p>
          <div className="stats">
            <span className="stat">
              ✅ {enabledCount}/{currentCapabilities.length} Current Features
            </span>
            <span className="stat">
              🚀 {futureCapabilities.length} Future Features
            </span>
          </div>
        </div>
        <button 
          className="expand-toggle"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? '▼' : '▶'} {isExpanded ? 'Collapse' : 'Expand'}
        </button>
      </div>
      
      {isExpanded && (
        <div className="options-content">
          <div className="tab-controls">
            <button 
              className={`tab-button ${activeTab === 'current' ? 'active' : ''}`}
              onClick={() => setActiveTab('current')}
            >
              🎯 Current Features ({currentCapabilities.length})
            </button>
            <button 
              className={`tab-button ${activeTab === 'future' ? 'active' : ''}`}
              onClick={() => setActiveTab('future')}
            >
              🚀 Future Features ({futureCapabilities.length})
            </button>
          </div>
          
          <div className="capabilities-grid">
            {activeTab === 'current' && Object.entries(currentGrouped).map(([categoryKey, capabilities]) => {
              const category = categories[categoryKey];
              return (
                <div key={categoryKey} className="category-section">
                  <h4 className="category-title" style={{ color: category.color }}>
                    {category.icon} {category.name}
                  </h4>
                  <div className="category-capabilities">
                    {capabilities.map(renderCapability)}
                  </div>
                </div>
              );
            })}
            
            {activeTab === 'future' && Object.entries(futureGrouped).map(([categoryKey, capabilities]) => {
              const category = categories[categoryKey];
              return (
                <div key={categoryKey} className="category-section future-section">
                  <h4 className="category-title" style={{ color: category.color }}>
                    {category.icon} {category.name} (Future)
                  </h4>
                  <div className="category-capabilities">
                    {capabilities.map(renderCapability)}
                  </div>
                </div>
              );
            })}
          </div>
          
          <div className="options-footer">
            <button className="save-button" onClick={saveAllSettings}>
              💾 Save All Settings
            </button>
            <div className="footer-info">
              <p>🔒 Settings are saved to your profile and synced across devices</p>
              <p>⚡ Changes take effect immediately for new conversations</p>
            </div>
          </div>
          
          {/* RELOAD PROMPT */}
          {showReloadPrompt && (
            <div style={{
              position: 'fixed',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              background: 'rgba(0,0,0,0.95)',
              border: '2px solid #00ff41',
              borderRadius: '12px',
              padding: '30px',
              zIndex: 10000,
              maxWidth: '500px',
              boxShadow: '0 10px 50px rgba(0,255,65,0.3)'
            }}>
              <h3 style={{color: '#00ff41', marginBottom: '15px'}}>⚠️ Model Restart Required</h3>
              <p style={{marginBottom: '20px', lineHeight: '1.6'}}>
                Settings saved successfully! Model needs to be restarted to apply new configuration.
              </p>
              <div style={{display: 'flex', gap: '10px', justifyContent: 'center'}}>
                <button 
                  onClick={reloadModel}
                  style={{
                    padding: '12px 24px',
                    background: 'linear-gradient(135deg, #667eea, #764ba2)',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                    fontWeight: 'bold',
                    cursor: 'pointer'
                  }}
                >
                  🔄 Reload Model Now
                </button>
                <button 
                  onClick={() => setShowReloadPrompt(false)}
                  style={{
                    padding: '12px 24px',
                    background: 'rgba(255,255,255,0.1)',
                    border: '1px solid rgba(255,255,255,0.3)',
                    borderRadius: '8px',
                    color: '#fff',
                    cursor: 'pointer'
                  }}
                >
                  ⏰ Later
                </button>
              </div>
              <p style={{fontSize: '0.85rem', marginTop: '15px', opacity: 0.7, textAlign: 'center'}}>
                Model will use old settings until restarted
              </p>
            </div>
          )}
          
          {/* BACKDROP */}
          {showReloadPrompt && (
            <div 
              onClick={() => setShowReloadPrompt(false)}
              style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'rgba(0,0,0,0.7)',
                zIndex: 9999
              }}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default ModelOptions;