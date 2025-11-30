from django import template
from django.utils.safestring import mark_safe
import markdown as md
import re

# Cria um objeto Library para registrar nossos filtros
register = template.Library()

@register.filter
def markdownify(text):
    html_content = md.markdown(text or "", extensions=["fenced_code"])
    # Remove script/style defensivamente sem depender de libs externas
    clean = re.sub(r'<\s*(script|style)[^>]*>.*?<\s*/\1\s*>', '', html_content, flags=re.I | re.S)
    return mark_safe(clean)


@register.filter
def duration_human(value):
    """Formata Duration/segundos para '2h 30min 2s', ocultando partes zeradas."""
    try:
        seconds = int(value.total_seconds()) if hasattr(value, "total_seconds") else int(value)
    except Exception:
        return "0s"
    hours, rem = divmod(max(seconds, 0), 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}min")
    if secs or not parts: parts.append(f"{secs}s")
    return " ".join(parts)
