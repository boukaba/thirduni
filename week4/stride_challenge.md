# STRIDE Challenge 🕵️‍♀️

        .--.       .--.
    _  `    \     /    `  _
     `\.===. \.^./ .===./`
            \/`"`\/
         ,  |     |  ,
        / `\|`-.-'|/` \
       /    |  \  |    \
    .-' ,-'`|   ; |`'-, '-.
        |   |    \|   | 
        |   |    ;|   |
        |   \    //   |
        |    `._//'   |
       .'             `.
    _,'                 `,_

Time to think like a security tester!

Below are six QuickBite Potential Threats.  
For each one, write which STRIDE category it fits into, and why.

---

Potential Threat 1:
Thousands of fake orders slow the app to a crawl.
STRIDE: D, Denial of Service
Why: a flood of requests that overwhelms the server

---

Potential Threat 2:
A driver marks an order “delivered,” but later insists they didn’t.
STRIDE: R, Repudiation
Why: there is no audit trail to prove the action was taken. No timestamp, no proof photo, no signature. Both sides can point fingers and we're stuck.

---

Potential Threat 3:
A driver discovers an admin dashboard link can see all the current orders.
STRIDE: E, Elevation of Privilege
Why: a lower-role user has gained admin access through a hidden route or weak access control.

---

Potential Threat 4:
A customer changes an order ID in the URL and views another person’s receipt.
STRIDE: S, Spoofing
Why: they're pretending to be another user. By tweaking the URL they're saying "I'm user number 42 now." If the app doesn't double-check who's actually making the request, everyone can see everyone else's private information.

---

Potential Threat 5:
An error message prints the customer’s full address to the browser console.
STRIDE: I, Information Disclosure
Why: a simple leak of private data. Developers often forget that error messages can leak secrets. If your stack trace or debug info exposes personal data, you've just handed attackers some free intel.

---

Potential Threat 6:
A customer edits their total price to $0.30 before checkout.
STRIDE: T, Tampering
Why: data is being modified before it is sent to the server. If we're not validating that number server-side, we've basically said "sure, thirty cents for a full meal, why not."

