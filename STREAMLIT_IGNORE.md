# Streamlit ephemeral bundle size fix

The deployment error is caused by the build/bundler packaging local directories that are not part of the source code.

## What to do
1. Delete your local virtual environment before bundling/building:
   - delete `.venv/`

2. Ensure Streamlit bundling ignores common large dirs (virtualenv, caches, local vector stores).

> Note: Streamlit Cloud packaging behavior is controlled by its own ignore rules.
> If your platform supports it, configure “files to exclude”/ignore patterns accordingly.

## Repo-side ignore files
- `.gitignore` and `.dockerignore` already exclude:
  - `.venv/`, `venv/`
  - `src/data/embeddings/`, `src/data/raw_documents/`
  - sqlite/db artifacts

## Recommended additional step
If your repo contains an existing local vector store or artifacts, remove them from the working tree before deployment.


