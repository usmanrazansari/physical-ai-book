// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An educational book on embodied intelligence and AI systems operating in the physical world',
  favicon: 'img/favicon.ico',
  staticDirectories: ['static', 'public'],

  // Set the production url of your site here
  url: 'https://usmanrazansari.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages deployment, it is often '/<projectName>/'
  baseUrl: '/physical-ai-book/',

  // GitHub pages deployment config.
  // If you aren't using GitHub Pages, you don't need these.
  organizationName: 'usmanrazansari', // Usually your GitHub org/user name.
  projectName: 'physical-ai-book', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: true,


  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-username/physical-ai-book/tree/main/',
        },
        blog: false, // Disable blog for book format
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
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
            href: 'https://github.com/your-username/physical-ai-book',
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
                href: 'https://github.com/your-username/physical-ai-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
  bottomHtml: `
    <div id="chat-root"></div>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/babel-standalone@7/babel.min.js"></script>
    <script type="text/babel">
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
            const resp = await fetch(`${BACKEND_URL}/ask`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ query })
            });
            const data = await resp.json();
            setHistory(prev => [...prev, { sender: 'Bot', text: data.answer || 'No answer' }]);
          } catch (e) {
            setHistory(prev => [...prev, { sender: 'Bot', text: 'Error: Try again later.' }]);
          }
          setQuery('');
        };

        return (
          <>
            <div onClick={() => setIsOpen(!isOpen)} style={{position:'fixed',bottom:'20px',right:'20px',background:'#007bff',color:'white',width:'60px',height:'60px',borderRadius:'50%',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',boxShadow:'0 4px 8px rgba(0,0,0,0.2)',zIndex:1000,fontSize:'30px'}}>
              💬
            </div>
            {isOpen && (
              <div style={{position:'fixed',bottom:'90px',right:'20px',width:'350px',height:'500px',background:'white',borderRadius:'10px',boxShadow:'0 4px 20px rgba(0,0,0,0.3)',display:'flex',flexDirection:'column',zIndex:1000}}>
                <div style={{background:'#007bff',color:'white',padding:'10px',borderTopLeftRadius:'10px',borderTopRightRadius:'10px'}}>Physical AI Book Chatbot</div>
                <div style={{flex:1,padding:'10px',overflowY:'auto'}}>
                  {history.map((msg, i) => (
                    <div key={i} style={{textAlign: msg.sender === 'You' ? 'right' : 'left', margin:'5px 0'}}>
                      <strong>{msg.sender}:</strong> {msg.text}
                    </div>
                  ))}
                </div>
                <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendQuery()} placeholder="Ask a question..." style={{width:'100%',padding:'10px',border:'none',borderTop:'1px solid #eee'}} />
              </div>
            )}
          </>
        );
      };

      const root = ReactDOM.createRoot(document.getElementById('chat-root'));
      root.render(<ChatWidget />);
    </script>
  `,

};

export default config;
