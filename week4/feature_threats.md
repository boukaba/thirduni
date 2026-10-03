# Feature Threat Modelling 🎶

     /\_/\
    ( o.o )
     > ^ <   let's think like a developer

Below are two key features from a music school portal — one for a student and one for a teacher.

For each feature, think through the six STRIDE categories and note what could go wrong.

---

## Feature 1: Student – Upload Practice Recording 🎤

A student logs in and uploads their weekly practice video for their teacher to review.

Possible STRIDE threats:
1. S — Spoofing: someone logs in as another student and uploads fake files
2. T — Tampering: a student alters or overwrites another user's recording
3. R — Repudiation: a student deletes their upload and denies ever doing it
4. I — Information Disclosure: uploaded videos or names could be visible to others
5. D — Denial of Service: students spam giant video files and slow the system
6. E — Elevation of Privilege: a student accesses the teacher area