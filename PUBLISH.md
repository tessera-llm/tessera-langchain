# Publish playbook — tessera-langchain

The CI workflows in `.github/workflows/` automate the heavy lifting. To
ship a new release, you need:

1. **Repo secrets configured** (one-time setup):
   - `PYPI_TOKEN` — PyPI token scoped to `tessera-langchain` (https://pypi.org/manage/account/token/)
   - `NPM_TOKEN` — npm automation token with publish access to `@tessera-llm/langchain`

   Set both via `gh secret set NAME --repo tessera-llm/tessera-langchain` or in the GitHub Settings → Secrets and variables → Actions UI.

2. **Version bumps** in three files (must match for the release to be coherent):
   - `python/pyproject.toml` → `version = "X.Y.Z"`
   - `python/tessera_langchain/_version.py` → `__version__ = "X.Y.Z"`
   - `node/package.json` → `"version": "X.Y.Z"`

3. **CHANGELOG.md update** with the new version block + entries.

4. **Commit + push** the version bump + CHANGELOG.

5. **Create + push the release tags** — one for each ecosystem:

   ```bash
   git tag python-v0.1.0
   git tag node-v0.1.0
   git push origin python-v0.1.0 node-v0.1.0
   ```

   - `python-v*` tag triggers `publish-python.yml` → PyPI publish
   - `node-v*` tag triggers `publish-node.yml` → npm publish

   You can push them together; the two workflows run in parallel.

6. **Verify after publish:**

   ```bash
   curl -sI https://pypi.org/pypi/tessera-langchain/X.Y.Z/json
   curl -sI https://registry.npmjs.org/@tessera-llm/langchain/X.Y.Z
   ```

   Both should return `200 OK`. PyPI usually indexes within 1-2 minutes; npm within 10-30 seconds.

7. **GitHub Release object** — after both publishes succeed, create a Release object on GitHub pointing at the `python-v*` tag (or the `node-v*` tag — either works as the canonical release marker for the version):

   ```bash
   gh release create python-v0.1.0 \
     --title "v0.1.0 — first public release" \
     --notes-file <(awk '/^## \[0\.1\.0\]/{flag=1} /^## \[/&&!/0\.1\.0/{flag=0} flag' CHANGELOG.md)
   ```

   The Release object is what awesome-list maintainers and analytics tools index — without it, the version on PyPI / npm looks orphaned.

8. **Announce** — see `marketing/awesome-list-prs-queue.md` in the main tessera-ai monorepo for the awesome-list submission flow. Single-package promotion playbook: post on the founder Twitter, drop a follow-up Discord message in any LangChain-related communities you participate in.

## Common failure modes

- **`twine check` fails:** typically a malformed README on PyPI side. Run `python -m build && python -m twine check dist/*` locally before tagging.
- **`npm publish` fails with `403 Forbidden`:** the `NPM_TOKEN` doesn't have publish access. Regenerate with `npm token create --read-only=false` and update the repo secret.
- **`PyPI` rejects with "Filename has already been used":** you're trying to re-publish the same version. Bump the version number; PyPI does not allow re-uploads of the same version even after deletion.

## Versioning policy

Semver. Wire format compatibility across minor versions (0.X.Y). Breaking changes only on major bumps. Python and Node move together (same version string in `pyproject.toml` and `package.json`).
