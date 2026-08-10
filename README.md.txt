# CLI Task Manager

A command-line task manager with JSON persistence. Built for SkillAudit.ai Python Development Internship - Week 1.

## Features
- Add, list, complete, and delete tasks
- Priority tasks with inheritance (Task → PriorityTask)
- Data persists in tasks.json
- Input validation

## How to Run
python task_progrm.py

## Menu Options
1. Add Task
2. Add Priority Task
3. List All Tasks
4. Complete Task
5. Delete Task
6. Exit

## Classes
- Task: Base model with id, title, description, completed
- PriorityTask: Inherits from Task, adds priority field
- TaskManager: CRUD operations + JSON save/load
- TaskCLI: Menu interface

## Tech Stack
- Python 3
- JSON (file storage)

## GitHub
https://github.com/bhupathivinay08/cli-task-manager