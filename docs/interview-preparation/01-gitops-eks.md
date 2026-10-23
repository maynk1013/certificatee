# Project 1 interview notes

## Architecture, Hinglish

Terraform pehle VPC banata hai. Public subnet sirf load balancer ya NAT ke liye hai. Worker nodes private subnet mein rehte hain, taaki unka IP seedha internet par na khule. IAM module do roles banata hai: ek EKS control plane ke liye, ek nodes ke liye. Policy attach EKS module mein hai, isliye cluster tab tak start nahi hota jab tak policy lag na jaaye.

Helm chart Deployment likhta hai. Liveness bolti hai process zinda hai ya nahi. Readiness bolti hai traffic dena hai ya nahi. Argo CD Git ko dekhta hai aur cluster ko usi tarah rakhne ki koshish karta hai. Prometheus numbers uthata hai. Alertmanager Slack tab bolega jab webhook file maujood ho.

Is machine par cluster create nahi hua. Interview mein yeh clearly bolo.

## Questions

1. GitOps aur normal CI/CD mein farak kya hai?
   Answer: CI image bana aur test karta hai. GitOps mein cluster ki desired state Git mein rehti hai, aur Argo CD usse reconcile karta hai. Deploy script cluster par kubectl chalaye, yeh zaroori nahi.
   Trade-off: GitOps ka audit achha hota hai, lekin drift aur prune galat ho to resource delete ho sakta hai.
   Follow-up: Prune kab band rakhoge? Jab CRD ya shared namespace ho.

2. VPC mein public aur private subnet kyun?
   Answer: Private subnet nodes ko direct inbound se bachata hai. NAT unhe outbound deta hai, jaise image pull.
   Trade-off: NAT gateway ka hourly cost hota hai. Bina NAT ke private nodes image pull nahi kar paate jab tak VPC endpoint na ho.
   Follow-up: S3 aur ECR ke liye VPC endpoints NAT cost kaise kam karte hain?

3. EKS control plane IAM aur node IAM alag kyun hain?
   Answer: Control plane AWS managed Kubernetes API chalata hai. Node EC2 hai jo kubelet aur CNI chalata hai. Dono ke trust policies alag services par hain: `eks.amazonaws.com` aur `ec2.amazonaws.com`.
   Trade-off: Node par `AmazonEKS_CNI_Policy` convenient hai, lekin IRSA se CNI ka role alag karna tighter hai.
   Follow-up: IRSA OIDC provider kis resource se aata hai?

4. Public API endpoint band rakhne ka asar kya hai?
   Answer: `endpoint_public_access = false` ka matlab laptop se seedha `kubectl` nahi chalega. Bastion, VPN, ya SSM chahiye.
   Trade-off: Zyada secure, lekin break-glass access sochna padta hai.
   Follow-up: Public access on karo to CIDR restriction ke bina kya risk hai?

5. Kubernetes secret encryption alag se kyun?
   Answer: etcd mein secret base64 hota hai, encrypted nahi. EKS encryption config KMS se secret resources encrypt karta hai.
   Trade-off: KMS key delete ho gayi to secret read nahi honge. Key rotation enable hai is module mein.
   Follow-up: Base64 encoding ko encryption kyun nahi kehte?

6. Liveness aur readiness mein farak?
   Answer: Liveness fail hone par kubelet container restart karta hai. Readiness fail hone par Service us pod ko traffic nahi deti, restart nahi karti.
   Trade-off: Slow startup par liveness tight ho to pod restart loop mein ja sakta hai.
   Follow-up: Is demo mein kaun sa path kaun si probe use karta hai? `/healthz` aur `/readyz`.

7. `maxUnavailable: 0` zero downtime sabit karta hai?
   Answer: Nahi. Yeh setting kehti hai rolling update mein purana pod tab tak na hate jab tak naya ready na ho. Isko measured zero downtime tab bolo jab load test ke dauran error rate dekha ho. Yahan woh test nahi hua.
   Trade-off: Update slow ho sakta hai aur extra pod ke liye capacity chahiye.
   Follow-up: `maxSurge: 1` ka matlab kya hai?

8. Argo CD self-heal kya karta hai?
   Answer: Koi cluster par manual change kare aur woh Git se alag ho, to Argo CD Git wali state wapas laga deta hai.
   Trade-off: Emergency hotfix jo sirf cluster par hai, woh mita diya jayega.
   Follow-up: Monitoring app par automated sync kyun band hai? Kyunki upstream chart upgrade pehle review honi chahiye.

9. Image tag `latest` kyun nahi?
   Answer: `latest` move hota hai. Git mein pata nahi chalta kaun si build cluster par hai. Is Dockerfile ka tag `python:3.12.11-slim` hai, aur chart mein tag alag value hai.
   Trade-off: Har release par values update karni padti hai. Yahi GitOps ka point hai.
   Follow-up: Digest pin tag pin se kaise better hai?

10. Prometheus alert ka denominator zero ho to?
    Answer: `clamp_min(..., 0.001)` division ko zero se bachata hai. Khali traffic par bhi expression number de sakta hai, isliye `for: 10m` aur real dashboard dono dekho.
    Trade-off: Clamp se bahut kam traffic par ratio distorted ho sakta hai.
    Follow-up: Absent series ke liye `up == 0` alag alert kyun hai?

11. Slack webhook Git mein kyun nahi?
    Answer: Webhook ek secret hai. Jo bhi us URL ko jaanta hai, channel mein post kar sakta hai. Alertmanager `api_url_file` use karta hai.
    Trade-off: File mount galat ho to alert silent rehta hai. Default receiver `null` hai taaki missing Slack poora Alertmanager na giraaye.
    Follow-up: Webhook rotate kaise karoge?

12. Terraform validate apply ke barabar hai?
    Answer: Nahi. Validate syntax aur types check karta hai. AWS account, quota, aur API errors plan ya apply par dikhte hain. Is repo ne apply nahi kiya.
    Trade-off: Validate sasta aur safe hai, lekin provider bugs nahi pakadta.
    Follow-up: `init -backend=false` state ko touch kyun nahi karta?

13. State file sensitive kyun hoti hai?
    Answer: State resource IDs aur kabhi kabhi attributes rakhti hai. Is EKS module ka CA output sensitive mark hai, phir bhi state mein data hota hai. State commit mat karo.
    Trade-off: Local state easy hai, team ke liye remote encrypted state chahiye.
    Follow-up: Project 3 ka lockfile isse kaise judta hai?

14. Dockerfile non-root user kyun hai?
    Answer: Container compromise hone par root se host par asar zyada ho sakta hai. User id 10001 chart ke `runAsUser` se match karta hai.
    Trade-off: Kuch images root ke bina port 80 bind nahi kar pati. Yahan port 8080 hai.
    Follow-up: Read-only root filesystem ke liye `/tmp` emptyDir kyun chahiye?

15. Interview mein is project ko 60 second mein kaise bolun?
    Answer: "Maine EKS ke liye Terraform modules likhe, ek health endpoint wali app ka Helm chart banaya, aur Argo CD plus Prometheus manifests git mein rakhe. Maine local par terraform validate, helm lint, aur pytest chalaye. AWS par cluster create nahi kiya, isliye main use running production nahi bolta."
    Trade-off: Honest scope chhota dikhta hai, lekin jhoot pakda gaya to interview kharab hota hai.
    Follow-up: Agar interviewer bole live dikhao, to kya chalaoge? Pytest, helm template, aur rollout nahi, yeh project 1 hai. Project 2 ka local log dikha sakte ho.
