# Project 2 interview notes

## Architecture, Hinglish

Do strategies hain. Blue-green mein preview copy ready hoti hai, active Service tab tak purane version par rehti hai. Canary mein weight 10, 30, 50, phir 100 hota hai. Beech mein analysis error ratio dekhti hai.

Local Python model yahi decision karta hai aur log likhta hai. Argo Rollouts YAML Helm se render hoti hai. Cluster par rollout nahi chala, isliye zero downtime claim mat karo.

## Questions

1. Blue-green aur canary ka practical farak?
   Answer: Blue-green ek switch hai. Canary dheere dheere users ko naye version par le jaata hai.
   Trade-off: Blue-green ko do copies ki capacity chahiye. Canary mein kuch users pehle bug dekh sakte hain.
   Follow-up: Database migration dono mein kyun mushkil hai?

2. `autoPromotionEnabled: false` kyun?
   Answer: Preview healthy hone ke baad bhi active traffic apne aap nahi badalta. Insaan ya pipeline promotion allow karti hai.
   Trade-off: Fast release slow ho jaati hai. Safety badhti hai.
   Follow-up: Local model ka `paused` status isi ko dikhata hai.

3. Analysis fail hone par kya hota hai?
   Answer: Canary model failure limit ke baad weight 0 kar deta hai aur active version v1 rehta hai. Blue-green active service ko switch nahi karta.
   Trade-off: False positive analysis good release ko bhi rok sakti hai.
   Follow-up: `failureLimit` 1 ka matlab kitni failures? Code `failures > failure_limit` check karta hai, isliye do failures par rollback hota hai. Yeh detail interviewer ko code se dikha dena.

4. Readiness ko analysis se alag kyun rakhte hain?
   Answer: Readiness pod ko Service se hatati hai. Analysis poore release ka error ratio dekhti hai. Dono kaam alag hain.
   Trade-off: Sirf readiness se slow errors nahi pakadte. Sirf analysis se crashloop late pakad mein aata hai.
   Follow-up: `FAIL_READY` aur `FAIL_API` demo mein kya karte hain?

5. Prometheus query galat ho to rollout kaise behave karega?
   Answer: Address galat ho to analysis fail hoti hai aur rollback ho sakta hai. Isliye pehle query ko Prometheus UI mein chalao.
   Trade-off: Analysis na lagao to broken release promote ho sakti hai.
   Follow-up: Success condition `result[0] >= 0.95` 5 percent error budget se kaise milti hai?

6. Kya yeh zero downtime hai?
   Answer: Nahi, jab tak live traffic ke dauran failed request count na maapa ho. Local model packets nahi bhejta.
   Trade-off: Interview mein chhota claim zyada strong hota hai.
   Follow-up: Kaun sa test dikhaoge? `evidence/canary-failure.log`.

7. Stable service aur canary service kyun alag hain?
   Answer: Taaki tum canary traffic ko alag se scrape kar sako. Active users stable service se jaate hain.
   Trade-off: Extra Service objects aur label rules.
   Follow-up: Blue-green ke active aur preview services ka yahi role hai.

8. Rollback aur redeploy mein farak?
   Answer: Rollback last known good revision par wapas jata hai. Redeploy naya build hai. Dono ko ek mat bolo.
   Trade-off: Rollback tab kaam nahi karta jab purana version naya schema na padh sake.
   Follow-up: Revision history limit 5 kyun rakhi?

9. Weight 10 percent ka matlab 10 percent pods hai ya traffic?
   Answer: Argo Rollouts `setWeight` traffic weight hai. Pod count hamesha same percentage nahi hota.
   Trade-off: Kam replicas par weight granular nahi hota.
   Follow-up: 2 replicas par 10 percent weight practically kya kar sakta hai?

10. Simulated failure ko production flag mat chhodo. Kaise bachoge?
    Answer: `simulateFailure` alag values file mein hai, default false hai. GitOps mein wahi file sync hoti hai jo tumne point ki.
    Trade-off: Galat values file Argo CD par lag gayi to saare pods unready ho jayenge.
    Follow-up: Values file ka naam Application manifest mein kahan dikhega?

11. Flagger aur Argo Rollouts?
    Answer: Dono canary kar sakte hain. Yahan Argo Rollouts isliye hai kyunki Rollout CRD seedha strategy dikhati hai. Flagger yahan implement nahi hai.
    Trade-off: Ek aur controller operate karna padta hai.
    Follow-up: Service mesh ke bina weight kaise shift hota hai?

12. Metrics nahi aa rahe aur analysis pending hai. Kya karoge?
    Answer: Pehle scrape target, phir Prometheus address, phir query. Analysis ko fail hone dena ya pause karna ek product decision hai. Is chart mein failure limit hai.
    Trade-off: Missing metrics ko success maanna khatarnaak hai.
    Follow-up: `clamp_min` yahan kyun hai?

13. Release ke dauran database migrate kar di. Rollback safe hai?
    Answer: Tab safe hai jab migration backward compatible ho. Yeh demo mein database hai hi nahi. Interview mein yeh limit bolo.
    Trade-off: Expand-contract migrations slow hoti hain, lekin rollback possible rehta hai.
    Follow-up: Expand aur contract phase kya hain?

14. Evidence log ko screenshot kyun nahi bola?
    Answer: Log us command ka output hai jo test ne likha. Woh cluster screenshot nahi hai. Dono ko label karo.
    Trade-off: Recruiter soch sakta hai cluster chala tha. README mein yeh clearly hai.
    Follow-up: Live demo mangne par Docker missing ho to kya bolenge?

15. Is project ko experience bullet kaise likhen?
    Answer: "Modeled canary and blue-green promotion gates, with an automatic rollback path when readiness or error ratio fails, and rendered the Argo Rollouts manifests with Helm." Measured downtime mat likho.
    Trade-off: Bullet kam impressive lag sakta hai. Woh theek hai.
    Follow-up: Kaun si file interviewer ko khud chalane ko doge?
