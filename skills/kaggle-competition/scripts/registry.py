"""Registry of the Kaggle competitions this harness drives.

One dict per competition, keyed by a short local `key` you use on the command
line (`python harness.py download <key>`). The harness reads `slug` (the API
identifier in the competition URL), `title`, and `rules_url`; the other fields
(`task`, `id_col`, `target_col`, `metric`) are notes for your own model code.

Add a competition = add an entry here (a pluggable seam — you never edit the
harness). Two examples below: a CSV-submission getting-started competition and
a code-competition that submits via a Kaggle kernel.

Prerequisite the API cannot do for you: click *Join / I Understand and Accept*
on each competition's rules page (`rules_url`) once — the API rejects downloads
and submissions until the rules are accepted on the website.
"""

COMPETITIONS = {
    # --- CSV path: a local model writes submission.csv, harness uploads it ---
    "titanic": {
        "slug": "titanic",
        "title": "Titanic - Machine Learning from Disaster",
        "task": "binary-classification",
        "id_col": "PassengerId",
        "target_col": "Survived",
        "metric": "accuracy",
        "rules_url": "https://www.kaggle.com/competitions/titanic/rules",
    },
    # --- Kernel path: scoring code runs on Kaggle infra (often GPU) ---
    # Replace with a real code-competition slug. Drive it with:
    #   python harness.py kernel-init <key> --gpu
    #   ... edit competitions/<key>/kernel/notebook.ipynb ...
    #   python harness.py kernel-push <key>
    #   python harness.py kernel-status <key>
    #   python harness.py kernel-output <key>
    "example-code-comp": {
        "slug": "your-code-competition-slug",
        "title": "Example Code Competition",
        "task": "code-competition",
        "metric": "tbd",
        "rules_url": "https://www.kaggle.com/competitions/your-code-competition-slug/rules",
    },
}
