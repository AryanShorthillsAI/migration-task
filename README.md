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


# Azure DevOps Migration Tools

The Azure DevOps Migration Tools allow you to bulk edit and migrate data between Team Projects on both Microsoft Team Foundation Server (TFS) and Azure DevOps Services. Take a look at the  [documentation](https://nkdagility.com/learn/azure-devops-migration-tools/) to find out how. This project is published as [code on GitHub](https://github.com/nkdAgility/azure-devops-migration-tools/) as well as a Winget package a `nkdAgility.AzureDevOpsMigrationTools`.

**Ask Questions on Github: https://github.com/nkdAgility/azure-devops-migration-tools/discussions**

## Compatability

These tools run on Windows and support connecting to Team Foundation Server 2013+, Azure DevOps Server, & Azure DevOps Services. They support both hosted and on-premise instances and can move data between any two.

- Supports all versions of TFS 2013+ and all versions of Azure DevOps.
- You can migrate from any TFS/Azure DevOps source to any TFS/Azure DevOps target.

## What do you get?

- *Move* Work Items, Test Plans & Suits, and Pipelines between projects, collections, and even organizations.
- *Merge* multiple projects into a single project even from different organizations.
- *Split* one project into several projects even between projects, collections, and even organizations.
- *Change* Process process from Agile to Scrum or any other template.
- *Bulk edit* Work Items.

## What does this tool do?

For the most part we support moving data between ((Azure DevOps Server | Team Foundation Server | Azure DevOps Services) <=> (Azure DevOps Server | Team Foundation Server | Azure DevOps Services)) for any version greater than 2013. 

- `Work Items` (including links and attachments) with custom mappings for fields and types
	- Copy Work Items between locations with history
	- Bulk Edit in place of Work Items (Great for cleaning up data, process template changes)
	- Optionaly includes `Teams`, `Shared Queries`
- `Test Plans & Suites` 
	- Copy Test Plans & Suites between locations
	- Includes `Configurations`, `Shared Steps`, `Shared Parameters`
- `Pipelines`
	- Copy Pipelines between locations
	- excludes XAML & Classic Builds & Release
- `Processes`
	- Copy Processes between locations

**Note**: 'Locations' includes `Projects`, `Collections`, `Organizations`

**Important:** This tool is intended for experienced users familiar with TFS/Azure DevOps object models and debugging in Visual Studio. It was developed by 100+ contributors from the Azure DevOps community to handle various scenarios and edge cases. _Not all cases are supported_.

**Support Options:** Community support is available on [GitHub](https://github.com/nkdAgility/azure-devops-migration-tools/discussions). For paid support, consider our [Azure DevOps Migration Services](https://nkdagility.com/capabilities/azure-devops-migration-services/).

## Quick Links

- [Documenation](https://nkdagility.com/docs/azure-devops-migration-tools/)
- [Installation](https://nkdagility.com/learn/azure-devops-migration-tools/installation/)
- [Permissions](https://nkdagility.com/learn/azure-devops-migration-tools/permissions/)
- [Getting Started](https://nkdagility.com/learn/azure-devops-migration-tools/getting-started/)
- [Configuration Reference](https://nkdagility.com/learn/azure-devops-migration-tools/Reference/)
- [Community Support](https://github.com/nkdAgility/azure-devops-migration-tools/discussions)
- [Commercial Support](https://nkdagility.com/capabilities/azure-devops-migration-services/)
- [Change Log](https://nkdagility.com/learn/azure-devops-migration-tools/change-log/)

The documentation for the preview is on [Preview](https://nkdagility.com/docs/azure-devops-migration-tools/preview/)]

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
   
