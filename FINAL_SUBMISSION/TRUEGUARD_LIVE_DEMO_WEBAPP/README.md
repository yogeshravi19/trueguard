# TRUEGUARD™ Live Demo WebApp: Vercel & Local Deployment Guide

An interactive, live web demonstration comparing:
- **WITHOUT TRUEGUARD:** Baseline TinyLlama-1.1B emitting hallucinations blindly.
- **WITH TRUEGUARD:** Real-time 4-sensor interception (ISP, AAS, EEM, DST) and 3-tier closed-loop mitigation (Safe Pass, Targeted RAG, Calibrated Refusal).

---

## 1. Instant Local Demo (0 Seconds Setup)
Simply **double-click** `index.html` on any laptop or phone browser!
- Works 100% offline with zero external dependencies.
- Full interactive token clicking, real-time telemetry animation, and category tabs.

Or launch via Python local server:
```bash
python -m http.server 8080
```
Then open: http://localhost:8080

---

## 2. Instant Free Vercel Hosting (Under 60 Seconds)

### Option A: Drag & Drop via GitHub (Easiest)
1. Push this folder to a new GitHub repository (e.g. `trueguard-live-demo`).
2. Go to https://vercel.com/new and log in with GitHub.
3. Select your repository and click **Deploy**.
4. In ~15 seconds, Vercel gives you a permanent HTTPS public URL (e.g., `https://trueguard-live-demo.vercel.app`) that you can present to the review panel!

### Option B: Deploy from Terminal (Vercel CLI)
Inside this folder, run:
```bash
npx vercel
```
1. Accept defaults by pressing `Enter`.
2. Vercel automatically deploys `index.html` using the included `vercel.json`.

---

## Capstone Research Details
- **Project Title:** Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies
- **Candidate:** Yogesh Ravi M (22MIA1052)
- **Faculty Guide:** Dr. Pradeep Kumar T.S.
- **School:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Chennai
