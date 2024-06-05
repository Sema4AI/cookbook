# Due Diligence checker

## Current workflow
- I want to start using a new dependency from PyPI
- Go to PyPI and search the package (..and be aware of squatting packages)
- Check the last 3 release, release older than a year probably has CVEs which can be a no-go
- Check the readme to find potential hints to things beeing installed on the OS level (apt-get, brew,...)
- Look for the link to source and mention of license
- If there is no link to source that is the first no-go
- If there is a link to GitHub repo, the license is checked from there
  - From github I check the amount contributors, insights view
  - I check the license from here and ask chatGPT for the summary
    - I should check (but I do not) if the license text is actually the license that it states of being (devs. can edit the text to make the license invalid)
- Enough yellow / red flags triggers either searching for a replacement or "implement from scratch"

## The Problem
Why

Developers should always check the due diligence for a dependency before taking it into a software project, to identify and weed out dependencies that we should or should not rely on. Problem is that "due diligence" can mean a lot of things to a lot of people so the standards change.

What
- The dependencies are coming from NPM, PyPI and conda-forge
  - First implementation just targets PyPI
- To do my due diligence check I need the following data points:
  - Must have a clearly defined license and I need summary of the how the licensed code can be used
  - I need a link to the source repo 
  - I need know when the last update to the package was done, seeing the last three version number and their release dates is key.
  - I need to know the amount of contributors to the project in GitHub
  - I need to know the usage of the package (download statistics etc.) for the package to know the viability of the project.
  - I need to get the number of forks and stars in the github project
- Based on these I need to decide what should I do with the dependency.

Result:
- I need a recommendation on the level of good / iffy / bad, and a reasoning for that
- I need to highlight absolute no-gos like missing licenses or prohibitive license, really old releases and lax maintenance schedule.
- For the bad dependencies the actions taken are to find a better replacement or to decide if to write the functionality without a dependency.

## Runbook

Why

Developers should always check the due diligence for a dependency before taking it into a software project, to identify and weed out dependencies that we should or should not rely on. Problem is that "due diligence" can mean a lot of things to a lot of people so the standards change.

What
- The dependencies are coming from NPM, PyPI and conda-forge
  - First implementation just targets PyPI
- To do my due diligence check I need the following data points:
  - Must have a clearly defined license and I need summary of the how the licensed code can be used
  - I need a link to the source repo 
  - I need know when the last update to the package was done, seeing the last three version number and their release dates is key.
  - I need to know the amount of contributors to the project in GitHub
  - I need to know the usage of the package (download statistics etc.) for the package to know the viability of the project.
  - I need to get the number of forks and stars in the github project
- Based on these I need to decide what should I do with the dependency.

Result:
- I need a recommendation on the level of good / iffy / bad, and a reasoning for that
- I need to highlight absolute no-gos like missing licenses or prohibitive license, really old releases and lax maintenance schedule.
- For the bad dependencies the actions taken are to find a better replacement or to decide if to write the functionality without a dependency.

How:
 - Firstly scan the package based on its name and get the PyPi metadata using `get_metadata`
 - Then get the full Snyk page using `parse_snyk`, the information on the previous step is getting the priority, but data that isn't coming from there, specially Github URL and Security Information and CVEs, will be taken from this step
 - Last step will be to get the Github Information, for that you will need to call the `get_repository` with the Github URL and afterwards the `repository_releases` with the `releases_url` property that is included in get_repository return data. These will return all the relevant Github information that needs to be appended to the final report.