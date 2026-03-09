# Codex Super Prompt --- Global IO Internship Scraper (Enhanced Version)

This document is an **enhanced version** of the Codex project prompt for
generating a full open‑source system that crawls international
organization internship opportunities.

You can feed this file directly into Codex / Cursor / VSCode AI coding
agents.

------------------------------------------------------------------------

## PROJECT OBJECTIVE

Build a **fully automated open‑source platform** that:

1. Crawls internship and early‑career positions from **international
    organizations worldwide**
2. Runs automatically **once per day**
3. Publishes results **daily at 10:00 Beijing Time**
4. Detects **new positions added each day**
5. Maintains **historical archives**
6. Generates a **public web dashboard**
7. Runs automatically via **GitHub Actions**
8. Is designed as a **high‑quality open source project**

The project must be runnable locally and deployable via GitHub Pages.

------------------------------------------------------------------------

## LOCAL PROJECT DIRECTORY

All files must be generated under:

C:`\Users`{=tex}`\hp074`{=tex}`\Desktop`{=tex}`\io`{=tex}-career

------------------------------------------------------------------------

## TARGET ORGANIZATIONS

The crawler should prioritize major international organizations (There is also a pdf I give it to you for reference)
including:

### United Nations System

Examples:

UN Secretariat\
UNDP\
UNICEF\
UNESCO\
WHO\
FAO\
ILO\
UN Women\
WFP\
UNHCR\
UNFPA\
UNOPS

The architecture must allow **all UN system entities to be added
easily**.

------------------------------------------------------------------------

### Major International Financial Institutions

World Bank Group\
IMF\
Asian Development Bank\
African Development Bank\
Inter‑American Development Bank\
European Bank for Reconstruction and Development

------------------------------------------------------------------------

### Global Governance Organizations

OECD\
WTO\
IOM\
ICRC\
IFRC\
Council of Europe\
European Commission traineeships

------------------------------------------------------------------------

### Regional Organizations

African Union\
ASEAN Secretariat\
APEC Secretariat\
Organization of American States

------------------------------------------------------------------------

## DATA FIELDS

Every position should be normalized to the following schema:

record_id\
org_name\
org_group\
job_title\
job_type\
location\
country_or_region\
deadline\
posted_date\
job_url\
source_url\
source_type\
summary\
language\
scraped_at\
scraped_date_bj\
is_new_today\
last_seen_date\
status

------------------------------------------------------------------------

## DATA OUTPUTS

Each run must produce:

### Latest dataset

CSV\
JSON\
Markdown\
Excel (optional)

Stored in:

data/processed/latest/

------------------------------------------------------------------------

### Daily new positions

Stored in:

data/processed/daily_new/

Example filename:

2026-03-09_new_positions.txt

Example record:

\[Organization\] UNICEF\
\[Position\] Communication Internship\
\[Location\] New York\
\[Deadline\] 2026‑03‑20\
\[Link\] https://example.com\
--------------------------------------------------

------------------------------------------------------------------------

## WEBSITE REQUIREMENTS

Generate a **minimal but professional public site**.

Features:

Search bar\
Organization filters\
Job type filters\
Highlight "New Today" positions\
Show last update time (Beijing time)

Design requirements:

Clean layout\
Modern typography\
Mobile responsive\
Fast loading\
GitHub Pages compatible

Files:

site/index.html\
site/style.css\
site/script.js

------------------------------------------------------------------------

## AUTOMATION

Use **GitHub Actions**.

Schedule:

Beijing 10:00\
UTC 02:00

Workflow:

Install dependencies\
Run crawler\
Generate outputs\
Update website data\
Commit changes\
Deploy GitHub Pages

------------------------------------------------------------------------

## PROJECT STRUCTURE

The generated repository must contain:

io-career/

README.md\
CHANGELOG.md\
LICENSE\
requirements.txt\
pyproject.toml

sources/\
official_sources.yaml\
aggregator_sources.yaml

docs/\
PROJECT_OVERVIEW.md\
ARCHITECTURE.md\
DATA_SCHEMA.md\
DEPLOYMENT.md\
SOURCES.md

src/io_career/

fetchers/\
parsers/\
pipeline/\
utils/

data/

raw/\
processed/\
archive/

site/

scripts/

tests/

.github/workflows/

daily_update.yml\
deploy_site.yml

------------------------------------------------------------------------

## COMMAND LINE INTERFACE

The system must support commands such as:

python -m io_career.main run\
python -m io_career.main validate-sources\
python -m io_career.main export-site\
python -m io_career.main compare

------------------------------------------------------------------------

## CORE FUNCTIONAL MODULES

The project should include:

Source registry\
Crawler engine\
Parser system\
Data normalization\
Duplicate detection\
Daily diff detection\
Exporter\
Website data generator

------------------------------------------------------------------------

## SCRAPING STRATEGY

Support:

Static HTML scraping\
JSON / API endpoints\
Dynamic rendering (Playwright when necessary)

The crawler should:

Respect rate limits\
Handle failures gracefully\
Log errors

------------------------------------------------------------------------

## VERSIONING

Initial version:

v0.1.0

Use semantic versioning.

Maintain CHANGELOG.md.

------------------------------------------------------------------------

## DOCUMENTATION REQUIREMENTS

The repository must include:

README.md\
docs/OPERATION_GUIDE.md\
docs/ARCHITECTURE.md\
docs/DATA_SCHEMA.md\
docs/SOURCES.md\
docs/DEPLOYMENT.md

Documentation must explain:

Installation\
Local execution\
Adding new sources\
Running crawlers\
GitHub deployment

------------------------------------------------------------------------

## EXTENSION CAPABILITIES

The architecture should allow future expansion: (but without API at this stage as a priority)

Telegram notifications\
Email alerts\
REST API\
Full web application

------------------------------------------------------------------------

## QUALITY REQUIREMENTS

The generated project must:

Run locally\
Produce structured output\
Generate daily new position files\
Generate website data\
Deploy successfully via GitHub Pages\
Be well documented

------------------------------------------------------------------------

## FINAL INSTRUCTION

Do NOT only provide architecture diagrams or pseudocode.

Generate:

Full directory structure\
Working crawler code\
Configuration files\
Website files\
GitHub Actions workflows\
Documentation

All files must be created inside:

C:`\Users`{=tex}`\hp074`{=tex}`\Desktop`{=tex}`\io`{=tex}-career

------------------------------------------------------------------------

## END OF PROMPT
