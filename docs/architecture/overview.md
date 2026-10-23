# Portfolio architecture

The seven projects are independent folders. They share ideas, not a single runtime. A recruiter can open one project without installing the others.

```mermaid
flowchart TB
  p1[01 GitOps EKS]
  p2[02 Progressive delivery]
  p3[03 Multi-environment Terraform]
  p4[04 Observability]
  p5[05 Cost reporter]
  p6[06 Backup drill]
  p7[07 Secrets]
  p1 --> p2
  p1 --> p4
  p3 --> p1
  p6 --> p1
  p7 --> p1
  p5 --> p3
```

What was exercised on this machine is recorded in the root README after the validation commands. AWS apply, image push, and a live Kubernetes install were not part of that run.

## Hinglish

Pehle network aur permissions ka design aata hai, phir application, phir usko safely release karna, phir usko dekhna, phir paise aur backup, aur last mein secret. Isliye folders ka number bhi yahi order follow karta hai. Har folder apna test khud chalata hai.
