# ganttify

This is a thin wrapper around the Altair python visualization library
specifically for creating Gantt charts of CI pipeline results given data in
the following JSON format:

```
[
    {
        'queue': 'OPTIONAL - pandas parsable timestamp',
        'start': 'REQUIRED - pandas parsable timestamp',
        'end': 'REQUIRED - pandas parsable timestamp',
        'status': 'REQUIRED - any string other than "success" is interpreted as a failure',
        'label': 'REQUIRED - label string',
    },
    ...
]
```

This satisfies my own use cases, use at your own risk.

For more control, recommend importing the ganttify module and invoking
make\_chart from a script.
"""
