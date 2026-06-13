import frappe
from frappe import _
from frappe.www.login import get_context as frappe_login_context

no_cache = True


def get_context(context):
    """Extend Frappe's stock login context with dynamic branding.

    Three distinct logo sources:
      Header  -> Website Settings app_logo (brand_logo)
      Watermark -> Company doctype company_logo (company_logo_image)
      Footer  -> Always https://dagaar.net/files/DAGAARLOGO20253c2ea8.png (dagaar_logo)
    """
    # Keep 100% of Frappe's auth context (LDAP, social, signup flags, 2FA...)
    frappe_login_context(context)

    ws = frappe.get_cached_doc("Website Settings")

    # ---- Header logo (Website Settings → app_logo) --------------------------
    context.brand_logo = (
        ws.get("app_logo")
        or ws.get("brand_image")
        or ws.get("banner_image")
        or ws.get("splash_image")
        or ""
    )

    # ---- Dagaar logo (always this URL — used in footer) ---------------------
    context.dagaar_logo = "https://dagaar.net/files/DAGAARLOGO20253c2ea8.png"

    # ---- Company name + company logo (for watermark) ------------------------
    company_name = None
    company_logo = ""
    default_company = frappe.db.get_single_value("Global Defaults", "default_company")
    if default_company:
        company_name, company_logo = frappe.db.get_value(
            "Company", default_company, ["company_name", "company_logo"]
        ) or (None, "")
    if not company_name:
        first = frappe.get_all(
            "Company",
            fields=["company_name", "company_logo"],
            order_by="creation asc",
            limit=1,
            ignore_permissions=True,
        )
        if first:
            company_name = first[0].company_name
            company_logo = first[0].company_logo or ""

    context.company_name = company_name or ws.get("app_name") or _("Dagaar Technology")
    # Watermark: company_logo from Company doctype, fallback to dagaar logo
    context.company_logo_image = company_logo or ""

    # ---- Optional extras (all overridable per-site) -------------------------
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
