## **Chapter 14: From Design Thinking to Mike Cohn’s User Stories**

When software fails, the root cause is rarely a missing semicolon; it is more often a mismatch between what was *built* and what real humans *need*. **Design Thinking** offers a disciplined empathy-first lens, while **user stories**—popularised by Mike Cohn—translate those fuzzy insights into small, testable increments for Agile teams.  This chapter traces the intellectual hand-off: from field interviews and empathy maps, through problem reframing, ideation, rapid prototypes, and finally to INVEST-compliant backlog items with acceptance criteria.  We will demonstrate how a single observation—tourists abandoning a bike because QR payment is confusing—travels through Define-Ideate-Prototype-Test and emerges as “*As a visitor I want a multi-language payment screen so that I can confirm the fee before scanning the QR*.”  By mastering this pipeline you will ensure that each sprint delivers not only code, but measurable value anchored in genuine user pain points.

---

### **1. Theories**

**1.1  Five-Stage Design Thinking Model**

1. **Empathise** – Immerse in the users’ environment; gather qualitative data via interviews, shadowing, diary studies.
2. **Define** – Synthesize findings into a *point-of-view* statement: *Bike renters struggle to trust digital payments when they cannot read Thai.*
3. **Ideate** – Divergent brainstorming (Crazy 8s, SCAMPER) followed by convergent selection (dot-votes, impact–effort matrix).
4. **Prototype** – Create low-fidelity artefacts (paper sketches, Figma wireframes) fast enough to throw away.
5. **Test** – Observe users interacting; capture frustration metrics (time-to-task, error count) and emotional cues.

The process is *non-linear*: Test insights often push teams back to Empathise or Ideate.

**1.2  Mike Cohn’s User Story Template**

> *As a \[actor] I want \[action] so that \[benefit].*

This linguistic skeleton forces clarity on *who* values the feature and *why*.  Good stories obey **INVEST**: *Independent, Negotiable, Valuable, Estimable, Small, Testable*.

**1.3  Acceptance Criteria & Given–When–Then**
While the story captures intent, *acceptance criteria* codify “done.”  Popularised in Behaviour-Driven Development:

```
Given   a visitor on the payment page
When    they select English
Then    fee, currency, and QR code are displayed in English
```

Criteria prevent the “definition of done” from drifting during development.

**1.4  MoSCoW & Kano Prioritisation**

* **MoSCoW**: Must-have, Should-have, Could-have, Won’t-have (this time).
* **Kano**: Basic, Performance, Exciters.  Helps product owners decide which stories enter the next sprint versus the parking lot.

**1.5  Story Mapping**
Jeff Patton’s technique arranges activities horizontally (user journey) and tasks vertically (increasing sophistication).  A release slice cuts horizontally; stories above the line ship, below are postponed.

**1.6  Linking Design Thinking to Stories**

* **Empathy Map** → Persona → Story *actor*.
* **Problem Statement** → Story *benefit*.
* **Prototype Feedback** → Acceptance criteria and Definition of Ready (DoR).
* **Test Metrics** → Definition of Done (DoD) and future *performance* stories.

**1.7  Anti-Patterns**

* Stories that bundle UI, backend, and DevOps: violate *Small* and *Independent*.
* Technical tasks disguised as stories (“Refactor payment module”): not directly *Valuable* to actor.
* Acceptance criteria reading like implementation (“use Tailwind class `bg-blue-500`”): breaks *Negotiable* principle.

**1.8  Large Story Breakdown**
Use *vertical slicing*: deliver thin end-to-end strips (UI→API→DB) rather than horizontal layers (all UI, then all API).  Tools: spike, tracer bullet, walking skeleton.

**1.9  Metrics for Success**

* *Lead time per story* (idea → prod).
* *Sprint Goal hit rate*.
* *User satisfaction* (System Usability Scale pre/post feature).
  Monitoring closes the feedback loop back to Design Thinking’s Test stage.

---

### **2. Step-by-Step Workshop**

* **Empathise**

  * Conduct a 15-min interview with a classmate acting as first-time tourist.
* **Define**

  * Write a POV: *\[Name] needs a way to … because …*.
* **Ideate**

  * Crazy 8s: fold paper, sketch 8 UI ideas in 8 minutes.
* **Prototype**

  * Pick top sketch; build Figma wireframe (2 screens max).
* **Test**

  * Perform a 3-minute usability test; record one quote and one metric.
* **Translate to Stories**

  * Craft 3 user stories with Given–When–Then.
  * Classify each under MoSCoW.
* **Map** stories on a simple board: columns = journey steps, rows = release slices.

---

### **3. Assignment**

* **Deliverables**

  1. PDF of empathy map and persona.
  2. Point-of-view problem statement.
  3. Three INVEST-compliant user stories with acceptance criteria.
  4. Story map screenshot (Miro/FigJam/whiteboard).
* **Reflection** (200 words): Compare how the usability test altered your original story assumptions.

---

### **4. Conclusion**

Integrating Design Thinking with Mike Cohn’s user stories ensures that empathy-derived insights survive translation into Agile backlogs.  Each story becomes a contract between product intent and engineering execution, while acceptance criteria couple UX quality with automated tests.  Practised iteratively, this pipeline transforms vague problems into measurable releases that delight users and satisfy sprint metrics—closing the virtuous loop of human-centred software development.
