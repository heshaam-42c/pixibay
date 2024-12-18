# Pixi Photo Sharing API
Intentionally vulnerable NodeJS API designed for users to share photos by uploading, viewing, and/or deleting pictures. Contains many common OWASP API Top 10 vulnerabilities.

## Purpose
To demonstrate 42Crunch API Security Testing on the Pixi Photo Sharing API.

### OpenAPI Specification:
`OASFiles/pixi.json`

### NodeJS:
`app/api-server.js`

## 42Crunch API Inventory & Security Testing
This public repository is enhanced with:
1. 42Crunch API Inventory & Static Security Testing
2. 42Crunch API Dynamic Security Testing
3. Github Advanced Security (GHAS) code scanning integration

## Included Dependencies
The following GitHub Actions plugin is included for API Inventory & Static Security Testing:
- 42Crunch REST API Static Security Testing - https://github.com/marketplace/actions/42crunch-rest-api-static-security-testing

The following Docker image is used for API Dynamic Security Testing:
- 42Crunch ScanD Agent docker image - https://hub.docker.com/r/42crunch/scand-agent

## How to use 
Fork this repository and use the predefined integration directly.

## GHAS Code Scanning
Code scanning results are visible under the Security tab. You must have code scanning enabled in your organization.
