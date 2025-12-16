# Book Content Metadata Contract

## Purpose
Defines the required metadata structure for each chapter in the Physical AI & Humanoid Robotics Book to ensure consistency and proper documentation generation.

## Chapter Metadata Schema

Each chapter file (`.md`) must include the following frontmatter:

```yaml
---
title: "Chapter Title"
description: "Brief description of chapter content"
sidebar_label: "Label for sidebar navigation"
sidebar_position: 1  # 1 or 2 for chapter position in module
tags:
  - robotics
  - [specific-topic]
  - [module-topic]
authors:
  - [author-name]
keywords:
  - [keyword1]
  - [keyword2]
  - [keyword3]
references:
  - [apa-citation-1]
  - [apa-citation-2]
---
```

## Module Metadata Schema

Each module index file (e.g., `docs/module-1-ros2/index.md`) must include:

```yaml
---
title: "Module Title"
description: "Overview of the module content"
sidebar_label: "Module X: Title"
slug: "/module-x"
---
```

## Content Requirements

1. Each chapter must have 1-2 main headings (##) for major sections
2. All citations must follow APA format
3. Content must be written in academic tone
4. No code examples or implementation details allowed
5. Each chapter should be 625-875 words to meet the 5,000-7,000 total word requirement across 8 chapters

## Validation Rules

- Title must be 5-60 characters
- Description must be 10-160 characters
- Sidebar position must be either 1 or 2 for chapters
- At least 3 keywords required per chapter
- At least 2 references required per chapter
- No external links to implementation resources (code repositories, etc.)