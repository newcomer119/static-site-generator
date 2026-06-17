Here is a comprehensive, production-ready README.md for your Static Site Generator project. It is structured to serve as both an overview for anyone visiting your repository and a step-by-step roadmap for your second build.

Static Site Generator
A custom, open-source static site generator built completely from scratch in Python. This engine reads raw Markdown files, builds an internal Abstract Syntax Tree (AST) using a custom HTML DOM object implementation, processes complex inline tokens (bold, italics, code, images, and hyperlinks), and compiles them into a unified, styled production website.

Features
Custom HTML DOM Engine: Handles document structures recursively without relying on third-party parsing libraries.

Inline Markdown Tokenizer: Processes nested styling combinations using regex lookbehinds and custom splitting logic.

Macro Block Processor: Classifies structural layouts (headings, unordered/ordered lists, code blocks, blockquotes, and paragraphs).

Automated Asset Syncing: Cleanly wipes destination paths and mirrors assets recursively.

Production Path Prefixing: Supports subdirectory nesting configurations, making it compatible with GitHub Pages out of the box.