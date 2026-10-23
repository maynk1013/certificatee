# Project 4 interview notes

## Architecture, Hinglish

Teen signal yaad rakho: rate, errors, duration. Saturation alag se CPU aur memory hai. Prometheus in numbers ko rakhta hai. Loki logs rakhta hai. Alloy pods se logs uthakar Loki ko bhejta hai. Grafana dono ko ek jagah dikha sakta hai. Alertmanager rule match par route karta hai.

Local lab sample text padh kar yahi sawal poochta hai. Woh Prometheus nahi hai. Interview mein yeh farak pehli line mein bolo.

## Questions

1. Metric aur log mein farak?
   Answer: Metric number hai, sasta aggregate. Log detail hai, mehnga storage. Dono chahiye. Metric batata hai kitna, log batata hai kaun sa request.
   Trade-off: Har log line ko metric mat banao. Cardinality phat jaati hai.
   Follow-up: User id ko label banana kyun galat hai?

2. SLI aur SLO?
   Answer: SLI woh measurement hai, jaise non-5xx divided by total. SLO us par target hai, jaise 99 percent. Yahan yeh examples hain, measured service level nahi.
   Trade-off: Tight SLO alert noise badhata hai. Loose SLO customer se pehle nahi hilta.
   Follow-up: Khali traffic ko 100 percent availability kyun nahi maana? Code `None` return karta hai.

3. Error budget kya hai?
   Answer: 99 percent SLO par 1 percent requests fail ho sakte hain window mein. Budget khatam ho to release rokna ek policy hai. Yahan budget calculate karke enforce nahi kiya gaya.
   Trade-off: Error budget bina traffic ke meaningful nahi.
   Follow-up: 5 percent alert threshold aur 99 percent SLO ek cheez nahi hain. Alert jaldi bolta hai.

4. Average latency aur percentile?
   Answer: Is demo ka metric sum aur count hai, isliye average nahi p95. Ek slow request average ko kheench sakta hai, ya chhupa sakta hai.
   Trade-off: Histogram zyada series banata hai, lekin percentile deta hai.
   Follow-up: Dashboard title average kyun kehta hai? Taaki galat claim na ho.

5. `for: 10m` kyun?
   Answer: Ek spike par page na ho. Alert tab fire kare jab condition 10 minute rahe.
   Trade-off: Short outage miss ho sakta hai.
   Follow-up: Critical target-down ka `for` 5 minute kyun chhota hai?

6. Test alert live Alertmanager se nahi gaya. Phir kya dikhaoge?
   Answer: `evidence/test-alert.log`, jo fixed bad sample se bana. Usme teen alert names hain. Yeh local evaluator hai.
   Trade-off: Recruiter asal Grafana chahe to yeh demo kam padega. Limitation bolo.
   Follow-up: Healthy sample par list khali kyun rehti hai?

7. Retention 7 din kaafi hai?
   Answer: Lab ke liye example hai. Incident ek hafte baad aaye to data gayab hoga. Production mein retention, disk, aur remote storage alag design hai. Yahan capacity test nahi hua.
   Trade-off: Lambi retention mehengi hai.
   Follow-up: Loki `168h` wahi 7 din hai.

8. Alloy DaemonSet kyun?
   Answer: Har node par logs hote hain. DaemonSet har node par collector rakhta hai. Deployment ek hi node padhta.
   Trade-off: Har node par CPU aur memory lagti hai. Values mein requests diye hain, measured nahi.
   Follow-up: Promtail se Alloy kyun? Grafana Alloy current collector hai. Promtail ko naya default mat bolo.

9. Grafana password Git mein kyun nahi?
   Answer: `existingSecret` use hota hai. Values file key names rakhti hai, password nahi.
   Trade-off: Secret cluster mein pehle se hona chahiye, warna pod start nahi hota.
   Follow-up: Default admin password wala chart dangerous kyun hai?

10. Alert routing mein null receiver kyun?
    Answer: Slack file na ho to bhi Alertmanager config valid rahe. Warning route optional Slack par hai.
    Trade-off: Default null hone par koi notice nahi karega jab tak route match na ho.
    Follow-up: Critical aur warning alag channel kab banate ho?

11. High cardinality ka example?
    Answer: `path` label mein har URL, ya `user_id`. Series count explode hota hai aur Prometheus memory badhti hai.
    Trade-off: Debug ke liye detail chahiye hoti hai. Use logs, not labels.
    Follow-up: Is demo ke labels kaun se hain? Method, path, aur status app metric mein hain. Path ko production mein limited rakho. Yeh ek improvement hai, abhi app path label rakhta hai. Interview mein bolo ki production mein path ko template karna chahiye.

12. Runbook alert se link kyun?
    Answer: Raat ko page aaye to engineer ko steps chahiye, dashboard nahi dhundna chahiye. Is repo ke runbooks sample hain.
    Trade-off: Runbook purana ho sakta hai. Usse code ke saath commit karo.
    Follow-up: Pehla step error rate par kya hai? 4xx aur 5xx alag karo.

13. Cluster metrics aur app metrics?
    Answer: `up` aur node CPU cluster side hain. `demo_http_requests_total` app khud export karti hai. Dono dashboards par hain.
    Trade-off: App metric tabhi aati hai jab scrape ho. ServiceMonitor project 1 ki dev values mein hai.
    Follow-up: Scrape fail ho to kaun sa alert? Target down, jab `up == 0`.

14. Production hardening kya bacha hai?
    Answer: Grafana auth, Loki TLS, object storage, multi-replica, aur real on-call. README yeh list karta hai as not implemented.
    Trade-off: Lab values ko production bolna galat hai.
    Follow-up: Single binary Loki ka replication factor 1 kya keh raha hai? Ek copy. Woh HA nahi hai.

15. 60 second pitch?
    Answer: "Maine golden signal dashboard aur alert rules git mein rakhe, aur ek local lab se sample metrics, logs, aur test alert verify kiye. Cluster install alag step hai aur maine use yahan nahi chalaya."
    Trade-off: Pitch mein tool names kaafi hain. Unhe tabhi bolo jab file dikha sako.
    Follow-up: Kaun si query error ratio hai? 5xx rate divided by total rate.
