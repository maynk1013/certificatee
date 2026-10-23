# Project 7 interview notes

## Architecture, Hinglish

Pehle secret code mein tha. Ab woh function error deti hai. Asli value store mein hai. App sirf provider se padhti hai aur log mein yeh likhti hai ki secret present hai, value nahi.

Local store versions rakhta hai. Rotation naya version likhti hai, verify karti hai, fail ho to pointer piche le jaati hai. AWS provider `GetSecretValue` call karta hai. Tests fake client use karte hain. Real secret create nahi hua.

Kubernetes `secretKeyRef` use karta hai. Terraform secret version set nahi karta, taaki value state mein na jaaye.

## Questions

1. Hardcoded secret sabse bada risk kya hai?
   Answer: Git history mein value reh jaati hai. Repo public ho to woh leak hai. Isliye value file mein thi hi nahi. Purana function ab raise karta hai.
   Trade-off: Example kam dramatic dikhta hai kyunki maine real-looking key commit nahi ki.
   Follow-up: Agar key commit ho gayi to pehle rotate, phir history. Sirf latest file se delete karna kaafi nahi.

2. Base64 Secret Kubernetes mein safe hai?
   Answer: Nahi. Base64 encoding hai. etcd encryption aur RBAC alag se chahiye. Project 1 EKS module encryption config dikhata hai, apply nahi hua.
   Trade-off: Encryption key ke bina secret phir bhi cluster admin ko dikh sakta hai.
   Follow-up: `stringData` bhi base64 hi store hota hai.

3. App secret log kyun nahi karti?
   Answer: Log aggregators lamba jeete hain. Test check karta hai value caplog mein nahi hai. Status mein sirf length aur present flag hai.
   Trade-off: Debug mushkil hota hai. Presence aur length kaafi hona chahiye.
   Follow-up: Exception message mein bhi value mat daalo. AccessDenied test yeh dekhta hai.

4. Rotation fail ho to recovery?
   Answer: Store pointer previous version par jaata hai. Purana value delete nahi hota. Evidence file value nahi likhti.
   Trade-off: Purane versions retain karna unhe protect karne ka kaam bhi banata hai.
   Follow-up: Dono versions kharab hon to naya known value likho, ticket mein value mat chipkao.

5. IRSA kya hai?
   Answer: Pod ka service account AWS role assume karta hai. Access key pod mein nahi hoti. Manifest mein annotation placeholder hai, real role nahi.
   Trade-off: OIDC provider cluster par hona chahiye. Yeh setup yahan apply nahi hua.
   Follow-up: Node role ko secret permission dena kyun loose hai? Har pod us node par wahi role le sakta hai.

6. Terraform secret value kyun nahi rakhta?
   Answer: Value state mein chali jaati hai. Resource sirf khali secret create karta hai, aur woh bhi flag true hone par. Value CLI se daalni hai, approval ke baad.
   Trade-off: Pehli value manual step hai. Woh better hai state leak se.
   Follow-up: `outputs` mein value kyun nahi? Sirf ARN, aur woh bhi tab jab resource bane.

7. Least privilege policy kis resource par hai?
   Answer: `GetSecretValue` aur `DescribeSecret` ek secret name ke ARN par. `secretsmanager:*` nahi hai.
   Trade-off: Name badla to policy update chahiye. Wildcard suffix AWS ke random suffix ke liye hai.
   Follow-up: `PutSecretValue` is policy mein kyun nahi? Reader ko rotate nahi karna chahiye.

8. Secret scanner kya pakadta hai?
   Answer: Private key header, `AKIA` plus 16 letters, aur Slack webhook URL. Test ek generated sample par fail karta hai aur repo par clean expect karta hai.
   Trade-off: Yeh gitleaks jaisa complete nahi hai. High entropy passwords miss ho sakte hain.
   Follow-up: Scanner ko CI mein tab bhi rakho jab woh basic ho, lekin uspar akela bharosa mat karo.

9. Kubernetes secret aur Secrets Manager dono kyun?
   Answer: App ko env chahiye, AWS ko source of truth. CSI driver ya external-secrets value ko Kubernetes secret mein laata hai. Yeh repo reference dikhata hai, driver install nahi karta.
   Trade-off: Sync delay aur extra controller.
   Follow-up: Env var process list mein dikh sakta hai. File mount kab better hai?

10. Vault kyun nahi?
    Answer: Local file store aur AWS interface dono test hue. Vault server install nahi tha. Main Vault backup ko is project ka tested part nahi bolta. Source resume par Vault ka alag purana project hai.
    Trade-off: Do products ek resume par confuse karte hain. Alag rakho.
    Follow-up: Vault dynamic secrets rotation se kaise alag hain?

11. Audit kis log se aata hai?
    Answer: AWS par CloudTrail `GetSecretValue` dikhata hai. Yahan CloudTrail query nahi chali. Local par application log sirf presence dikhati hai.
    Trade-off: Bina audit ke pata nahi chalta kaun sa pod padh raha tha.
    Follow-up: AccessDenied ko incident mana jayega agar woh unexpected principal se aaye.

12. Revocation?
    Answer: Naya version likho, purane version ko disable karo, aur jahan value gayi ho wahan se hatao. Yeh AWS step documented hai, execute nahi hua.
    Trade-off: Disable karte hi purane consumers tootenge. Pehle naya version verify karo.
    Follow-up: Local store rollback disable nahi karta, pointer hilata hai.

13. CI logs mein secret kaise aata hai?
    Answer: `set -x` ya `terraform output` value print kar de. Is repo ka output ARN tak hai. Test generated artifacts mein value na ho, yeh evidence JSON check karta hai.
    Trade-off: Debug flags pipeline par band rakhne padte hain.
    Follow-up: Masked variable bhi echo ho sakta hai kuch runners par. Mask par bharosa akela kaafi nahi.

14. Incident response order?
    Answer: Leak roko, value rotate karo, access revoke karo, phir Git history aur tickets saaf karo, phir timeline likho. Secret ko chat mein dobara mat bhejo.
    Trade-off: Forensics ke liye purana value chahiye ho to use password manager mein rakho, issue body mein nahi.
    Follow-up: Kaun se log is repo khud karta hai? Presence only.

15. Pitch?
    Answer: "Maine demo app ko provider based secret read par shift kiya, local rotation aur rollback test kiya, aur logs mein value na aaye yeh assert kiya. AWS call fake client se test hua. Real secret create nahi kiya."
    Trade-off: Live Secrets Manager console demo nahi hai.
    Follow-up: Kaun sa test sabse important hai? Log redaction wala.
