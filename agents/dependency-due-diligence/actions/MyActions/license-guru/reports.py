import anthropic


def get_template_html_wrap(content: str):
    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        <div class="p-6 sm:p-10 max-w-4xl mx-auto">
            <div class="grid gap-6">
                {content}
            </div>
        </div>
    </body>
    </html>
    """


def generate_template(client: anthropic.Anthropic, prompt: str, example: str) -> str:
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        temperature=0,
        system=f"""
Write a HTML card that contains the following information:
- Title: Python Dependency Audit Report
- Description: A comprehensive review of the project's Python dependencies.

### Content example
{example}
""",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
    )

    return message.content[0].text


content_mock = """
<div class="rounded-lg border bg-card text-card-foreground shadow-sm w-full max-w-3xl" data-v0-t="card">
  <div class="flex flex-col space-y-1.5 p-6">
    <h3 class="whitespace-nowrap text-2xl font-semibold leading-none tracking-tight">
      Due Diligence Report: Python Package
    </h3>
  </div>
  <div class="p-6 grid gap-6">
    <div class="grid gap-2">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium">License</h2>
        <div class="inline-flex w-fit items-center whitespace-nowrap rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
          MIT
        </div>
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        The MIT License is a permissive open-source license that allows for free use, modification, and distribution
        of the package, even for commercial purposes, as long as the original copyright and license notice are
        included.
      </p>
    </div>
    <div class="grid gap-2">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium">Source Repository</h2>
        <a class="text-blue-600 hover:underline" href="#">
          GitHub
        </a>
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        The source code for this Python package is hosted on GitHub, allowing for easy collaboration, issue
        tracking, and contribution.
      </p>
    </div>
    <div class="grid gap-2">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium">Version History</h2>
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="h-4 w-4"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span>Last 3 Versions</span>
          </div>
        </div>
      </div>
      <div class="grid gap-2">
        <div class="flex items-center justify-between">
          <div>
            <div class="font-medium">v2.3.1</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">June 15, 2023</div>
          </div>
          <div>
            <div class="font-medium">v2.2.0</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">April 22, 2023</div>
          </div>
          <div>
            <div class="font-medium">v2.1.3</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">February 10, 2023</div>
          </div>
        </div>
      </div>
    </div>
    <div class="grid gap-2">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium">Contributors</h2>
        <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>25 Contributors</span>
        </div>
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        The project has a healthy community of contributors on GitHub, indicating active development and
        maintenance.contributors on GitHub,
      </p>
    </div>
    <div class="grid gap-2">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium">Usage Statistics</h2>
        <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" x2="12" y1="15" y2="3"></line>
          </svg>
          <span>1.2M Downloads</span>
        </div>
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        The package has a significant number of downloads, suggesting widespread adoption and usage in the Python
        community.
      </p>
    </div>
    <div class="grid gap-2">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium">GitHub Engagement</h2>
        <div class="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
          <div class="flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="h-4 w-4"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            <span>12.3K Stars</span>
          </div>
          <div class="flex items-center gap-2"></div>
        </div>
      </div>
    </div>
  </div>
</div>
"""
