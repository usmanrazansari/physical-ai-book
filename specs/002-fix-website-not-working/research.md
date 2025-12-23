# Research: Fix Website Not Working

## Decision: Technology Stack Identified
The Physical AI Book website is built with:
- **Framework**: Docusaurus 3.1.0 (static site generator based on React)
- **Frontend**: React 18.x with custom components
- **Deployment**: GitHub Pages (configured in docusaurus.config.js)
- **Node.js Version**: >=18.0 (as specified in package.json)

## Rationale
The website uses Docusaurus, which is a modern documentation framework that creates static websites. The main issues likely stem from:
1. Build configuration problems
2. Missing or misconfigured dependencies
3. Chat widget integration issues
4. Deployment configuration issues

## Current Implementation Analysis
1. **Main site**: src/pages/index.js - Homepage with features, books, and CTA sections
2. **Layout**: src/theme/Layout/index.js - Includes the ChatWidget globally
3. **Chat Widget**: src/plugins/ChatWidget.js - Floating chat interface that connects to backend
4. **Chat Interface**: src/components/ChatInterface/ChatInterface.jsx - The actual chat component

## Key Issues Identified
1. The ChatWidget is loaded on every page via the global Layout
2. The backend URL is hardcoded to localhost:8000, which won't work in production
3. The website might fail to build if there are dependency issues
4. There could be runtime errors in the browser that prevent proper rendering

## Potential Solutions
1. Fix the backend URL configuration for different environments
2. Ensure all dependencies are properly installed
3. Add error handling for the chat widget to prevent it from breaking the entire site
4. Verify the build process works correctly