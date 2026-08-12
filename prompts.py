"""
prompts.py
Lab 4 - LLMs and Prompt Engineering for Decision Support

Final prompt templates used by the microfinance loan decision-support system.
Kept here (instead of buried inline in the notebook) because prompts ARE code:
they need version history and review just like any other logic.

See prompts.md in this repo for the version history / how each prompt evolved.
"""

# ---------------------------------------------------------------------------
# Component 1: Summarization
# ---------------------------------------------------------------------------
# V1 was a bare one-liner. It produced summaries that added details not in
# the original letter (hallucination) and had no consistent structure.
# V2 adds a system prompt that fixes the persona, the target length, and
# -- critically -- an explicit "do not invent details" instruction.

SUMMARY_PROMPT_V1 = "Summarize this: {letter}"

SUMMARY_SYSTEM_V2 = """You are an assistant to a microfinance loan officer in Ghana.
Summarize loan application letters factually and neutrally in 3-4 sentences.
Do not invent, guess, or add any detail that is not explicitly stated in the letter."""

SUMMARY_PROMPT_V2 = "Summarize this loan application:\n\n{letter}"

# ---------------------------------------------------------------------------
# Component 2: Structured extraction (JSON)
# ---------------------------------------------------------------------------
# The system prompt pins down the exact schema (six named keys) and forces
# nulls instead of guesses for missing fields. A one-shot example is given
# to lock the output format -- the example is deliberately NOT one of the
# six letters being processed, so the model can't just memorize/leak the
# answer instead of performing the extraction.
#
# NOTE: EXTRACT_EXAMPLE is combined with the letter text using string
# concatenation (+), not str.format() -- the literal { } braces in the
# example JSON would otherwise be parsed as format fields and raise a
# KeyError.

EXTRACT_SYSTEM = """You extract structured data from microfinance loan application letters.
Return ONLY a JSON object with exactly these keys:
applicant_name (string), amount_ghs (number), purpose (string),
monthly_profit_ghs (number or null), has_collateral_or_guarantor (boolean), repayment_months (number or null).
If a field is not stated in the letter, use null. Do not guess."""

EXTRACT_EXAMPLE = """Example letter:
"My name is Ama Serwaa. I run a small chop bar in Tema and need GHS 6000 to renovate my kitchen.
I make about GHS 700 profit a month. My brother will guarantee the loan. I can pay GHS 400 monthly for 15 months."

Example output:
{"applicant_name": "Ama Serwaa", "amount_ghs": 6000, "purpose": "renovate kitchen",
"monthly_profit_ghs": 700, "has_collateral_or_guarantor": true, "repayment_months": 15}"""


def build_extract_prompt(letter_text: str) -> str:
    """Build the extraction prompt.

    Uses concatenation rather than .format() -- see note above about the
    literal JSON braces in EXTRACT_EXAMPLE.
    """
    return EXTRACT_EXAMPLE + "\n\nNow extract from this letter:\n\n" + letter_text


# ---------------------------------------------------------------------------
# Component 3: Decision-support brief
# ---------------------------------------------------------------------------
# Combines the letter + the extracted JSON into a structured brief for the
# loan officer. The system prompt explicitly forbids the model from
# outputting "approve"/"reject" -- the model may support the decision, it
# must never make it. This is both a practical safeguard (final say stays
# with a human loan officer) and an ethical one (an automated approve/reject
# call could be unfair or biased and directly affects someone's access to
# credit).

BRIEF_SYSTEM = """You are an assistant to a microfinance loan officer in Ghana.
Given a loan application letter and its extracted data, produce a decision-support brief with:
1. Strengths (bullet points, grounded only in the letter)
2. Risks / red flags (bullet points)
3. Missing information the officer should request
4. Suggested next step (e.g. "invite for interview", "request documents", "flag for senior review")
Never output "approve" or "reject" -- final decisions are made by a human loan officer, not you."""

BRIEF_PROMPT = "Letter:\n{letter}\n\nExtracted data:\n{extracted}\n\nProduce the brief."
