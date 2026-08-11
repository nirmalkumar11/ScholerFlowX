import os

from crewai import LLM

# --- Workaround for crewAI#5886 -----------------------------------------
# CrewAI 1.14.7 tags every outgoing message with `cache_breakpoint: true`
# (for Anthropic-style prompt caching) regardless of provider. Only the
# Anthropic adapter strips it back out before sending; Groq (and other
# non-Anthropic providers) reject the unknown field with a 400 error:
#   GroqException - property 'cache_breakpoint' is unsupported
# Neutralizing the tagging function is the fix the maintainers pointed to
# in the issue thread until it's patched upstream.
try:
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except ImportError:
    # crewai's internal module layout changed — nothing to patch.
    pass
# --------------------------------------------------------------------------


def get_llm():
    """
    Returns a CrewAI LLM wired to Groq's hosted API instead of a local
    Ollama server. Requires GROQ_API_KEY to be set (get a free key at
    https://console.groq.com/keys).

    Model choice: llama-3.3-70b-versatile is a strong general-purpose
    open model available on Groq's free tier. Swap GROQ_MODEL if you'd
    rather use something smaller/faster (e.g. "llama-3.1-8b-instant").
    """

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key at "
            "https://console.groq.com/keys and set it as an environment "
            "variable (or in .env) before starting the app."
        )

    model = os.environ.get("GROQ_MODEL", "groq/llama-3.3-70b-versatile")

    return LLM(
        model=model,
        api_key=api_key,
        temperature=0.1
    )
