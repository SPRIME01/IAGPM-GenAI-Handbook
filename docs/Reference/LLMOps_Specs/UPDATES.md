# LLMOps Specs Updates — 2025-11-12

This file records small, non-breaking runtime additions made to the Governed-Speed
LLMOps specs on 2025-11-12.

1. Runtime LLM provider selection

   - New environment variable: `PAC_LLM_PROVIDER`.
   - Supported values:
     - `http` (default) — Policy Gateway forwards requests to an upstream HTTP LLM endpoint (e.g., vLLM).
     - `litellm` — Policy Gateway constructs a LiteLLM client adapter when `litellm` is installed.
   - Purpose: allow deployments to pick the provider implementation without code changes.

2. Streaming proxy endpoint

   - New HTTP endpoint: `POST /proxy/completion/stream` on the Policy Gateway.
   - Behavior: returns Server-Sent-Events (SSE) with `data: <chunk>\n\n` for each
     text chunk produced by the configured LLM adapter's streaming API.
   - Use cases: low-latency UIs, token-by-token progress, partial result rendering.

3. Testing and CI notes

   - Added an integration test that verifies the SSE endpoint with a mocked
     adapter that produces multiple chunks.
   - CI pipeline retains pip cache but avoids caching the entire `.venv` for
     runner robustness (caching `.venv` can cause ABI/binary wheel mismatches
     across runners).

Reference: See `services/policy-gateway/src/app.py` for wiring and
`services/policy-gateway/tests/test_streaming.py` for a sample test.
