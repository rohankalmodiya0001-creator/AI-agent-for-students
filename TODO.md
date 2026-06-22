# TODO - Fix ephemeral storage / bundle size error

- [ ] Update repo to avoid bundling large data at build time (Docker image/Streamlit packaging)
  - [x] Inspect and update `.dockerignore`
  - [ ] Confirm any other large folders that are not ignored (e.g., `src/data/*`, `*.tar.gz`, etc.)
- [ ] Ensure runtime data is volume-mounted, not copied into the image
  - [x] Add comment clarifying data should be mounted at runtime in `Dockerfile`
- [ ] Rebuild/redeploy (after cleaning build cache)
- [ ] If still failing on Streamlit Cloud bundling: adjust deployment packaging (gitignore / remove large files)

