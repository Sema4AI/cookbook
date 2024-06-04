# Due Diligence checker

## Current workflow
- TODO

## The Problem
Why
- I need to do due diligence for different dependencies in software project to identify and weed up dependencies that we should or should not rely on.

What
- The dependencies are coming from NPM, PyPI and conda-forge
- To do my due diligence check I need th following data points
  - Must have a clearly defined license and I need summary of the how the licensed code can be used
  - I need a link to the source repo 
  - I need know when the last update to the package was done, seeing the last three version number and their release dates is key.
  - I need to know the amount of contributors to the project in GitHub
  - I need to know the download statistics for the package.
  - I need to get the number of forks and stars in the github project
- Based on these I need to decide what should I do with the dependency.

Result:
- I need a recommendation on the level of good / iffy / bad, and a reasoning for that
- I need to highlight absolute no-gos like missing licenses or prohibitive license, really old releases and lax maintenance schedule.
- For the bad dependencies the actions taken are to find a better replacement or to decide if to write the functionality without a dependency.







