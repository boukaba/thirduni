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
1. Spoofing – Someone logs in as another student and uploads fake files.
2. Tampering – A student alters or overwrites another user’s recording.
3. Repudiation – A student deletes their upload and denies ever doing it.
4. Information Disclosure – Uploaded videos or names are visible to others.
5. Denial of Service – Students spam giant video files and slow the system.
6. Elevation of Privilege – A student accesses the teacher area or grades.


---

## Feature 2: Teacher – Provide Lesson Feedback 🎹

A teacher reviews student submissions and leaves comments or grades.

Possible STRIDE threats:
1. S — Spoofing: a student spoofs a teacher account and leaves feedback on their own video
2. T — Tampering: a student intercepts a feedback request and tweaks the teacher's rating or comment before it is saved
3. R — Repudiation: a teacher edits or deletes a comment and then insists they never did (no audit trail or timestamp)
4. I — Information Disclosure: the feedback page accidentally shows other students' videos, or the API returns too much information
5. D — Denial of Service: multiple teachers upload a lot of feedback files at once, portal slows down or crashes
6. E — Elevation of Privilege: a teacher finds a hidden admin page and can see every student's videos