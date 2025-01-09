# Pixi - a Photo Sharing API
Intentionally vulnerable NodeJS API designed for users to share photos by uploading, viewing, and/or deleting pictures. Contains many common OWASP API Top 10 vulnerabilities.

## 42Crunch API Inventory, Static & Dynamic Security Testing
GitHub Actions is enabled on this repository with the following 42Crunch plugins:
1. ### 42Crunch - API Static Security Testing
   Discover, inventory, and analyze API quality\
   GitHub Actions - https://github.com/marketplace/actions/42crunch-rest-api-static-security-testing


2. ### 42Crunch - API Dynamic Security Testing
   Dynamically analyze API implementation for security risks and OWASP API Top 10 vulnerabilities\
   Docker - https://hub.docker.com/r/42crunch/scand-agent


3. Github Advanced Security (GHAS) code scanning integration is enabled

### OpenAPI (Swagger) Specification:
`OASFiles/pixi.json`

### Source code (NodeJS):
`app/api-server.js`

## Purpose
To demonstrate 42Crunch API Security Testing on the Pixi Photo Sharing API.

## How to use 
Fork this repository and use the predefined integration directly.

## GHAS Code Scanning
Code scanning results are visible under the Security tab. You must have code scanning enabled in your organization.
