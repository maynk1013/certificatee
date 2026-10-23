# Project 3 interview notes

## Architecture, Hinglish

Module drawing hai, environment form hai. Dev, staging, aur prod alag folders hain, lekin networking, IAM, aur compute module same hain. CIDR aur tags tfvars json mein hain.

State ka design S3 plus `use_lockfile = true` hai, Terraform 1.10 ke baad. Lock isliye taaki do apply ek saath state na bigaden. Yeh lock real bucket par test nahi hua.

`create_compute` false hai. Matlab committed config instance nahi banati jab tak koi jaan bujh kar flag na badle.

## Questions

1. Environment folder aur workspace mein kya choose kiya?
   Answer: Alag folders. Har environment ki file khud padh kar samajh aa jaati hai. Workspace ek directory mein zyada chhupa hota hai.
   Trade-off: Teen jagah same module call repeat hoti hai.
   Follow-up: Terragrunt kab sochoge? Jab repetition actually hurt kare. Yahan nahi lagaya.

2. Remote state kyun?
   Answer: Laptop state team ke liye gayab ho jaati hai, aur usme sensitive attributes hote hain. S3 versioning se purani state mil sakti hai.
   Trade-off: Bucket permissions galat hon to state leak ho sakti hai.
   Follow-up: State mein password kyun nahi daalte?

3. DynamoDB lock aur S3 lockfile?
   Answer: Purana pattern DynamoDB tha. Terraform 1.10+ S3 backend `use_lockfile` se lock object rakhta hai. Is repo ka example wahi hai, kyunki pinned Terraform 1.14 hai.
   Trade-off: Purane runners 1.9 par yeh attribute nahi samajhte.
   Follow-up: Lock atka ho to force-unlock kab karoge? Jab pakka ho koi apply nahi chal raha.

4. `terraform validate` credentials kyun nahi maangta?
   Answer: Woh local configuration check hai. Plan AWS API se actual diff nikalta hai.
   Trade-off: Validate green hone ka matlab account mein apply safe hai, aisa nahi.
   Follow-up: Invalid fixture validate par fail kyun hoti hai? Kyunki HCL syntax toota hua hai.

5. Tag policy alag script kyun hai?
   Answer: Variable validation plan time par chalti hai, bina credentials ke CI plan nahi karna chahta. JSON checker committed files ko abhi padh leta hai.
   Trade-off: Koi resource tag module ke bahar chhoot sakta hai. Yeh required keys ko tfvars par check karta hai.
   Follow-up: `Environment=qa` kyun reject hoga? Allowed set dev, staging, prod hai.

6. Least privilege yahan kahan dikhta hai?
   Answer: Instance profile tab banta hai jab compute on ho. Policy describe calls ko `*` deti hai kyunki AWS un actions par resource ARN support nahi karta. Log write ek log group tak hai. SSH inbound nahi hai.
   Trade-off: `*` wala describe statement dekhne mein wide lagta hai. Isko explain karna zaroori hai.
   Follow-up: `ec2:*` kyun nahi diya?

7. IMDSv2 `http_tokens = required` kya bachata hai?
   Answer: Purana metadata service SSRF se role credentials le sakta tha. Tokens usko mushkil banate hain.
   Trade-off: Purani SDK bina token ke toot sakti hai.
   Follow-up: Hop limit 1 kyun rakhte hain containers ke case mein?

8. NAT prod tfvars mein true hai. Kya woh ban gaya?
   Answer: Nahi. Woh sirf configuration hai. Apply nahi hua. NAT ka cost tab aata hai jab resource create ho.
   Trade-off: Interviewer ko lag sakta hai prod VPC maujood hai. Clearly bolo nahi hai.
   Follow-up: NAT ke bina private subnet outbound kaise karegi?

9. Same module ko teen baar init kyun?
   Answer: Har environment alag root module hai, alag state key honi chahiye. Ek state mein teeno duniya rakhna risky hai.
   Trade-off: Init time badhta hai.
   Follow-up: State key example mein `ENV_NAME` replace karna kyun zaroori hai?

10. Encryption aur recovery?
    Answer: Example mein `encrypt = true` hai. Recovery bucket versioning se aati hai, jo is repo ne create nahi kiya. Documented control hai, tested control nahi.
    Trade-off: SSE-S3 simple hai. SSE-KMS alag audit deta hai aur key policy maangta hai.
    Follow-up: KMS key delete ho to state kaise khologi?

11. Checkov ya tfsec kyun optional rahe?
    Answer: tfsec ab Trivy ki taraf point karta hai. Checkov is machine par tabhi chala hai jab install successful ho. Root README woh fact likhega jo command ne dikhaya.
    Trade-off: Custom tag check Checkov jaisa deep nahi hai.
    Follow-up: Kaun sa misconfiguration tum khud pakadte ho? Missing owner, invalid HCL, public IP off, encrypted root volume.

12. `desired_capacity = 0` bhi paise le sakta hai?
    Answer: Haan, agar ASG, launch template, ya NAT create ho. Isliye `create_compute` false hai. Zero capacity ka matlab zero cost nahi hota.
    Trade-off: Flag false hone par reviewer ko lagta hai compute adhoora hai. README mein yeh safety switch hai.
    Follow-up: Apply se pehle plan file kaise review karoge?

13. Provider version pin kyun?
    Answer: `~> 5.82` 5.82 se 6 se pehle tak jaata hai. Terraform `>= 1.10, < 2` lockfile feature ke saath match karta hai.
    Trade-off: Pin purana pad sakta hai. Upgrade alag commit mein karo.
    Follow-up: Lock file commit karte ho ya nahi? Root modules ke `.terraform.lock.hcl` ko commit karna reproducibility ke liye better hai, agar init ke baad generate ho.

14. Default tags aur resource tags dono?
    Answer: Provider `default_tags` har supported resource par lagta hai. Module phir bhi Name tag merge karta hai.
    Trade-off: Kuch resources default tags support nahi karte.
    Follow-up: Cost allocation ke liye kaun se tags kaafi hain?

15. Is project ko interview mein kaise defend karoge?
    Answer: "Maine teen environments ko same modules se alag rakha, state locking ka Terraform 1.10 design likha, aur CI ko ek toota hua config reject karwaya. Apply nahi kiya."
    Trade-off: Live AWS console demo nahi hai.
    Follow-up: Agar bole account hai, to pehle plan dikhao, apply se pehle approval lo.
