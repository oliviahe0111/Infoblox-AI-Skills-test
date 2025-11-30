# cons.md (Template)
List at least 3 concrete limitations and tradeoffs of your approach.

1. Tradeoff: Trusting LLM for Guessed Data

Issue: When deterministic rules can’t determine a field, we rely on the LLM to fill in the gap.
Impact: While the LLM can provide a reasonable guess, there’s always a risk that this “guessed” data is inaccurate. The tradeoff is balancing deterministic reliability with LLM flexibility.
Mitigation: Feed the LLM as much context and up-to-date data as possible to improve accuracy.

2. Data Staleness in LLM References

Issue: The LLM relies on internal reference data (like team rosters) that may not always be up-to-date.
Impact: This can lead to outdated or incorrect owner/team assignments if the reference data lags behind organizational changes.
Mitigation: Regularly refresh the LLM’s reference data.

3. Model Hallucination Risk

Issue: Even at a low temperature setting, the LLM might generate plausible but incorrect outputs.
Impact: Incorrect values may appear valid and require manual correction.
Mitigation: Closely monitor outputs and refine prompts to reduce ambiguity.

4. Dependence on Input Data Quality

Issue: The LLM’s accuracy depends on the quality of the raw input fields.
Impact: Poor or misleading input can lead to inaccurate LLM interpretations.
Mitigation: Ensure input data is as clean and clear as possible before processing.