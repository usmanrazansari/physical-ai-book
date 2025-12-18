// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An educational book on embodied intelligence and AI systems operating in the physical world',
  favicon: 'img/favicon.ico',
  staticDirectories: ['static', 'public'],
  url: 'https://usmanrazansari.github.io',
  baseUrl: '/physical-ai-book/',
  organizationName: 'usmanrazansari',
  projectName: 'physical-ai-book',
  deploymentBranch: 'gh-pages',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/usmanrazansari/physical-ai-book/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],
  themeConfig: ({
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI Book',
      logo: {
        alt: 'Physical AI Book Logo',
        src: 'img/logo.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          href: 'https://github.com/usmanrazansari/physical-ai-book',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Book',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/usmanrazansari/physical-ai-book',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
      // This is where we inject the chat widget
      customHtml: `
        <div id="chat-root"></div>
      `,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    // Load React, ReactDOM, and Babel from CDN
    scripts: [
      'https://unpkg.com/react@18/umd/react.production.min.js',
      'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js',
      'https://unpkg.com/@babel/standalone/babel.min.js',
      {
        innerHTML: `
          const { useState } = React;

          const ChatWidget = () => {
            const [isOpen, setIsOpen] = useState(false);
            const [query, setQuery] = useState('');
            const [history, setHistory] = useState([]);

            const BACKEND_URL = "https://usmanhello-physical-ai-book.hf.space";

            const sendQuery = async () => {
              if (!query.trim()) return;
              setHistory([...history, { sender: 'You', text: query }]);
              try {
                const resp = await fetch(https://usmanhello-physical-ai-book.hf.space/chat`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ query })
                });
                const data = await resp.json();
                setHistory(prev => [...prev, { sender: 'Bot', text: data.answer || 'No answer received' }]);
              } catch (e) {
                setHistory(prev => [...prev, { sender: 'Bot', text: 'Error: Could not connect to chatbot. Try again later.' }]);
              }
              setQuery('');
            };

            return (
              <>
                <div
                  onClick={() => setIsOpen(!isOpen)}
                  style={{
                    position: 'fixed',
                    bottom: '20px',
                    right: '20px',
                    background: '#007bff',
                    color: 'white',
                    width: '60px',
                    height: '60px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer',
                    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
                    zIndex: 10000,
                    fontSize: '30px'
                  }}
                >
                  💬
                </div>

                {isOpen && (
                  <div style={{
                    position: 'fixed',
                    bottom: '90px',
                    right: '20px',
                    width: '350px',
                    height: '500px',
                    background: 'white',
                    borderRadius: '10px',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
                    display: 'flex',
                    flexDirection: 'column',
                    zIndex: 10000
                  }}>
                    <div style={{ background: '#007bff', color: 'white', padding: '10px', borderTopLeftRadius: '10px', borderTopRightRadius: '10px' }}>
                      Physical AI Book Chatbot
                    </div>
                    <div style={{ flex: 1, padding: '10px', overflowY: 'auto' }}>
                      {history.map((msg, i) => (
                        <div key={i} style={{ textAlign: msg.sender === 'You' ? 'right' : 'left', margin: '5px 0' }}>
                          <strong>{msg.sender}:</strong> {msg.text}
                        </div>
                      ))}
                    </div>
                    <input
                      type="text"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && sendQuery()}
                      placeholder="Ask a question about the book..."
                      style={{ width: '100%', padding: '10px', border: 'none', borderTop: '1px solid #eee' }}
                    />
                  </div>
                )}
              </>
            );
          };

          const container = document.getElementById('chat-root');
          if (container) {
            const root = ReactDOM.createRoot(container);
            root.render(<ChatWidget />);
          }
        `,
        type: 'text/babel',
        'data-type': 'jsx',
      },
    ],
  }),
};

export default config;
