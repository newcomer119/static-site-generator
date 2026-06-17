# GrugSite: A Bare-Metal Markdown to HTML Compiler in Python

GrugSite is a custom, open-source static site generator built completely from scratch in Python. Instead of relying on third-party parsing libraries, this engine tokenizes raw Markdown strings, constructs an internal Abstract Syntax Tree (AST) using a custom DOM node implementation, and recursively compiles the nodes into a fast, static production website.

## 🎯 Motivation

Most modern static site generators (like Hugo or Jekyll) are massive, black-box systems wrapped in complex dependencies. I built GrugSite to master the fundamental mechanics underneath the hood of web compilers:
1. **The DOM Layer**: Managing parent-child rendering lifecycles entirely programmatically.
2. **Lexical Analysis**: Breaking down string text streams into valid token states using regular expressions and string splitters.
3. **AST Composition**: Structuring macro layouts (blocks) and micro styles (inline elements) into a unified, predictable hierarchy.

---

## 🚀 Quick Start

### 1. Requirements
* Python 3.10 or higher
* Unix terminal environment (Linux, WSL, or macOS)

### 2. Local Development Sandbox
To compile the site locally and spin up a development testing server, execute the launch utility script from your project root:
```bash
chmod +x main.sh
./main.sh


## 🤝 Contributing

### Clone the repo

```bash
git clone https://github.com/xyz/zipzod@latest
cd zipzod
```

### Build the compiled binary

```bash
go build
```

### Run the test suite

```bash
go test ./...
```

### Submit a pull request

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
