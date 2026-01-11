# Anthropic Skills Workspace

A collection of local Codex skills with focused workflows, scripts, and references.

## Table of Contents

- [Overview](#overview)
- [Skills](#skills)
  - [iOS Simulator Skill](#ios-simulator-skill)
  - [macOS Calendar and Reminders](#macos-calendar-and-reminders)
  - [macOS Notes](#macos-notes)
  - [Medical Education](#medical-education)
  - [Operation ID Assigner](#operation-id-assigner)
  - [Planning With Files](#planning-with-files)

## Overview

This repo hosts multiple skill packages. Each skill includes its own `SKILL.md` with usage details, scripts, and references.

## Skills

### iOS Simulator Skill

Path: `ios-simulator-skill-1.3.1/`

- Purpose: Automate iOS app testing, building, and simulator management with accessibility-driven navigation.
- Includes 21 scripts covering build/test, navigation, accessibility audits, visual diffs, and simulator lifecycle.
- Entry point: `ios-simulator-skill-1.3.1/SKILL.md`

### macOS Calendar and Reminders

Path: `macos-calendar/`

- Purpose: Create, read, update, and delete Calendar and Reminders data via EventKit.
- Uses a wrapper script to manage the conda environment and permissions.
- Entry point: `macos-calendar/SKILL.md`

### macOS Notes

Path: `macos-notes/`

- Purpose: Manage Apple Notes via AppleScript with a Python CLI.
- Supports listing, creating, reading, searching, and deleting notes and folders.
- Entry point: `macos-notes/SKILL.md`

### Medical Education

Path: `medical-education/`

- Purpose: Build interactive medical education materials in self-contained HTML.
- Focuses on presentations, disease animations, anatomy viewers, and molecular visualizations.
- Entry point: `medical-education/SKILL.md`

### Operation ID Assigner

Path: `operation-id-assigner/`

- Purpose: Convert Chinese surgical procedure combinations into standardized ID signatures.
- Uses reference CSV data and supplemental rules for multi-ID mappings.
- Entry point: `operation-id-assigner/SKILL.md`

### Planning With Files

Path: `planning-with-files/`

- Purpose: Use persistent markdown files for multi-step task planning and progress tracking.
- Provides templates and scripts for `task_plan.md`, `findings.md`, and `progress.md`.
- Entry point: `planning-with-files/SKILL.md`
