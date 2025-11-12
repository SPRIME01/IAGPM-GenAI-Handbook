from __future__ import annotations

from typing import Any, Iterator

try:
    import litellm
except Exception:  # pragma: no cover - litellm may not be installed in analysis env
    litellm = None

from policy_gateway.domain.models import CompletionRequest, CompletionResponse
from policy_gateway.ports.llm_adapter import LLMAdapterPort


class LiteLLMAdapter(LLMAdapterPort):
    """Adapter that uses the `litellm` client when available.

    This adapter attempts to use litellm's synchronous APIs if present. If
    `litellm` is not available the adapter raises at runtime. The stream()
    method will fall back to yielding the single completed result if streaming
    isn't supported by the installed litellm client.
    """

    def __init__(self, model: str | None = None, **kwargs: Any) -> None:
        if litellm is None:
            raise RuntimeError("litellm package is not installed")
        self.model = model or "local"
        self._cfg: dict[str, Any] = kwargs

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        # try to use a synchronous completion API if available
        if hasattr(litellm, "completion"):
            resp = litellm.completion(
                model=self.model,
                prompt=request.prompt,
                max_tokens=request.max_tokens or None,
                **self._cfg,
            )
            # response may be a dict-like or an object
            content = getattr(resp, "text", None) or (
                resp.get("text") if isinstance(resp, dict) else None
            )
            if content is None:
                # try other fields
                content = getattr(resp, "content", None) or (
                    resp.get("content") if isinstance(resp, dict) else str(resp)
                )
            model = getattr(resp, "model", None) or (
                resp.get("model") if isinstance(resp, dict) else self.model
            )
            usage = getattr(resp, "usage", None) or (
                resp.get("usage") if isinstance(resp, dict) else {}
            )
            return CompletionResponse(
                content=str(content), model=model, usage=usage or {}
            )

        # last-resort: try client.create(...) pattern
        if hasattr(litellm, "Client"):
            client = litellm.Client(**self._cfg)
            resp = client.complete(
                model=self.model,
                prompt=request.prompt,
                max_tokens=request.max_tokens or None,
            )
            text = getattr(resp, "text", None) or (
                resp.get("text") if isinstance(resp, dict) else str(resp)
            )
            return CompletionResponse(
                content=str(text),
                model=getattr(resp, "model", self.model),
                usage=getattr(resp, "usage", {}),
            )

        raise RuntimeError("No usable litellm completion API found")

    def stream(self, request: CompletionRequest) -> Iterator[str]:
        # If litellm supports a streaming iterator, use it. Otherwise yield the
        # completed content as a single-chunk stream.
        if hasattr(litellm, "stream"):
            for chunk in litellm.stream(
                model=self.model,
                prompt=request.prompt,
                max_tokens=request.max_tokens or None,
                **self._cfg,
            ):
                # chunk may be text or event objects
                if isinstance(chunk, str):
                    yield chunk
                else:
                    text = getattr(chunk, "text", None) or (
                        chunk.get("text") if isinstance(chunk, dict) else str(chunk)
                    )
                    if text:
                        yield text
            return

        # Fallback — single chunk
        yield self.complete(request).content
