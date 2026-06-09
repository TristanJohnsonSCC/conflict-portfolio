# Conflict Portfolio (Web)

Static portfolio site for the Communication course. Chapters are generated from the draft files in the parent `Communication` folder.

## Local preview

Open `docs/index.html` in a browser, or run a simple local server:

```bash
cd docs
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## Rebuild after editing chapters

From this folder:

```bash
python build_portfolio.py
```

## GitHub Pages setup

1. Create a new GitHub repository (for example `conflict-portfolio`).
2. Copy the contents of the `docs` folder into the repo, **or** push this whole `Conflict Portfolio` folder and use `/docs` as the Pages source.
3. On GitHub: **Settings → Pages**
4. Under **Build and deployment**, set **Source** to **Deploy from a branch**
5. Choose branch `main` and folder `/docs`
6. Save. GitHub will give you a URL like:

   `https://your-username.github.io/conflict-portfolio/`

7. Submit that link to your instructor.

## Before submitting

- Optionally add your name on the home page in `build_portfolio.py` or `docs/index.html`.
- Re-run `python build_portfolio.py` after any chapter edits.

## Included chapters

1. Birth Order
2. Attachment Style
3. Personality Type
4. Family & Culture
5. Communication Style
6. Conflict Style
7. Coping Skills
8. Resolving Conflicts
