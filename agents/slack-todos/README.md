# Slack ToDos

Have you ever thought about turning your saved items from Slack into actionable ToDo events right in your Google Calendar?

We believe that you should keep your focus on one task at a time and never let distractions creep in your work day, but sometimes the priority will dictate the context switch. Therefore, we try to minimize that by encouraging you save any pending item to be solved, so you can come back later on.

This way we came with a solution that understands all your saved for later conversations, including the reasoning behind the thread replies, so they can be summarized and turned into ToDo events under your Google Calendar with an emphasis on the essential.

## Prompt example

```
Get me all the saved items newer than yesterday?
```

> Here is the saved item from your Slack channels that is newer than yesterday:
>
> General Channel
> - Message from Cosmin Poieana
> - Date: 2024-06-28
> - Content: "But this one definitely has to be saved and done: let's upgrade that truststore dep to the latest upstream."
> 
> This message contains an actionable item regarding upgrading the truststore dependency to the latest upstream version. Would you like assistance in planning this task or need further details?

```
Can you place this in my Calendar un Tuesday? I prefer morning slots.
```

> The task to upgrade the truststore dependency to the latest upstream version has been successfully scheduled for Tuesday, July 2nd, from 08:00 to 09:00. Here are the details:
>
> - Summary: Upgrade Truststore Dependency
> - Description: Task to upgrade the 'truststore' dependency to the latest upstream version as requested by Cosmin Poieana.
> - Time: 08:00 - 09:00
> 
> If you need any further adjustments or additional tasks scheduled, just let me know!

## Actions

Custom actions:

- [Todoist](./actions/)

Gallery prebuilt action packs:

- [Slack](https://github.com/Sema4AI/gallery/blob/main/actions/slack/README.md)
- [Google Calendar](https://github.com/Sema4AI/gallery/blob/main/actions/google-calendar/README.md)
