# Project 6 interview notes

## Architecture, Hinglish

Do alag backups hain. Git Kubernetes YAML aur config ko yaad rakhta hai. Data file ka local drill checksum ke saath copy banata hai, corrupt karta hai, phir copy wapas laata hai.

AWS Backup vault aur daily plan Terraform mein hain, lekin `create_backup_resources` false hai. Cross-region copy false hai aur test nahi hua.

RPO kitna data kho sakte ho. RTO kitni der mein wapas aa sakte ho. Yahan 24 hours aur 4 hours targets hain, results nahi.

## Questions

1. RPO aur RTO?
   Answer: RPO last good copy kitni purani ho sakti hai. RTO restore shuru se service wapas tak ka time. Target likhna aur stopwatch se napna alag hai.
   Trade-off: Chhota RPO zyada frequent backup maangta hai.
   Follow-up: Daily backup par RPO target 24 hours us schedule se consistent hai. Usse chhota claim mat karo.

2. Git backup hai ya nahi?
   Answer: Manifests ke liye haan, kyunki desired state Git mein hai. Database bytes ke liye nahi. Dono ko ek backup mat bolo.
   Trade-off: Git history tab kaam ki hai jab repo khud safe ho. Repo ka backup alag sawal hai.
   Follow-up: Kaun si YAML git mein hai? `manifests/demo-web-deployment.yaml`.

3. Checksum kyun?
   Answer: Copy ban gayi, yeh kaafi nahi. Sha256 payload aur metadata ko milata hai. Tamper test fail hota hai.
   Trade-off: Checksum availability nahi deta. Woh sirf integrity hai.
   Follow-up: Size match ho aur hash na ho to bhi fail kyun?

4. Local elapsed time ko RTO kyun nahi bolte?
   Answer: Woh ek chhoti file ki copy ka time hai. AWS restore, DNS, aur app start usme nahi hain. JSON label yeh kehta hai.
   Trade-off: Number dikhta hai, log uska galat use kar sakte hain. Label padho.
   Follow-up: Asli RTO tab likhna jab poora drill stopwatch se napo.

5. Restore ko overwrite kyun nahi karte?
   Answer: Galat restore last good copy bhi mita sakta hai. Naye naam par restore karo, check karo, phir switch karo.
   Trade-off: Do copies ka cost. Woh safety ka cost hai.
   Follow-up: Drill local file ko corrupt karti hai sirf restore directory mein, source fixture ko nahi.

6. AWS Backup aur RDS automated backup?
   Answer: RDS apna backup rakh sakta hai. AWS Backup central policy de sakta hai. Yahan RDS instance hai hi nahi. Policy document dono options likhti hai.
   Trade-off: Do systems hone par retention confuse ho sakti hai. Ek owner choose karo.
   Follow-up: Point-in-time recovery daily snapshot se chhota RPO de sakti hai. Yahan PITR test nahi hua.

7. Cross-region tabhi jab budget ho?
   Answer: Copy ka storage aur transfer cost hota hai, aur har service support nahi karti. Flag false hai. Main cross-region recovery ko working nahi bolta.
   Trade-off: Region failure ka plan adhoora rehta hai. Us adhoore pan ko chhupana nahi hai.
   Follow-up: Destination vault ARN example mein placeholder account `000000000000` hai. Apply se pehle yeh galat hai, isliye flag off hai.

8. IAM `AWSBackupServiceRolePolicyForBackup` broad kyun hai?
   Answer: AWS ka managed role backup APIs ke liye aisa hi hota hai. Woh tab attach hota hai jab resources create hon. Default create false hai.
   Trade-off: Managed policy kam least-privilege hai. Custom policy likhna possible hai, par service actions miss ho sakte hain.
   Follow-up: Backup role ko admin role mat do.

9. EKS backup ka matlab kya hai?
   Answer: Stateless pods Git se phir ban sakte hain. Persistent volumes aur etcd alag se backup maangte hain. Is repo ne Velero ya AWS Backup for EKS restore test nahi kiya.
   Trade-off: "Cluster git mein hai" bolna PV data ko ignore karta hai.
   Follow-up: Demo deployment mein volume hai? Nahi. Data drill alag JSON file hai.

10. Approval gate kyun?
    Answer: Restore aur delete customer data chhoo sakte hain. Policy kehti hai create, restore, overwrite, delete se pehle approval.
    Trade-off: Incident mein approval slow lagta hai. Break-glass ko pehle se likho. Yahan break-glass account nahi banaya.
    Follow-up: CI mein apply job kyun nahi hai?

11. Retention 35 din aur minimum check 7 din?
    Answer: Policy 35 kehti hai. Validator 7 se neeche ko reject karta hai taaki test galat config pakde. 35, 7 se bada hai, isliye valid hai.
    Trade-off: Compliance kabhi 35 se lambi hoti hai. Yeh portfolio number ek example hai.
    Follow-up: Legal hold ho to delete_after mat chalao.

12. Failed restore par rollback?
    Answer: Naye resource ko hatao aur application ko purane Git commit par rakho. Original ko pehle hi mat mitao.
    Trade-off: Dono resources thodi der chalte hain.
    Follow-up: Runbook ka pehla AWS step kya hai? Recovery point hai bhi ya nahi, yeh confirm karo. Yahan recovery point create nahi hua.

13. Backup metadata mein secret kyun nahi?
    Answer: Metadata name, hash, size, retention rakhta hai. Data file synthetic orders hain, password nahi.
    Trade-off: Hash se content reverse nahi hota, lekin chhoti file ka hash dictionary se match ho sakta hai. Yahan file public synthetic hai.
    Follow-up: Real database dump ko Git mein mat daalo.

14. Test drill ko production drill mat bolo.
    Answer: Data synthetic hai, AWS involve nahi hai, aur scope ek file hai. Value yeh hai ki checksum aur restore automated hain.
    Trade-off: Interviewer zyada expect kare to honestly scope batao.
    Follow-up: Agle level par kya add karoge? Disposable RDS, approval ke baad, aur stopwatch.

15. Pitch?
    Answer: "Maine backup policy, git manifests, aur ek synthetic restore drill banaya jo checksum se integrity check karta hai. RPO aur RTO targets hain. AWS Backup config gated hai aur cross-region test nahi hua."
    Trade-off: Measured cloud RTO nahi hai.
    Follow-up: Evidence file ka naam? `evidence/local-restore-drill.json`.
