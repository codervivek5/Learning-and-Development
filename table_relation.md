Bhai, aapke database tree (`nexora` database ke `public` schema) mein jo 5 tables dikh rahi hain—`organization`, `user`, `project`, `document`, aur `workflow_run`—unka aapas mein ek perfect **Multi-Tenant (SaaS) Architecture** ka relation hai.

In saari tables ke beech ke dynamic links aur connections ko aasan bhasha mein samajhte hain:

---

### 🏢 1. Core Tenant Room (`organization`)

Yeh aapke poore system ka root (baap) hai. Har ek company ya client jo aapke SaaS platform par register karegi, usko yahan ek unique entry milegi (jaise Genpact, Nexora etc.).

* Baki saari tables isko directly target karti hain taaki ek organization ka data doosri organization ko kabhi na dikhe (**Data Isolation**).

---

### 👥 2. Users Management (`user`)

* **Relation with Organization:** **Many-to-One (`INT REFERENCES organization(id)`)**
* **Matlab:** Ek organization ke andar kayi saare users (`SUPER_ADMIN`, `LEARNER`, `CREATOR`) ho sakte hain, lekin ek user kisi ek hi organization ka hissa hoga.

---

### 📂 3. Workspaces (`project`)

* **Relation with Organization:** **Many-to-One (`REFERENCES organization(id) ON DELETE CASCADE`)**
* **Relation with User:** Bhale hi ise kisi user ne banaya ho, par yeh query level par organization se scoped hota hai.
* **Matlab:** Ek organization ke andar multiple AI course-creation projects chal sakte hain. Agar poori organization hi delete ho jaye (`CASCADE`), toh uske saare projects automatic saaf ho jayenge.

---

### 📄 4. Knowledge Base Context (`document`)

* **Relation with Project:** **Many-to-One (`REFERENCES project(id) ON DELETE CASCADE`)**
* **Relation with Organization:** **Many-to-One (`REFERENCES organization(id)`)**
* **Matlab:** Jab aap AI training pipeline ke liye koi raw file ya metadata upload karte hain, toh woh kisi specific `project_id` ke andar mapping hold karti hai. Agar project delete hua, toh usse linked saare reference documents automatic drop ho jayenge.

---

### ⚙️ 5. Execution State (`workflow_run`)

* **Relation with Project:** **Many-to-One (`REFERENCES project(id) ON DELETE CASCADE`)**
* **Relation with Organization:** **Many-to-One (`REFERENCES organization(id)`)**
* **Matlab:** Jab bhi aap kisi project ke liye ADDIE AI Agent run karte hain, toh us particular processing iteration ke realtime state-data aur text logs is table mein save hote hain. Yeh hamesha ek single project aur single organization se linked hota hai.

---

### 📊 Quick ER-Diagram Summary Matrix

Aap asani se visual flow dekh sakte hain ki kaise saari foreign keys right direction mein refer kar rahi hain:

```
  ┌────────────────────────────────────────┐
  │              organization              │
  └────┬──────────────┬──────────────┬─────┘
       │              │              │
       ▼ (1:N)        ▼ (1:N)        ▼ (1:N)
   ┌───────┐      ┌─────────┐    ┌──────────────┐
   │ user  │      │ project │    │ document     │
   └───────┘      └────┬────┘    └──────┬───────┘
                       │                │
                       ├────────────────┤
                       ▼ (1:N)          ▼ (1:N)
                 ┌──────────────┐       │
                 │ workflow_run │◄──────┘
                 └──────────────┘

```

* Saari tables ke variable models aur data parameters bina change hue database tree mein ab isi perfect integrity constraints ke sath structured hain!