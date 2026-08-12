# Prompt Version History

Final prompt templates are in [`prompts.py`](./prompts.py). This file documents how each
one evolved and why, as required by Part 3.4 of the lab.

## 1. Summarization

| Version | Prompt | Problem it had / fixed |
|---|---|---|
| V1 | `"Summarize this: {letter}"` | No persona, no length target, no grounding instruction. Output sometimes added details that were not in the original letter (hallucination) and varied wildly in length/tone between letters. |
| V2 | System prompt fixes the persona ("assistant to a microfinance loan officer"), the target length (3-4 sentences), and adds an explicit instruction not to invent, guess, or add details not stated in the letter. | Removed the invented/incorrect details seen in V1. Output became consistently factual and scannable. |

**Why it matters:** in a loan-decision context, invented details (hallucination) could lead
directly to an incorrect or unfair lending decision, so "no invented details" is not
optional polish -- it's a correctness requirement.

## 2. Structured extraction (JSON)

Single final version — `EXTRACT_SYSTEM` + `EXTRACT_EXAMPLE`.

Key design decisions and why:
- **Schema is pinned in the system prompt** (exact key names/types) so downstream code can
  rely on a fixed shape.
- **"Use null, do not guess"** was added after observing the model fill in plausible-looking
  but fabricated values (e.g. a repayment period) when a field was missing from the letter.
- **The one-shot example is NOT one of the six letters being processed.** Using one of the
  real letters as the example risks the model pattern-matching/memorizing that specific
  answer rather than performing genuine extraction on it.
- **Built with string concatenation, not `.format()`.** The example output contains literal
  JSON braces (`{ }`), which `.format()` would misinterpret as format fields and raise a
  `KeyError`. Concatenation sidesteps this entirely.
- **Temperature = 0.** Extraction is a task with one correct answer per letter, not a
  creative task, so we want the most deterministic output the model can give.

## 3. Decision-support brief

Single final version — `BRIEF_SYSTEM` + `BRIEF_PROMPT`.

Combines the raw letter and the extracted JSON so the model has both the qualitative
narrative and the structured facts to work from. The prompt fixes a four-part output
structure (strengths / risks / missing info / suggested next step) and explicitly forbids
the model from outputting "approve" or "reject":

- **Practical reason:** the system is meant to support the loan officer's judgment, not
  replace it.
- **Ethical reason:** an automated approve/reject call could encode or amplify bias and has
  a direct, material effect on someone's access to credit.
