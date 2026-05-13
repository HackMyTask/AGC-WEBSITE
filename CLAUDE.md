# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: AGC-WEBSITE

A website project for AGC. This is a new project under development.

## Getting Started

The project structure and tech stack are being established. Check back once initial setup is complete.

## Development Commands

To be added as the project is scaffolded.

## Architecture

To be documented as the project structure is defined.

## gstack

gstack is installed at `~/.claude/skills/gstack` and provides 47+ specialized skills for code review, planning, design, deployment, and more.

### Available Skills

Core skills:
- `/gstack` - Main gstack interface
- `/gstack-autoplan` - Automatic planning
- `/gstack-browse` - Browse and search code
- `/gstack-review` - Code review
- `/gstack-qa` - Quality assurance
- `/gstack-ship` - Ship and deploy code
- `/gstack-land-and-deploy` - Land PRs and deploy

Design skills:
- `/gstack-design-review` - Design review
- `/gstack-design-consultation` - Design consultation
- `/gstack-design-html` - HTML design
- `/gstack-design-shotgun` - Rapid design iteration

Planning skills:
- `/gstack-plan-eng-review` - Engineering review planning
- `/gstack-plan-design-review` - Design review planning
- `/gstack-plan-devex-review` - Developer experience review planning
- `/gstack-plan-ceo-review` - CEO review planning
- `/gstack-plan-tune` - Plan tuning

Other skills:
- `/gstack-investigate` - Investigation
- `/gstack-benchmark` - Benchmarking
- `/gstack-retro` - Retrospectives
- `/gstack-health` - Health checks
- `/gstack-upgrade` - Upgrade gstack

### Usage

Run any skill with `/gstack-<skill-name>` or use `/gstack-upgrade` to keep gstack current.
