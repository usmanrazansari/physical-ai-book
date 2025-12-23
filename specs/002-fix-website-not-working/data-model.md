# Data Model: Website Fixes

## Key Entities

### Website Pages
- **Name**: WebsitePage
- **Description**: Individual sections of the Physical AI Book website that users navigate to
- **Attributes**:
  - path: String (URL path for the page)
  - title: String (page title)
  - content: String (page content in MDX format)
  - status: String (status of the page: loaded, error, loading)

### User Session
- **Name**: UserSession
- **Description**: Represents the current state of a user's interaction with the website
- **Attributes**:
  - sessionId: String (unique identifier for the session)
  - startTime: DateTime (when the session started)
  - currentPage: String (current page the user is on)
  - isActive: Boolean (whether the session is currently active)

### Backend Services
- **Name**: BackendService
- **Description**: External systems that provide data and functionality to the website
- **Attributes**:
  - serviceType: String (type of service: chatbot, search, etc.)
  - endpoint: String (API endpoint URL)
  - status: String (status: connected, disconnected, error)
  - responseTime: Number (last response time in milliseconds)

## Relationships
- WebsitePage contains zero or more UserSession instances
- UserSession interacts with zero or more BackendService instances
- BackendService supports multiple WebsitePage instances

## State Transitions
- WebsitePage: loading → loaded (when page content is successfully loaded)
- WebsitePage: loading → error (when page fails to load)
- UserSession: active → inactive (when session ends)
- BackendService: disconnected → connected (when connection is established)
- BackendService: connected → error (when service becomes unavailable)