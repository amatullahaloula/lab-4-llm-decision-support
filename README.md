# Lab 4 — LLMs and Prompt Engineering for Decision Support

A decision-support system for a (fictional) microfinance loan officer in Ghana. Given a
pile of free-text loan application letters, the system:

1. **Summarizes** each application into a short, factual brief.
2. **Extracts** structured data (JSON) that a downstream system could store.
3. Produces a **decision-support brief** (strengths / risks / missing info / next step) —
   while keeping a human loan officer firmly in the loop for the actual approve/reject call.

The notebook also **evaluates** the system: extraction accuracy against gold-standard
labels, run-to-run reliability at different temperatures, and robustness under
hallucination-probing (asking about details the letter never mentions, and feeding it
irrelevant text).

## Repository contents

| File | Purpose |
|---|---|
| `Lab_4_LLM_Decision_Support.ipynb` | Main notebook: all sections, code, and written reasoning. |
| `prompts.py` | Final prompt templates (`SUMMARY_*`, `EXTRACT_*`, `BRIEF_*`), importable as code. |
| `prompts.md` | Version history of the prompts — what changed between versions and why. |
| `requirements.txt` | Python dependencies. |
| `AI_Use_Declaration_Form.docx` | Completed AI-use declaration for this submission. |

## Setup

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a free-tier API key from **Google Gemini** (or adapt `ask_llm()` in the notebook to
   another OpenAI-compatible provider such as Groq).
3. **Never hard-code or commit your API key.**
   - **Locally:** put it in a `.env` file (already covered by `.gitignore`) and load it with
     `python-dotenv`.
   - **Google Colab:** use the Secrets panel (key icon) and read it with
     `google.colab.userdata.get("GeminiAPIKey")`.
4. Run the notebook top to bottom: `Kernel → Restart & Run All`.

## How it works

- `ask_llm(user_prompt, system_prompt, temperature, max_tokens)` wraps the Gemini API call
  used throughout the notebook.
- **Summarization** (`SUMMARY_SYSTEM_V2` / `SUMMARY_PROMPT_V2`) turns a letter into a 3–4
  sentence factual brief.
- **Extraction** (`EXTRACT_SYSTEM` / `EXTRACT_EXAMPLE`, temperature = 0) returns strict JSON
  for six fields: `applicant_name`, `amount_ghs`, `purpose`, `monthly_profit_ghs`,
  `has_collateral_or_guarantor`, `repayment_months`.
- **Brief generation** (`BRIEF_SYSTEM` / `BRIEF_PROMPT`) combines the letter and the
  extracted JSON into a four-part brief. The prompt explicitly forbids the model from
  outputting "approve" / "reject" — the system supports the decision, it does not make it.

See `prompts.md` for the full reasoning behind each prompt's design.

## Evaluation summary

The notebook's Section 4 measures:

- **Extraction accuracy** against three gold-labeled letters (`GOLD` dict), field by field.
- **Reliability**, by running extraction 5× at temperature 0 vs. temperature 1.0 on the same
  letter and comparing how often the JSON output is identical.
- **Hallucination probing**, by (a) asking about a detail not present in a letter, and
  (b) feeding the extractor irrelevant, non-loan-related text.

Full results and discussion are in the notebook's Section 4 cells and reasoning answers.

## AI use declaration

This submission's AI-use declaration is in `AI_Use_Declaration_Form.docx`.
