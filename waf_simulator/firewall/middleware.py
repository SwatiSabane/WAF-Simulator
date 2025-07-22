import re
from django.http import HttpResponseForbidden
from .models import WAFRule

class WAFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Bypass WAF check if flagged to skip
        if getattr(request, "_skip_waf", False):
            return self.get_response(request)

        if request.method == "POST":
            body = request.body.decode("utf-8", errors="ignore")
            print("WAF checking body:", body)

            # Simple keyword-based detection
            waf_rules = WAFRule.objects.filter(is_active=True)
            for rule in waf_rules:
                if rule.pattern.lower() in body.lower():
                    return HttpResponseForbidden("403 Forbidden: Request blocked by WAF")
                    
        return self.get_response(request)