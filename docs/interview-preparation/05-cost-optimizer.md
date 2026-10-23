# Project 5 interview notes

## Architecture, Hinglish

Yeh tool sweeper nahi, reporter hai. Snapshot padhta hai: instances, CPU average, volumes, Elastic IPs, tags. Phir CSV aur JSON likhta hai. Default dry-run hai. Stop command alag hai aur bina allow switch ke refuse karti hai.

Savings tab likhta hai jab price catalog snapshot mein ho aur flag on ho. Sample report mein savings null hai. Us null ko "maine paise bacha liye" mat bolna.

## Questions

1. Idle instance ka rule kya hai?
   Answer: Running ho, aur CPU average threshold se neeche ho. Missing CPU par woh idle nahi, insufficient data hai.
   Trade-off: CPU kam hone ka matlab unused nahi. Batch job raat ko chalti hai aur din mein idle dikhti hai.
   Follow-up: Lookback window snapshot ke average mein chhupa hai. Live CloudWatch call default CLI mein nahi hai.

2. Stopped instance ko report kyun nahi karta?
   Answer: Woh already stopped hai. Finding tab useful hai jab koi action bache. EBS alag se unattached volume check karta hai.
   Trade-off: Stopped instance ka disk phir bhi bill karta hai. Woh volume detector ka kaam hai agar disk unattached ho. Attached stopped volume yahan alag detector nahi hai. Yeh gap bolo.
   Follow-up: Nat gateway aur idle load balancer is tool mein nahi hain.

3. Unattached EIP kyun waste hai?
   Answer: Associated na ho to kai accounts mein hourly charge lagta hai. Associated ho to wahi charge nahi lagta. Tool association_id ya instance_id dekhta hai.
   Trade-off: Failover ke liye khali IP jaan bujh kar rakhi ja sakti hai. Isliye action "release only after confirming" hai, automatic nahi.
   Follow-up: Remediation EIP release kyun nahi karta? Kyunki default mutating action sirf approved stop hai.

4. Tag finding savings kyun nahi deti?
   Answer: Missing tag ka bill alag se nahi nikalta. Woh ownership problem hai. Estimate basis yeh clearly kehta hai.
   Trade-off: FinOps teams tags ko cost allocation ke liye use karti hain, lekin tag ka apna dollar amount nahi hota.
   Follow-up: `Environment=qa` inconsistent kyun hai? Allowed set dev, staging, prod hai.

5. Dry-run default kyun?
   Answer: Galat automation se instance band ho sakta hai. Report pehle, action baad mein, aur action par id list.
   Trade-off: Tool kam "magic" lagta hai. Wahi safe hai.
   Follow-up: `execute_plan` client None ho to kya karta hai? Refuse.

6. Estimate aur actual saving?
   Answer: Hourly price times 730 hours ek arithmetic estimate hai. Bill, credits, aur tax usme nahi. Sample path price hi nahi bhejta.
   Trade-off: 730 hours ek month ka rough hour count hai, calendar month nahi.
   Follow-up: Fixture test mein 1 dollar per hour times 730 = 730. Woh fixture hai, AWS price nahi.

7. IAM `Resource: "*"` least privilege kaise hua?
   Answer: `DescribeInstances` aur Cost Explorer resource-level ARN support nahi karte. Stop permission alag file mein hai aur tag condition ke saath hai. Default policy stop nahi karti.
   Trade-off: Describe phir bhi poora account dekh sakta hai. SCP ya permission boundary usse aur baandh sakti hai. Yahan SCP nahi hai.
   Follow-up: `ec2:StopInstances` par tag condition ka naam kya hai? `CostOptAllowStop`.

8. AccessDenied par tool crash kyun nahi karta poori report ko?
   Answer: `call_with_retry` non-throttle errors ko `AwsCallError` banata hai. Live collector is error ko report ke `errors` list mein rakh sakta hai. Default CLI snapshot use karta hai, AWS nahi.
   Trade-off: Error nigal kar empty success dikhana galat hota. Isliye exception clear hai.
   Follow-up: Throttle par teen tries kyun? Temporary limit ke liye. Permanent error par retry nahi.

9. Lambda aur EventBridge?
   Answer: Handler dry-run JSON lautata hai. Schedule create nahi hua. Optional target hai.
   Trade-off: Lambda tabhi useful hai jab snapshot event mein ho. Woh khud inventory nahi kheenchta is sample mein.
   Follow-up: Lambda ko remediation policy kyun nahi doge by default?

10. Slack message secret kyun nahi?
    Answer: Webhook URL log mein nahi aata. Empty URL par koi HTTP call nahi hoti. Real Slack send test nahi hua.
    Trade-off: Message body mein resource id theek hai, secret theek nahi.
    Follow-up: Kaun sa test empty webhook check karta hai?

11. Boto3 pagination real account mein kyun zaroori hai?
    Answer: Describe calls pages mein aati hain. Ek page par ruk gaye to report adhoori hogi. Yeh live collector abhi default path nahi hai, isliye main pagination ko implemented live feature nahi bolta.
    Trade-off: Snapshot tests pagination ko cover nahi karte.
    Follow-up: Agar live mode likho to `NextToken` kahan loop karega?

12. Region list kaise choose karoge?
    Answer: Enabled regions describe karke, phir har region. Sample ek region dikhata hai. Missing permission ek region ko poori job nahi girana chahiye.
    Trade-off: Zyada regions zyada API calls.
    Follow-up: Global service jaise IAM tags regionless hote hain.

13. CSV aur JSON dono kyun?
    Answer: CSV spreadsheet ke liye, JSON dusre tool ke liye. Dono same fields rakhte hain, taaki farak na pade.
    Trade-off: Do writers maintain karne padte hain. Test JSON ko check karta hai.
    Follow-up: `estimate_label` kyun hai? Taaki null savings ko zero dollar na padh lo.

14. Cost Explorer ko optional kyun rakha?
    Answer: CE permission har account mein nahi hoti, aur woh actual bill deta hai. Is tool ka sample CE ko call nahi karta. IAM example mein action likha hai taaki baad mein jod sako.
    Trade-off: Bina CE ke estimate public price se bhi weak hota hai.
    Follow-up: CUR aur Athena project 5 mein nahi hain. Woh alag, bada design hai.

15. Pitch?
    Answer: "Maine ek dry-run reporter banaya jo synthetic inventory se idle candidates, loose disks, loose IPs, aur tag gaps nikalta hai. Savings tab likhta hai jab price do, aur sample report mein maine koi monthly saving nahi dikhayi. AWS resource change default path par nahi hota."
    Trade-off: Live account demo nahi hai.
    Follow-up: Kaun si file report hai? `evidence/sample-report.json` after tests.
