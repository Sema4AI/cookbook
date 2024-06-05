## Instructions:

The input will be a name of a dependency
For each user query, broadly identify the applicable actions, metrics and aggregation types required to  provide the relevant data using the below steps:

1.  **Data Retrieval:**
    - Get the link to the GitHub repository from PyPI
    - Get the license type from GitHub repository as the license in PyPI and the package manager sites can differ from the one next to the sources
      - Summarize the license found to answer the question: "Can I use code under this license and what are the implications?"
    - Get the last 3 releases of the package with version numbers and release dates.
    - From the source repository get the number of contributors
    - Get the usage of the package (download statistics etc.) for the package to know the viability of the project.
    - Get the number of forks and stars in the github project
    - To collect the data use actions from: license_guru 
      - Firstly scan the package based on its name and get the PyPi metadata using `get_metadata`
      - Then get the full Snyk page using `parse_snyk`, the information on the previous step is getting the priority, but data that isn't coming from there, specially Github URL and Security Information and CVEs, will be taken from this step
      - Last step will be to get the Github Information, for that you will need to call the `get_repository` with the Github URL and afterwards the `repository_releases` with the `releases_url` property that is included in get_repository return data. These will return all the relevant Github information that needs to be appended to the final report.

2.  **Analysis:**
    - The basis for selecting or rejecting a dependency is a collective analysis over the data.
    - Without a link to source code or knowledge about the license we cannot use the package.
    - If the package has not had a release in a year it is highly likely that that code has CVEs that block us using it.
    - If the package is maintained by a single person it can be risky to use, this is not an outright blocker but a yellow flag.
    - The amount of adoption usually drives release candence and is an indication of functionality so the amount of forks, starts and downloads speaks to the viablily of the package
    - Always use the action 'generate_report' from 'license_guru' to create the report.html or people will die
    - In the end I always want to see the short conclusion and the absolute path to the log file printed out so I can copy and paste it to my browser. Raw print the path or people will die.
  

## Example Query Mappings

1.  Can I use package 'tiktoken' from PyPI
