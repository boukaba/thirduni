# OWASP Bug Triage 🔍

         _
        /_/_      .'''.
     =O(_)))) ...'     `.
        \_\              `.    .'''
                           `..'

Example:
Customer passwords are being stored in plain text in the database.
OWASP Top 10: Cryptographic Failures
Fix: Scramble or hash passwords before storing so they can’t be read directly. 


---

Restaurant uploaded a file called menu.js instead of an image, and it actually ran when someone opened it through the CDN.
OWASP Top 10: Security Misconfiguration
Fix: Only allow image uploads and store files somewhere they can't be executed as code.

Driver changed the order ID in the URL and could see another customer’s order details.
OWASP Top 10: Broken Access Control
Fix: The backend must always verify that the person requesting an order actually owns that order.

Any logged-in user can open /admin/orders and see restaurant dashboards.
OWASP Top 10: Broken Access Control
Fix: Hidden links are never enough. The server must confirm only admins can open certain pages. Non-admins should see a rejection, not a dashboard.

Payment webhooks are coming in with fake “paid” statuses because we’re not verifying where the request is coming from.
OWASP Top 10: Software and Data Integrity Failures
Fix: Verify that webhook messages really come from the payment provider, not someone pretending to be them.

Login form is still using plain HTTP — credentials show up in clear text in the network tab.
OWASP Top 10: Cryptographic Failures
Fix: Always use HTTPS everywhere, especially for logins, so credentials can't be seen by anyone watching the traffic.

Logs are printing full card numbers and addresses whenever a payment fails.
OWASP Top 10: Security Logging and Monitoring Failures
Fix: Only log what is necessary and mask private data, like showing just the last few digits of a card.

---

Need a refresher? Check out `owasp10_reference.md`!