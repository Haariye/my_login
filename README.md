# My Login — Dagaar Technology

Per-site login page override for Frappe/ERPNext v15.

Install only on the site that should get this login:

    bench get-app https://github.com/<you>/my_login.git
    bench --site yoursite.com install-app my_login
    bench build --app my_login
    bench --site yoursite.com clear-website-cache

Branding is pulled at runtime — nothing hardcoded:
- Logo: Website Settings → App Logo (fallback: brand/banner image)
- Company name: Global Defaults → Default Company, else first Company
- Support email: `support_email` in site_config.json (optional)

All Frappe auth features keep working: password login, LDAP, social login,
login via email link, forgot password, signup, 2FA.
