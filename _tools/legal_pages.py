#!/usr/bin/env python3
"""Gera paginas legais (site + produto) para um dominio do repo funis.

Uso: python3 _tools/legal_pages.py
Edite SITE / PRODUCT abaixo para outro dominio/produto.
"""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {
    "domain": "besthealthadvice.online",
    "name": "Best Health Advice",
    "email": "contact@besthealthadvice.online",
    "updated": "November 10, 2026",
}

PRODUCT = {
    "slug": "gut",
    "name": "Gut Active",
    "support_email": "support@gutactive.store",
    "support_phone": "+1 833 762 6319",
    "address": "GutActive (C/O Fulfillment), 19655 E 35th Drive, Suite 100, Aurora, CO 80011, USA",
    "source": "https://bg.gutactive.store",
}

CSS = """
*{box-sizing:border-box}html,body{margin:0}
body{font-family:'Montserrat',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1f2a24;background:#f6f8f6;line-height:1.65}
header{background:#00552d;color:#fff;padding:18px 16px;text-align:center}
header a{color:#fff;text-decoration:none;font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:15px}
main{max-width:760px;margin:0 auto;padding:32px 16px 48px}
.card{background:#fff;border-radius:12px;padding:28px 24px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
h1{font-size:28px;line-height:1.25;margin:0 0 6px;color:#00552d}
.meta{color:#6b7a72;font-size:13px;margin:0 0 24px}
h2{font-size:19px;margin:28px 0 8px;color:#123d27}
p,li{font-size:15.5px}
ul{padding-left:20px}
a{color:#0b6b3a}
.note{background:#f1f6f2;border-left:4px solid #00552d;padding:12px 14px;border-radius:6px;font-size:14.5px}
footer{max-width:760px;margin:0 auto;padding:0 16px 40px;text-align:center;font-size:13px;color:#6b7a72}
footer nav{display:flex;flex-wrap:wrap;gap:6px 14px;justify-content:center;margin-bottom:10px}
footer a{color:#4a5a51}
"""


def footer_links():
    s = PRODUCT["slug"]
    links = [
        ("Terms &amp; Conditions", "/terms/"), ("Privacy Policy", "/privacy/"), ("Contact", "/contact/"),
        ("Disclaimer", "/disclaimer/"), ("References", f"/{s}/references/"), ("Refund", f"/{s}/refund/"),
        ("Shipping", f"/{s}/shipping/"),
    ]
    return "".join(f'<a href="{h}">{t}</a>' for t, h in links)


def page(path, title, body):
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | {SITE['name']}</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<header><a href="/">{SITE['name']}</a></header>
<main><div class="card">
<h1>{html.escape(title)}</h1>
<p class="meta">Last updated: {SITE['updated']}</p>
{body}
</div></main>
<footer><nav>{footer_links()}</nav>
<p>These statements have not been evaluated by the Food and Drug Administration. Products mentioned on this site are not intended to diagnose, treat, cure, or prevent any disease.</p>
<p>&copy; 2026 {SITE['name']}. All rights reserved.</p></footer>
</body>
</html>
"""
    full = os.path.join(ROOT, SITE["domain"], "public", path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(out)
    print("ok", path)


S, P = SITE, PRODUCT
support = (f'<a href="mailto:{P["support_email"]}">{P["support_email"]}</a> or by phone at '
           f'<a href="tel:{P["support_phone"].replace(" ", "")}">{P["support_phone"]}</a>')
site_mail = f'<a href="mailto:{S["email"]}">{S["email"]}</a>'

# ---------------- site-level pages ----------------
page("/contact/", "Contact Us", f"""
<h2>Questions about an order</h2>
<p>All orders for {P['name']} are processed and fulfilled by the manufacturer, not by {S['name']}. For anything related to an order — tracking, shipping, cancellations, returns or refunds — please contact the {P['name']} Customer Support Team directly:</p>
<ul>
<li>Email: <a href="mailto:{P['support_email']}">{P['support_email']}</a></li>
<li>Phone: <a href="tel:{P['support_phone'].replace(' ', '')}">{P['support_phone']}</a></li>
</ul>
<p class="note">Tip: include your order number, the full name and the email used at checkout so the support team can locate your order quickly.</p>
<h2>Questions about this website</h2>
<p>For questions about the content of {S['domain']}, our policies or privacy requests, write to {site_mail}. We usually reply within 2 business days.</p>
""")

page("/privacy/", "Privacy Policy", f"""
<p>This Privacy Policy explains how {S['name']} ("we", "us") collects and uses information when you visit {S['domain']} (the "Site").</p>
<h2>Information we collect</h2>
<ul>
<li><strong>Information collected automatically:</strong> IP address, browser and device type, pages viewed, referring website, and the date and time of your visit.</li>
<li><strong>Cookies and similar technologies:</strong> we and our partners use cookies, pixels and similar tools to measure traffic, understand how visitors use the Site and measure the performance of our advertising.</li>
<li><strong>Information you send us:</strong> if you email us, we receive your email address and the content of your message.</li>
</ul>
<p>We do not sell products directly on this Site and we do not collect payment information. Purchases are completed on third-party checkout pages operated by the product manufacturer and its payment processor, which are governed by their own privacy policies.</p>
<h2>How we use information</h2>
<ul>
<li>To operate, maintain and improve the Site;</li>
<li>To measure the performance of our content and advertising campaigns;</li>
<li>To respond to your messages;</li>
<li>To detect and prevent fraud or misuse of the Site.</li>
</ul>
<h2>Third-party services</h2>
<p>We work with third parties such as hosting providers, video players, analytics providers and advertising networks (for example, content recommendation platforms). These partners may set their own cookies and collect information about your visit in accordance with their own privacy policies.</p>
<h2>Your choices</h2>
<ul>
<li>You can block or delete cookies in your browser settings. Some parts of the Site may not work properly without them.</li>
<li>You can opt out of interest-based advertising from many networks at <a href="https://optout.aboutads.info" rel="nofollow">optout.aboutads.info</a> and <a href="https://optout.networkadvertising.org" rel="nofollow">optout.networkadvertising.org</a>.</li>
<li>Depending on where you live (for example, California or the European Union), you may have the right to request access to, correction of, or deletion of your personal information. To make a request, email {site_mail}.</li>
</ul>
<h2>Children</h2>
<p>The Site is not directed to children under 18, and we do not knowingly collect information from them.</p>
<h2>Data security and retention</h2>
<p>We use reasonable measures to protect information and keep it only as long as necessary for the purposes described above.</p>
<h2>Changes</h2>
<p>We may update this policy from time to time. Changes take effect when posted on this page with a new "Last updated" date.</p>
<h2>Contact</h2>
<p>Questions about this policy: {site_mail}.</p>
""")

page("/terms/", "Terms &amp; Conditions", f"""
<p>By accessing or using {S['domain']} (the "Site") you agree to these Terms. If you do not agree, please do not use the Site.</p>
<h2>Informational purposes only</h2>
<p>All content on the Site is provided for general informational purposes only and is not medical advice. It is not a substitute for advice from your physician or another qualified health professional. Always consult a healthcare professional before starting any diet, exercise or supplementation program, or if you have or suspect you have a health problem.</p>
<h2>Third-party products and websites</h2>
<p>The Site presents products that are manufactured, sold and shipped by third parties. When you click a link to buy a product, you leave the Site and are subject to the terms, policies and checkout of that third party. {S['name']} is not the seller of these products and is not responsible for their fulfillment, shipping, returns or refunds. Please see the <a href="/contact/">Contact</a> page for the manufacturer's support details.</p>
<h2>Affiliate relationship</h2>
<p>{S['name']} may receive a commission when you purchase a product through links on the Site. This does not change the price you pay. See our <a href="/disclaimer/">Disclaimer</a> for details.</p>
<h2>Results may vary</h2>
<p>Individual results vary. Testimonials and examples shown on the Site reflect individual experiences and are not a guarantee that you will achieve the same results.</p>
<h2>Intellectual property</h2>
<p>Content on the Site, including text, graphics and layout, is protected by applicable intellectual property laws. Product names, logos and images belong to their respective owners.</p>
<h2>Disclaimer of warranties and limitation of liability</h2>
<p>The Site is provided "as is" without warranties of any kind. To the fullest extent permitted by law, {S['name']} is not liable for any damages arising from your use of the Site or of any product purchased from a third party.</p>
<h2>Changes</h2>
<p>We may update these Terms at any time. Continued use of the Site after changes are posted means you accept the updated Terms.</p>
<h2>Contact</h2>
<p>Questions about these Terms: {site_mail}.</p>
""")

page("/disclaimer/", "Disclaimer", f"""
<h2>Affiliate disclosure</h2>
<p>{S['name']} is an independent publisher. Some links on this Site are affiliate links, which means we may earn a commission if you click a link and make a purchase, at no additional cost to you. We are not the manufacturer or seller of the products presented on this Site.</p>
<h2>Not medical advice</h2>
<p>The information on this Site is for educational and informational purposes only and is not intended as a substitute for professional medical advice, diagnosis or treatment. Never disregard professional medical advice or delay seeking it because of something you read or watched on this Site.</p>
<h2>FDA statement</h2>
<p>These statements have not been evaluated by the Food and Drug Administration. Products presented on this Site are not intended to diagnose, treat, cure, or prevent any disease.</p>
<h2>Results vary</h2>
<p>Results vary from person to person and depend on many factors, including diet, activity level and individual health. No specific result is guaranteed.</p>
<h2>Consult your doctor</h2>
<p>Consult your healthcare professional before using any dietary supplement, especially if you are pregnant or nursing, taking medication, or have a medical condition.</p>
""")

# ---------------- product pages (policies provided by the manufacturer) ----------------
src_note = (f'<p class="note">This policy is provided by {P["name"]}, the manufacturer and seller of the product. '
            f'Orders, shipping and refunds are handled entirely by {P["name"]}\'s Customer Support Team: {support}.</p>')

page(f"/{P['slug']}/refund/", f"{P['name']} Refund Policy", src_note + f"""
<h2>60-Day Satisfaction Promise</h2>
<p>If you're not fully satisfied with your purchase, please contact the {P['name']} Customer Support Team to request assistance. Your order is protected by a 60-Day Satisfaction Promise. Consistent use during this period is recommended so the product has adequate time to work.</p>
<h2>Keep-the-Product Option (Partial Refund)</h2>
<p>If you prefer not to return the product, the manufacturer may offer an optional partial refund with no return required. Accepting this offer closes your order and ends the right to a further return. This option is discretionary and based on order history and usage feedback.</p>
<h2>How to Request a Refund</h2>
<p><strong>Step 1 — Contact Support:</strong> email <a href="mailto:{P['support_email']}">{P['support_email']}</a> with the subject line "Refund Request – Order #_____". The support team will review your request and provide return instructions.</p>
<p><strong>Step 2 — Ship your return within 7 calendar days:</strong> send back all bottles (empty or unopened) and any included bonuses or gifts within 7 days after receiving the return instructions. Include the packing slip inside the package.</p>
<ul>
<li>Use a trackable shipping method and email the tracking ID to support.</li>
<li>Return shipping is the customer's responsibility unless an incorrect or damaged item was shipped — in those cases, a prepaid label will be provided.</li>
<li>C.O.D. deliveries or "Return to Sender" packages cannot be accepted.</li>
</ul>
<h2>Return Address</h2>
<p>{P['address']}</p>
<h2>What Gets Refunded</h2>
<p>Eligible amount: product price paid. Refunds are issued to the original payment method only.</p>
<h2>Processing Times</h2>
<ul>
<li>Inspection &amp; approval: typically 3–5 business days after the returned package arrives.</li>
<li>Credit card: 5–7 business days. Debit card: 5–10 business days.</li>
</ul>
<p>A confirmation email is sent once the refund is processed.</p>
<h2>Eligibility Limits</h2>
<ul>
<li>Bulk or reseller orders are not eligible.</li>
<li>Suspected misuse (e.g., repeated returns or altered items) may require verification or be declined.</li>
</ul>
""")

page(f"/{P['slug']}/shipping/", f"{P['name']} Shipping Policy", src_note + f"""
<h2>Processing Time</h2>
<p>Please allow 1–2 business days for your order to be processed and shipped. During holidays, orders can experience delays. If invalid information is provided, processing may be delayed an additional 3–5 business days. Orders ship Monday–Friday, excluding weekends and US holidays.</p>
<h2>Domestic Delivery Time — Standard Shipping</h2>
<p>Time in transit depends on the shipping method selected and does not include weekends or holidays. All delivery times are estimates and may be affected by events beyond the seller's control.</p>
<h2>Refused, Lost, Stolen or Delayed Packages</h2>
<p>If a package is refused, the shipping and handling fee will be charged, and a refund will not be initiated until the product is received back. UPS is the primary delivery service used; the seller is not responsible for lost or stolen packages shipped via UPS.</p>
<h2>Cancel Order</h2>
<p>Orders go directly into fulfillment. If you contact support within 24 hours of purchase, you can cancel the order. After 24 hours cancellations are not possible; if the order has shipped, you will need to refuse the package or return it.</p>
<h2>Wrong Address</h2>
<p>It is the buyer's responsibility to ensure the shipping address is correct. The seller is not responsible for incorrect addresses provided by the buyer.</p>
<h2>Delivery of Items</h2>
<p>If the tracking number shows the package was delivered to the customer's address, refunds are not offered for items claimed as not delivered.</p>
<h2>Returns</h2>
<p>To obtain a refund, return all bottles (empty, full or partially full) within 60 days of the original order date, including your order ID, full name, address, email and phone number, to:</p>
<p>{P['address']}</p>
""")

refs = [
    ("Peer-reviewed studies on the types of ingredients in Gut Active", [
        ("Yang J, Wang HP, Zhou L, Xu CF. Effect of dietary fiber on constipation: a meta analysis. World J Gastroenterol. 2012;18(48):7378-7383.", "https://doi.org/10.3748/wjg.v18.i48.7378",
         "Dietary fiber intake increased stool frequency in people with constipation."),
        ("McRorie JW, Daggy BP, Morel JG, et al. Psyllium is superior to docusate sodium for treatment of chronic constipation. Aliment Pharmacol Ther. 1998;12(5):491-497.", "https://doi.org/10.1046/j.1365-2036.1998.00336.x",
         "Psyllium husk (an ingredient in Gut Active) increased stool water content and bowel movement frequency."),
        ("Attaluri A, Donahoe R, Valestin J, Brown K, Rao SSC. Randomised clinical trial: dried plums (prunes) vs. psyllium for constipation. Aliment Pharmacol Ther. 2011;33(7):822-828.", "https://doi.org/10.1111/j.1365-2036.2011.04594.x",
         "Dried plums (plum fruit is an ingredient in Gut Active) improved spontaneous bowel movements and stool consistency."),
        ("Chen HL, Cheng HC, Wu WT, Liu YJ, Liu SY. Supplementation of konjac glucomannan into a low-fiber Chinese diet promoted bowel movement and improved colonic ecology in constipated adults. J Am Coll Nutr. 2008;27(1):102-108.", "https://doi.org/10.1080/07315724.2008.10719681",
         "Glucomannan (an ingredient in Gut Active) increased bowel movement frequency in constipated adults."),
        ("Dimidi E, Christodoulides S, Fragkos KC, Scott SM, Whelan K. The effect of probiotics on functional constipation in adults: a systematic review and meta-analysis of randomized controlled trials. Am J Clin Nutr. 2014;100(4):1075-1084.", "https://doi.org/10.3945/ajcn.114.089151",
         "Probiotics as a group improved whole-gut transit time, stool frequency and consistency; effects varied by strain."),
    ]),
]
body = '<p>The studies below evaluated the types of ingredients found in Gut Active (psyllium husk, oat bran, apple pectin, glucomannan, plum fruit and Lactobacillus acidophilus), often at amounts different from those in the product. They did not evaluate Gut Active itself.</p>'
for h, items in refs:
    body += f"<h2>{h}</h2><ul>" + "".join(
        f'<li><a href="{u}" rel="nofollow noopener" target="_blank">{t}</a><br>{d}</li>' for t, u, d in items) + "</ul>"
page(f"/{P['slug']}/references/", "References", body)
