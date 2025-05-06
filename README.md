# Migration Task

This repository provides a Python-based solution for migrating data from one project in a given organization to another project in another organzation on  Azure DevOps board. It includes a configurable script that reads data from the source project and migrates it to the destination project.

## Features

- **Configurable Parameters**: Easily set up your Azure storage details and file paths using the `configuration.json` file.
- **Manual workflow**: Includes a `_workflow_dispatch_` trigger to run migration on whim. 
- **Seamless migration**: Migrates everything including the history of azure devops board.

## Prerequisites

- SOURCE_PAT & DESTINATION_PAT tokens with (**Administrator priviliges** in both source and destination project), configured in the repository secret.

## Technologies used

- Python 3.x
- Naked agility (https://github.com/nkdAgility/azure-devops-migration-tools)

## Installation

1. **Fork the Repository**:

   Click the **Fork** button at the top right of this page to create a copy of this repository under your own GitHub account.

2. **Clone Your Fork**:

   Replace `your-username` with your actual GitHub username:

   ```bash
   git clone https://github.com/your-username/migration-task.git
   cd migration-task
   
3. **Access configuration.json and configure accoriding to requirement**:
   ```bash
   vim configuration.json #or nano configuration.json
   ```
   
4. **Edit .github/workflows/main.yaml for modifying event trigger**:
   ```bash
   vim .github/workflows/main.yaml #or nano .github/workflows/main.yaml
   ```
   
5. **Commit and push to GitHub**
   ```bash
   git commit -m "commit message"
   git push
   ```
   
## Perfomring Migration

- Open your github repo -> Go to the repository -> Actions Tab -> select the workflow -> Run Workflow -> provide input paramters.
   
