// All available themes
export const themes = {
  matrix: {
    name: 'Matrix',
    '--primary-bg': '#0d0d0d',
    '--secondary-bg': '#1a1a1a',
    '--accent': '#00ff41',
    '--text': '#00ff41',
    '--text-secondary': '#00aa00',
    '--border': '#00ff41',
    '--hover': 'rgba(0, 255, 65, 0.1)',
    '--shadow': 'rgba(0, 255, 65, 0.3)',
  },
  cyberpunk: {
    name: 'Cyberpunk',
    '--primary-bg': '#0a0a0a',
    '--secondary-bg': '#1a1a2e',
    '--accent': '#ff00ff',
    '--text': '#00ffff',
    '--text-secondary': '#ff00ff',
    '--border': '#ff00ff',
    '--hover': 'rgba(255, 0, 255, 0.2)',
    '--shadow': 'rgba(255, 0, 255, 0.5)',
  },
  pro: {
    name: 'Professional',
    '--primary-bg': '#1e1e1e',
    '--secondary-bg': '#252526',
    '--accent': '#007acc',
    '--text': '#d4d4d4',
    '--text-secondary': '#969696',
    '--border': '#007acc',
    '--hover': 'rgba(0, 122, 204, 0.2)',
    '--shadow': 'rgba(0, 122, 204, 0.3)',
  },
  terminal: {
    name: 'Terminal',
    '--primary-bg': '#000000',
    '--secondary-bg': '#0a0a0a',
    '--accent': '#33ff33',
    '--text': '#33ff33',
    '--text-secondary': '#22aa22',
    '--border': '#33ff33',
    '--hover': 'rgba(51, 255, 51, 0.1)',
    '--shadow': 'rgba(51, 255, 51, 0.4)',
  },
  dark: {
    name: 'Dark',
    '--primary-bg': '#121212',
    '--secondary-bg': '#1e1e1e',
    '--accent': '#bb86fc',
    '--text': '#e1e1e1',
    '--text-secondary': '#a1a1a1',
    '--border': '#bb86fc',
    '--hover': 'rgba(187, 134, 252, 0.2)',
    '--shadow': 'rgba(187, 134, 252, 0.3)',
  },
  light: {
    name: 'Light',
    '--primary-bg': '#ffffff',
    '--secondary-bg': '#f5f5f5',
    '--accent': '#1976d2',
    '--text': '#212121',
    '--text-secondary': '#616161',
    '--border': '#1976d2',
    '--hover': 'rgba(25, 118, 210, 0.1)',
    '--shadow': 'rgba(25, 118, 210, 0.2)',
  },
  hacker: {
    name: 'Hacker',
    '--primary-bg': '#0c0c0c',
    '--secondary-bg': '#141414',
    '--accent': '#ff3131',
    '--text': '#00ff00',
    '--text-secondary': '#00cc00',
    '--border': '#ff3131',
    '--hover': 'rgba(255, 49, 49, 0.2)',
    '--shadow': 'rgba(255, 49, 49, 0.5)',
  },
  neon: {
    name: 'Neon',
    '--primary-bg': '#0a0a1a',
    '--secondary-bg': '#14141f',
    '--accent': '#ff006e',
    '--text': '#00f5ff',
    '--text-secondary': '#ff006e',
    '--border': '#ff006e',
    '--hover': 'rgba(255, 0, 110, 0.2)',
    '--shadow': 'rgba(255, 0, 110, 0.6)',
  },
};

export const applyTheme = (themeName) => {
  const theme = themes[themeName] || themes.matrix;
  const root = document.documentElement;
  
  Object.keys(theme).forEach(key => {
    if (key !== 'name') {
      root.style.setProperty(key, theme[key]);
    }
  });
  
  localStorage.setItem('theme', themeName);
};

export const getStoredTheme = () => {
  return localStorage.getItem('theme') || 'matrix';
};
