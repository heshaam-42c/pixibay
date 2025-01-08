# Pixi Photo Sharing API
Intentionally vulnerable NodeJS API designed for users to share photos by uploading, viewing, and/or deleting pictures. Contains many common OWASP API Top 10 vulnerabilities.

## Purpose
To demonstrate 42Crunch API Security Testing on the Pixi Photo Sharing API.

### OpenAPI (Swagger) Specification:
`OASFiles/pixi.json`

### Source code (NodeJS):
`app/api-server.js`

## 42Crunch API Static & Dynamic Security Testing
This repository is enhanced with the following plugins:
1. GitHub Actions - 42Crunch API Static Security Testing

https://github.com/marketplace/actions/42crunch-rest-api-static-security-testing


2. Docker - 42Crunch API Dynamic Security Testing

https://hub.docker.com/r/42crunch/scand-agent


3. Github Advanced Security (GHAS) code scanning integration is enabled

## How to use 
Fork this repository and use the predefined integration directly.

## GHAS Code Scanning
Code scanning results are visible under the Security tab. You must have code scanning enabled in your organization.
