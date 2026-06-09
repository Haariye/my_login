import frappe
from frappe import _
from frappe.www.login import get_context as frappe_login_context

no_cache = True


def get_context(context):
    """Extend Frappe's stock login context with dynamic branding.

    Nothing is hardcoded:
    - Logo      -> Website Settings (App Logo, then Brand/Banner image)
    - Company   -> Global Defaults default company, else first Company
    - Support   -> `support_email` key in site_config.json (optional)
    """
    # Keep 100% of Frappe's auth context (LDAP, social, signup flags, 2FA...)
    frappe_login_context(context)

    ws = frappe.get_cached_doc("Website Settings")

    # ---- Logo --------------------------------------------------------------
    # Try company logo first from Website Settings, then fall back to Dagaar
    context.brand_logo = (
        ws.get("app_logo")
        or ws.get("brand_image")
        or ws.get("banner_image")
        or ws.get("splash_image")
        or ""
    )
    context.brand_logo_fallback = "https://dagaar.net/files/DAGAARLOGO2025.png"

    # ---- Company name ------------------------------------------------------
    company_name = None
    default_company = frappe.db.get_single_value("Global Defaults", "default_company")
    if default_company:
        company_name = frappe.db.get_value("Company", default_company, "company_name")
    if not company_name:
        first = frappe.get_all(
            "Company",
            fields=["company_name"],
            order_by="creation asc",
            limit=1,
            ignore_permissions=True,
        )
        company_name = first[0].company_name if first else None
    context.company_name = company_name or ws.get("app_name") or _("Dagaar Technology")

    # ---- Optional extras (all overridable per-site, never hardcoded) -------
    context.portal_tagline = (
        frappe.conf.get("login_tagline")
        or _("Operations, finance, and insight — unified in one secure portal.")
    )
    context.portal_description = frappe.conf.get("login_description") or _(
        "This portal connects your team to real-time business data, "
        "workflows, and reporting across {0}. All activity is monitored "
        "for compliance."
    ).format(context.company_name)
    context.support_email = frappe.conf.get("support_email")
    context.portal_version = frappe.conf.get("portal_version") or "v1.0"

    context.no_cache = 1
    return context
