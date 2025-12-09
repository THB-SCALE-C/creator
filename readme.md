# Creator

Creator is the SCALE-C content generation and packaging module. It wraps a DSPy workflow plus templated assembly so learning units can be produced programmatically and exported as H5P packages for delivery in SCALE-C.

## Installation
- Requires Python 3.12+
- Set `OPENROUTER_API_KEY` in your environment for the default LM provider (OpenRouter).

## Quick start
```python
import dspy
from creator import Creator
from creator.dspy_components.test import SingleChoice

class LearningUnit(dspy.Signature):
    topic: str = dspy.InputField()
    title: str = dspy.OutputField()
    slides: list[SingleChoice] = dspy.OutputField()

creator = Creator(
    signature_class=LearningUnit,
    instructions="Keep the language simple and engaging."
)

unit = creator.create_unit("phishing basics")
package_path = creator.assemble_unit(output_dir=".out", out_name="unit.h5p")
print(f"H5P ready at {package_path}")
```
- `Creator.create_unit` runs the DSPy predictor to generate a typed learning unit.
- `assemble_unit` transforms the prediction into H5P content via the unit assembler.
- Prefer class-based signatures, but you can also pass `signature_json` or a DSPy `Module` via `module_predictor`.

## Components
- `creator.content_creator` builds and runs DSPy predictors (optionally with chain-of-thought).
- `creator.unit_assembler` renders generated slides into H5P assets (configuration in `unit_assembler/config.yml`).
- `creator.llm` provides `create_openrouter_lm` if you need a standalone LM instance.

## Notes for SCALE-C integration
- The package is importable as `creator` and keeps artifacts under `.out/` by default.
- You can inspect `Creator.system_prompt`, `Creator.raw_response`, or `Creator.history` for debugging generation traces.
