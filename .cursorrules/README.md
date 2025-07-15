# Cursor Rules Organization

This directory contains all Cursor rules files (`.mdc`) for the mentali project.

## File Structure

### Core Development Rules
- `thinkcode.mdc` - Core development principles and coding standards
- `role_definition.mdc` - Python/ML development role and technology stack

### Code Quality & Maintenance
- `clean.mdc` - Automated code cleaning and formatting guidelines
- `code-refactor.mdc` - Code optimization, security, and documentation rules
- `unitest.mdc` - Comprehensive unittest best practices and testing guidelines

### Project Management
- `analyze_issue.mdc` - GitHub issue analysis and implementation specification template

### MCP Development
- `mcp-best-practices.mdc` - Model Context Protocol tool development guidelines
- `mcp-inspector-debugging.mdc` - MCP debugging and inspection guidelines

## Usage

Cursor automatically loads all `.mdc` files from the `.cursorrules/` directory. These rules will be applied based on their `globs` patterns and `alwaysApply` settings.

## File Naming Convention

- Use descriptive names with underscores for spaces
- Group related rules with prefixes (e.g., `mcp-*` for MCP-related rules)
- Keep filenames concise but clear about their purpose 