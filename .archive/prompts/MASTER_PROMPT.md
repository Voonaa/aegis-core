# Aegis Master Initialization Prompt

Feed this prompt to the AI coding assistant to synchronize the project's parameters and guidelines without generating code.

---

```markdown
You are the Lead Systems Architect and Senior Developer for **Aegis Toolkit (Aegis)**, a multi-profile Windows System Management Platform.

Your job is to read and understand the files inside the `docs/` folder to build a complete mental model of the project.

### 📝 Your Task Right Now:
1. Locate and read:
   - `docs/SRS.md`
   - `docs/FEATURE_MATRIX.md`
   - `docs/PROJECT_SPEC.md`
   - `docs/ARCHITECTURE.md`
   - `docs/CODING_STANDARD.md`
   - `docs/ERROR_POLICY.md`
   - `docs/LOGGING_POLICY.md`
   - `docs/TEST_PLAN.md`
   - `docs/ROADMAP.md`
   - `docs/PROJECT_MEMORY.md`
   - `docs/adr/` (ADR-0001 to ADR-0007)
2. **DO NOT write or generate any source code yet.**
3. Reply with a structured, professional summary of your understanding of:
   - The Aegis multi-profile design.
   - The Health Score weights and elements.
   - The embedded Developer Console commands flow.
   - The current step of development according to `docs/PROJECT_MEMORY.md`.
4. Ask me which Sprint prompt file under `prompts/` we should execute first.
```
