# TODO - Fix ephemeral storage / bundle size error

- [ ] Identify whether deployment is via Streamlit Cloud (Python bundle) or Docker (image build)
- [ ] Remove large persistent data from repo and ensure it is excluded from bundling
  - [ ] Ensure `src/data/**` is not committed (raw_documents, embeddings, memory, sqlite/db)
  - [ ] Ensure `.gitignore` and `.dockerignore` exclude these directories
- [ ] Update Dockerfile to avoid copying excluded/unnecessary large folders
  - [ ] Prefer `COPY src ./src` and copy only required small assets
- [ ] Verify local build: `docker build .` (should stay small)
- [ ] Re-deploy and confirm bundle size < 500MB

- [ ] If still failing, inspect the deployment logs to locate the biggest bundled folder/file

