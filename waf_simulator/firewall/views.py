from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import WAFRule

# WAF Logic
def waf_check(request):
    if getattr(request, '_skip_waf', False):
        return True

    if request.method == "POST":
        body = request.POST.get('user_input', '')
        print("WAF checking body:", body)

        for rule in WAFRule.objects.filter(is_active=True):
            if rule.pattern.lower() in body.lower():
                print(f"Blocked by rule: {rule.name}")
                return False
    return True

# Form page
def input_form(request):
    if request.method == "POST":
        if not waf_check(request):
            return HttpResponseForbidden("403 Forbidden: Request blocked by WAF")

        user_input = request.POST.get('user_input')
        return render(request, 'firewall/result.html', {'user_input': user_input})
    return render(request, 'firewall/form.html')

# Dashboard
def dashboard(request):
    query = request.GET.get('q', '')
    if query:
        rules = WAFRule.objects.filter(name__icontains=query)
    else:
        rules = WAFRule.objects.all()
    
    return render(request, 'firewall/dashboard.html', {'rules': rules, 'query': query})

# Add Rule
def add_rule(request):
    if request.method == "POST":
        request._skip_waf = True
        name = request.POST.get('name')
        pattern = request.POST.get('pattern')

        if name and pattern:
            WAFRule.objects.create(name=name, pattern=pattern)
    return redirect('dashboard')

# Delete Rule
def delete_rule(request, rule_id):
    rule = get_object_or_404(WAFRule, id=rule_id)
    rule.delete()
    return redirect('dashboard')

# Toggle Rule
def toggle_rule(request, rule_id):
    rule = get_object_or_404(WAFRule, id=rule_id)
    rule.is_active = not rule.is_active
    rule.save()
    return redirect('dashboard')
