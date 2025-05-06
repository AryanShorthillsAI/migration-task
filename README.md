# Migration Task

This repository provides solution based on naked agility for migrating data from one project in a given organization to another project in another organzation on  Azure DevOps board. It includes a configurable script that reads data from the source project and migrates it to the destination project.

## Features

- **Configurable Parameters**: Easily set up your Azure storage details and file paths using the `configuration.json` file.
- **Manual workflow**: Includes a `_workflow_dispatch_` trigger to run migration on whim. 
- **Seamless migration**: Migrates everything including the history of azure devops board.

## Prerequisites

- SOURCE_PAT & DESTINATION_PAT tokens with (**Administrator priviliges** in both source and destination project), configured in the repository secret.

## Technologies used

- Python 3.x
- Naked agility (https://github.com/nkdAgility/azure-devops-migration-tools)

![Azure DevOps Migration Tools from Naked Agility with Martin Hinshelwood](https://github.com/user-attachments/assets/997cc49f-cbe9-4f22-a8e1-49b529d0dff0)
![GitHub release](https://img.shields.io/github/v/release/nkdAgility/azure-devops-migration-tools)
![GitHub pre-release](https://img.shields.io/github/v/release/nkdAgility/azure-devops-migration-tools?include_prereleases)

[![Build Status](https://dev.azure.com/nkdagility/AzureDevOps-Tools/_apis/build/status%2FMigrationTools-CIv2?branchName=main)](https://dev.azure.com/nkdagility/AzureDevOps-Tools/_build/latest?definitionId=115&branchName=main)
![Azure DevOps tests](https://img.shields.io/azure-devops/tests/nkdagility/AzureDevOps-Tools/115?compact_message&style=plastic&logo=azuredevops&label=Tests)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=vsts-sync-migrator%3Amaster&metric=coverage)](https://sonarcloud.io/dashboard?id=vsts-sync-migrator%3Amaster)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=vsts-sync-migrator%3Amaster&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=vsts-sync-migrator%3Amaster)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=vsts-sync-migrator%3Amaster&metric=security_rating)](https://sonarcloud.io/dashboard?id=vsts-sync-migrator%3Amaster)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=vsts-sync-migrator%3Amaster&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=vsts-sync-migrator%3Amaster)
![Visual Studio Marketplace Rating](https://img.shields.io/visual-studio-marketplace/stars/nkdagility.vsts-sync-migration?logo=visualstudio)
![Chocolatey Downloads](https://img.shields.io/chocolatey/dt/vsts-sync-migrator)
[![Elmah.io](https://img.shields.io/badge/sponsored_by-elmah_io-0da58e)](https://elmah.io)

Created and maintained by [Martin Hinshelwood](https://www.linkedin.com/in/martinhinshelwood/) (http://nkdagility.com)

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
   
