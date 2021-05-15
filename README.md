# Lecture bot &middot; [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/beeklz/teams-lecture-bot/blob/main/LICENCE)

A Microsoft Teams bot will automatically join a meeting and record it.

## Requirements

- Chrome
- [Selenium](https://github.com/SeleniumHQ/selenium)
- [Webdriver manager](https://github.com/bonigarcia/webdrivermanager)

## Getting started

- Step 1:
  Install dependencies from [requirements.txt](requirements.txt):

  ```bash
  python3 -m pip install -r requirements.txt
  ```

- Step 2:
  Create your environment file in the root directory:

  ```bash
  touch .env
  ```

- Step 3:
  Set up your environment `.env`:

  ```text
  EMAIL=
  PASSWORD=

  TEAM=
  ```

## Usage

- Execute Python script:

  ```bash
  python3 -m bot
  ```

## Licensing

Licenced by MIT licence.
