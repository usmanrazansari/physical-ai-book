# Data Model: Physical AI & Humanoid Robotics Book

## Entities

### Module
- **Name**: Text identifier for the module (e.g., "The Robotic Nervous System")
- **Description**: Brief overview of the module's focus
- **Chapters**: Collection of 2 chapter references
- **Navigation**: Sidebar position and parent-child relationships

### Chapter
- **Title**: Chapter title (e.g., "ROS 2 architecture")
- **Content**: Markdown content of the chapter
- **Module**: Reference to parent module
- **Position**: Order within the module (1 or 2)
- **Metadata**: Author, date, citations

### Citation
- **Source**: Reference to the original source (book, paper, article)
- **Type**: Peer-reviewed, technical documentation, conference paper, etc.
- **Format**: APA format as required
- **Link**: URL or DOI when available

### NavigationItem
- **Label**: Text for the navigation element
- **Path**: URL path relative to site root
- **Parent**: Reference to parent navigation item (if any)
- **Children**: Collection of child navigation items

## Relationships

- Each Module contains exactly 2 Chapters (requirement FR-001)
- Each Chapter belongs to exactly 1 Module
- Each Chapter may have multiple Citations
- NavigationItems form a hierarchical structure reflecting Modules and Chapters

## Validation Rules

- Module names must be unique within the book
- Chapter titles must be unique within each module
- Citations must follow APA format (requirement FR-003)
- Content must maintain academic tone (requirement FR-003)
- No code examples allowed (requirement FR-004)
- No ethics discussions or vendor comparisons (requirement FR-005)