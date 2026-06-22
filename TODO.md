# TODO - Fix ephemeral storage / bundle size error

- [ ] Update repo to avoid bundling large data at build time (Docker image/Streamlit packaging)
  - [ ] Verify `.dockerignore` and add missing patterns (sqlite/db + persistent chroma dir)
  - [ ] Ensure Streamlit/packaging doesn’t include heavy `src/data/**` (add to `.gitignore` + consider removing from repo)
- [ ] Ensure runtime data is volume-mounted, not copied into the image
- [ ] If still failing on Streamlit Cloud bundling: adjust deployment packaging (gitignore / remove large files)
- [ ] Commit changes to GitHub with a new branch

