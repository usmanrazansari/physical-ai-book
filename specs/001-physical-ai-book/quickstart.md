# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Prerequisites

- Node.js 18+ installed
- Git for version control
- GitHub account for deployment

## Setup Instructions

1. **Install Docusaurus**
   ```bash
   npx create-docusaurus@latest website classic
   ```

2. **Navigate to project directory**
   ```bash
   cd website
   ```

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Create module directories**
   ```bash
   mkdir -p docs/module-1-ros2
   mkdir -p docs/module-2-digital-twin
   mkdir -p docs/module-3-ai-robot-brain
   mkdir -p docs/module-4-vla
   ```

5. **Start development server**
   ```bash
   npm start
   ```

## Creating Content

1. **Module Structure**: Each module should have an index.md file and 2 chapter files
2. **Content Format**: Write in Markdown with academic tone
3. **Citations**: Use APA format for all references
4. **Navigation**: Update `sidebars.js` to include new content

## Deployment to GitHub Pages

1. **Configure docusaurus.config.js** for GitHub Pages
2. **Set up GitHub Actions** for automated deployment
3. **Push to main branch** to trigger deployment

## Content Creation Workflow

1. Research and draft content following academic standards
2. Ensure all claims are verified against peer-reviewed sources
3. Maintain conceptual focus without code examples
4. Test navigation and cross-references
5. Validate academic tone and accuracy