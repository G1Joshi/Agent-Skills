---
name: sanity
description: Sanity structured content platform. Use for content management.
---

# Sanity

Sanity is "Content as Data". The **Studio v3** is a real-time React application that you host, giving you complete control over the editing experience.

## When to Use

- **Structured Content**: You need complex relationships references.
- **Real-time Collaboration**: Like Google Docs for your content.
- **Custom Workflows**: You need custom approval buttons in the CMS.

## Core Concepts

### GROQ

Graph-Relational Object Queries. Powerful alternative to GraphQL. `*[_type == "movie" && rating > 8]`.

### The Studio

A React Single Page App (embedded in your Next.js app) for editing.

### Portable Text

JSON format for rich text (not HTML/Markdown), enabling custom rendering on any platform.

## Best Practices (2025)

**Do**:

- **Use Visual Editing**: Embed the studio in your app for clickable previews (Overlays).
- **Use GROQ**: It is much more concise than GraphQL for Sanity data.
- **Use TypeScript**: Define schema types with `defineType`.

**Don't**:

- **Don't hardcode IDs**: Use references.

## References

- [Sanity Documentation](https://www.sanity.io/)
