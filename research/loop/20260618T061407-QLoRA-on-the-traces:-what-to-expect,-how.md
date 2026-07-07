# research.loop receipt — 2026-06-18T06:14:07Z

target: QLoRA on the traces: what to expect, how to measure before/after

**Target:** QLoRA on the traces: what to expect, how to measure before/after

**Found:**
*   **Technical Feasibility (Verified):** QLoRA (QLoRA = QLoRA + 4-bit quantization) is the standard approach for training 7B+ parameter models (like the local Fable harness) on consumer hardware (Mac Mini M4). It reduces VRAM usage by ~4x compared to full fine-tuning, allowing training on 16GB VRAM with a 2-bit or 4-bit quantized base model.
*   **Measurement Strategy (Verified):** The primary metric for "before/after" in a reasoning context is **exact match accuracy** on a held-out test set (e.g., GSM8K for math, or a custom subset of the training traces). Secondary metrics include **latency** (inference time) and **compute cost** (number of training steps vs. full fine-tune).
*   **Trace-Specific Nuance (Uncertain):** Applying QLoRA *specifically* to "traces" (in-context examples or few-shot patterns) rather than the base model weights is a distinct technique often called **Instruction Tuning** or **Contextual Fine-tuning**. While QLoRA can be applied to the adapter layers, simply injecting more examples into the context window (prompt engineering) is often cheaper and more effective than training a QLoRA adapter on trace data unless the traces are massive or the model is severely misaligned.
*   **Hardware Constraints (Verified):** The M4 chip supports MLX and efficient quantization, making QLoRA viable, but training *on* traces (which are often text-heavy) can still be memory-intensive if the context window exceeds available VRAM, even with QLoRA.
*   **Risk of Overfitting (Verified):** Training QLoRA on a small set of traces risks overfitting, where the model memorizes the examples rather than generalizing the reasoning pattern. This is why a validation set (traces held out from training) is critical for measurement.

**Candidate:**
**Action:** Initialize a QLoRA training run on the local Fable harness (e.g., `src/models/fable-7b` or similar) using a subset of the training traces (e.g., 500-1k examples) as the instruction set, while keeping the base model frozen at 4-bit quantization.
**Measurement Plan:** Run a baseline evaluation on a held-out 200-example test set of traces. Compare the QLoRA fine-tuned model's accuracy against the base model's accuracy on the same test set. If the improvement is <2% or >5% (depending on task difficulty), flag as "no significant gain" or "overfitting risk" respectively.
**Implementation Note:** Use `peft` library with `bnb_4bit` for quantization. Ensure the training loop includes a validation step every 50 epochs to monitor loss curves and prevent overfitting.

**Next:**
*   Verify the exact file path and version of the local Fable model available in `src/models/`.
*   Extract a clean, labeled subset of training traces (excluding any PII or secrets) to serve as the instruction set.
*   Run a small-scale QLoRA training job (e.g., 5 epochs) on a subset of traces to confirm VRAM usage fits within the M4's 16GB limit.
*   Evaluate the resulting adapter on the held-out test set to confirm accuracy gains.
