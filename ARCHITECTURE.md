# 🎨 Visual Guide & Architecture Diagrams

## Application Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APPLICATION                     │
│                  (requirement_ticket.py)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    USER INTERFACE                         │   │
│  │  ┌──────────────────────────────────────────────────┐    │   │
│  │  │ Input Text Area                                  │    │   │
│  │  │ (Paste or type business requirement)            │    │   │
│  │  └──────────────────────────────────────────────────┘    │   │
│  │              ↓ [Analyze & Generate Ticket]               │   │
│  │  ┌──────────────────────────────────────────────────┐    │   │
│  │  │ Sidebar Configuration                           │    │   │
│  │  │ • Confidence Threshold (0.0 - 1.0)              │    │   │
│  │  │ • Help & Documentation                          │    │   │
│  │  │ • Entity Legend                                 │    │   │
│  │  └──────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         ↓                                         │
├─────────────────────────────────────────────────────────────────┤
│                    NLP PROCESSING ENGINE                          │
│                (requirement_processor.py)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              REQUIREMENT PROCESSOR                      │     │
│  │                                                         │     │
│  │  1. TEXT PREPROCESSING                                 │     │
│  │     └─ spaCy Tokenization & POS Tagging               │     │
│  │                                                         │     │
│  │  2. ENTITY EXTRACTION                                  │     │
│  │     ├─ Pattern-based NER (8 entity types)             │     │
│  │     ├─ Entity Ruler patterns matching                 │     │
│  │     └─ Dependency parsing enrichment                  │     │
│  │                                                         │     │
│  │  3. REQUIREMENT CLASSIFICATION                         │     │
│  │     ├─ Keyword detection                              │     │
│  │     ├─ Entity scoring                                 │     │
│  │     └─ Confidence calculation                         │     │
│  │                                                         │     │
│  │  4. ANALYSIS & HIGHLIGHTING                            │     │
│  │     ├─ Keyword extraction                             │     │
│  │     ├─ Text highlighting                              │     │
│  │     └─ Confidence metrics                             │     │
│  │                                                         │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
							↓
┌─────────────────────────────────────────────────────────────────┐
│                      ANALYSIS RESULTS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐    ┌─────────────────────┐              │
│  │ REQUIREMENT STATUS  │    │ CONFIDENCE METRICS  │              │
│  │ ✅ Valid            │    │ • Req Score: 85%    │              │
│  │ or                  │    │ • Extract: 82%      │              │
│  │ ❌ Not Valid        │    │ • Entities: 5       │              │
│  └─────────────────────┘    └─────────────────────┘              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         HIGHLIGHTED TEXT WITH ENTITY TAGS              │    │
│  │                                                         │    │
│  │ We need [STAKEHOLDER: user] to [ACTION: track]         │    │
│  │ [OBJECT: fitness goals] in [SYSTEM: mobile app]        │    │
│  │ that is [QUALITY: secure] and [QUALITY: scalable]      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │            EXTRACTED ENTITIES                           │    │
│  │                                                         │    │
│  │  Primary:                                               │    │
│  │  • Stakeholder: user                                   │    │
│  │  • Action: track                                        │    │
│  │  • Object: fitness goals                               │    │
│  │  • System: mobile application                          │    │
│  │                                                         │    │
│  │  Secondary:                                             │    │
│  │  • Priority: medium                                     │    │
│  │  • Quality: secure, scalable                           │    │
│  │  • Constraints: None                                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              VISUALIZATIONS                             │    │
│  │  • Confidence Breakdown (Plotly Bar Chart)             │    │
│  │  • Metrics Dashboard (4 Key Stats)                     │    │
│  │  • Entity Legend (8 Color-coded Types)                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         GENERATED BUSINESS REQUIREMENT TICKET          │    │
│  │                                                         │    │
│  │ {                                                       │    │
│  │   "ticket_id": "REQ-ABC12345",                          │    │
│  │   "is_requirement": true,                              │    │
│  │   "requirement_confidence": 0.85,                      │    │
│  │   "stakeholder": "user",                               │    │
│  │   "action": "track",                                    │    │
│  │   "object": "fitness goals",                           │    │
│  │   ...                                                   │    │
│  │ }                                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────┐    ┌─────────────────────┐              │
│  │ EXPORT OPTIONS      │    │ SHARE OPTIONS       │              │
│  │ • JSON              │    │ • Copy Ticket       │              │
│  │ • CSV               │    │ • Share Link (URL)  │              │
│  │ • Full Analysis     │    │ • Email              │              │
│  └─────────────────────┘    └─────────────────────┘              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
START
  ↓
┌─────────────────────┐
│  USER ENTERS TEXT   │
│  "We need a mobile  │
│   app for users to  │
│   track fitness"    │
└─────────────────────┘
  ↓
┌──────────────────────────────┐
│  STREAMLIT: receive input    │
│  Display preview & metrics   │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ SPACY: tokenize & parse      │
│                              │
│ Tokens: [We, need, a, ...]   │
│ Deps: [nsubj, ROOT, det, ...]│
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ ENTITY RULER: pattern match  │
│                              │
│ Match: STAKEHOLDER "users"   │
│ Match: ACTION "track"        │
│ Match: OBJECT "fitness"      │
│ Match: SYSTEM "app"          │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ DEPENDENCY PARSING: enrich   │
│                              │
│ Extract subject from nsubj   │
│ Extract predicate from ROOT  │
│ Extract object from dobj     │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ CONFIDENCE SCORING           │
│                              │
│ Count entities: 4            │
│ Base confidence: 4/5 = 80%   │
│ Boost: +30% (has key ents)   │
│ Final: 100% (capped)         │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ REQUIREMENT CLASSIFICATION   │
│                              │
│ Req keywords found: "need"   │
│ Score: 0.4 (40%)             │
│ Entity score: 0.3 (30%)      │
│ Object score: 0.15 (15%)     │
│ Quality score: 0.15 (15%)    │
│ Total: 1.0 (100%) = YES      │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ CREATE TICKET                │
│                              │
│ {                            │
│   ticket_id: REQ-ABC123      │
│   is_requirement: true       │
│   stakeholder: user          │
│   action: track              │
│   ...                        │
│ }                            │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ RENDER RESULTS               │
│                              │
│ • Status badge               │
│ • Metrics cards              │
│ • Highlighted text           │
│ • Charts                      │
│ • Extracted entities         │
│ • Ticket JSON                │
│ • Export buttons             │
└──────────────────────────────┘
  ↓
┌──────────────────────────────┐
│ USER ACTIONS                 │
│                              │
│ ├─ Download JSON             │
│ ├─ Download CSV              │
│ ├─ Copy Ticket               │
│ ├─ Try Another Text          │
│ └─ Adjust Settings           │
└──────────────────────────────┘
  ↓
END
```

## Entity Extraction Process

```
Original Text:
"We need a mobile app that allows users to securely track their fitness"

						↓

TOKENIZATION:
[We] [need] [a] [mobile] [app] [that] [allows] [users] [to] [securely] 
[track] [their] [fitness]

						↓

POS TAGGING:
We(PRP) need(VB) a(DT) mobile(JJ) app(NN) that(WDT) allows(VBZ) 
users(NNS) to(TO) securely(RB) track(VB) their(PRP$) fitness(NN)

						↓

DEPENDENCY PARSING:
need
├─ nsubj: We
├─ dobj: app
│  └─ amod: mobile
└─ xcomp: track
   ├─ aux: allows
   ├─ dobj: fitness
   └─ advmod: securely

						↓

PATTERN MATCHING (Entity Ruler):
✓ "We" matches STAKEHOLDER pattern → organization
✓ "users" matches STAKEHOLDER pattern → user
✓ "track" matches ACTION pattern
✓ "fitness" matches OBJECT pattern
✓ "app" matches SYSTEM pattern
✓ "securely" matches QUALITY pattern → secure

						↓

EXTRACTED ENTITIES:
{
  "stakeholder": ["organization", "user"],
  "action": "track",
  "object": "fitness",
  "system": "app",
  "quality": "secure",
  ...
}

						↓

DEPENDENCY ENRICHMENT:
• Root verb "need" → primary action
• Subject "We" (nsubj) → stakeholder
• Direct object → what is tracked (fitness)
• Primary verb "track" (xcomp) → actual action
• Adverbial "securely" → quality attribute

						↓

FINAL ENTITIES:
{
  "stakeholder": "user",
  "action": "track",
  "object": "fitness",
  "system": "mobile app",
  "quality": "secure",
  "confidence": 0.95
}
```

## Entity Type Reference Matrix

```
┌──────────────┬─────────────┬──────────────────────┬──────────────────┐
│ ENTITY TYPE  │ COLOR       │ EXAMPLES             │ EXTRACTION METHOD│
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ STAKEHOLDER  │ 🔵 BLUE     │ user, admin,         │ Pattern match    │
│              │             │ customer, developer  │ + dependency     │
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ ACTION       │ 🟡 YELLOW   │ create, track,       │ Verb lemma match │
│              │             │ update, manage       │ + modal verbs    │
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ OBJECT       │ 🔷 CYAN     │ report, data,        │ Noun pattern     │
│              │             │ notification         │ + dobj/pobj      │
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ SYSTEM       │ 🟣 PURPLE   │ application,         │ Pattern match    │
│              │             │ platform, API        │ + domain terms   │
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ QUALITY      │ ⚫ GRAY      │ secure, scalable,    │ Adjective pattern│
│              │             │ reliable, fast       │ + attribute terms│
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ PRIORITY     │ 🔴 RED      │ high, medium, low,   │ Keyword match    │
│              │             │ critical, urgent     │ + mapping        │
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ CONDITION    │ 🔷 TEAL     │ when, if, after,     │ advcl/mark       │
│              │             │ before, while        │ + subtree span   │
├──────────────┼─────────────┼──────────────────────┼──────────────────┤
│ CONSTRAINT   │ 🟣 MAGENTA  │ within 2 seconds,    │ Numeric match    │
│              │             │ max 1000 users       │ + time units     │
└──────────────┴─────────────┴──────────────────────┴──────────────────┘
```

## Confidence Scoring Breakdown

```
REQUIREMENT CONFIDENCE CALCULATION
═══════════════════════════════════

Input: "We need a mobile app that securely allows users to track fitness"

Step 1: Keyword Detection
┌─────────────────────────────────┐
│ Requirement Keywords Found:     │
│ ✓ "need" → requirement keyword  │
│ ✓ "track" → action verb         │
│                                 │
│ Score: 0.40 (40% weight)        │
└─────────────────────────────────┘

Step 2: Entity Detection
┌─────────────────────────────────┐
│ Key Entities Present:           │
│ ✓ Stakeholder: user             │
│ ✓ Action: track                 │
│ ✓ Object: fitness               │
│                                 │
│ All 3 present → Score: 0.30     │
│ (30% weight)                    │
└─────────────────────────────────┘

Step 3: Object Extraction
┌─────────────────────────────────┐
│ Object Detected:                │
│ ✓ "fitness" as object           │
│ ✓ Extracted successfully        │
│                                 │
│ Score: 0.15 (15% weight)        │
└─────────────────────────────────┘

Step 4: Quality Attributes
┌─────────────────────────────────┐
│ Quality Keywords:               │
│ ✓ "secure" (security/safety)    │
│                                 │
│ Score: 0.15 (15% weight)        │
└─────────────────────────────────┘

═════════════════════════════════════
FINAL SCORE: 0.40 + 0.30 + 0.15 + 0.15 = 1.0 (100%)
═════════════════════════════════════

CLASSIFICATION: ✅ IS A REQUIREMENT
```

## User Interface Sections

```
╔═══════════════════════════════════════════════════════════════════╗
║                   BUSINESS REQUIREMENT TICKET GENERATOR            ║
║              Transform unstructured text into structured tickets   ║
╚═══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ ⚙️  SIDEBAR CONFIGURATION                                       │
│                                                                 │
│ Confidence Threshold: ▁▂▃▄▅▆▇█ 0.50                             │
│                                                                 │
│ 📖 How it works                                                 │
│ 🏷️ Entity Types                                                │
│ 📚 Examples                                                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 📝 INPUT TEXT                │ ✨ PREVIEW                       │
│ ┌──────────────────────────┐│ ┌──────────────────────────────┐ │
│ │ Paste or type your       ││ │ Text Preview:                 │ │
│ │ business requirement:    ││ │                              │ │
│ │                          ││ │ We need a mobile app...      │ │
│ │ [4-line text area]       ││ │                              │ │
│ │                          ││ │                              │ │
│ │                          ││ │                              │ │
│ │                          ││ │                              │ │
│ └──────────────────────────┘│ │                              │ │
│                             │ │                              │ │
│                             │ │                              │ │
│                             │ └──────────────────────────────┘ │
│                                                                 │
│ [━━━━ 🚀 Analyze & Generate Ticket ━━━━]                       │
└──────────────────────────────────────────────────────────────────┘

AFTER ANALYSIS:
═══════════════════════════════════════════════════════════════════

┌───────────────────────────────────────────────────────────────┐
│ ✅ Valid Business Requirement                                 │
│ This text has been identified as a business requirement with  │
│ high confidence.                                              │
└───────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Requirement  │ Extraction   │ Entities     │ Keywords     │
│ Score        │ Confidence   │ Found        │ Found        │
│              │              │              │              │
│    92%       │     82%      │      5       │      7       │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌──────────────────────────────────┬─────────────────────────────┐
│ 🔍 HIGHLIGHTED TEXT              │ 📈 CONFIDENCE BREAKDOWN     │
│                                  │                             │
│ We [STAKEHOLDER: user] to         │ Requirement Score: █████░ │
│ [ACTION: track] [OBJECT: fitness] │ Extraction Conf:   ████░░ │
│ in [SYSTEM: mobile app] that is   │                             │
│ [QUALITY: secure]                 │                             │
│                                  │ Entity Legend:              │
│ [Legend showing 8 colors]         │ 🔵 Stakeholder             │
│                                  │ 🟡 Action                  │
│                                  │ 🔷 Object                  │
│                                  │ ... (8 types)              │
└──────────────────────────────────┴─────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 🏷️ EXTRACTED ENTITIES                                        │
│                                                              │
│ Primary Entities:        │ Secondary Attributes:            │
│ 👤 Stakeholder: user     │ 🎯 Priority: medium              │
│ ⚙️ Action: track         │ ⭐ Quality: secure               │
│ 📦 Object: fitness       │ 🔄 Condition: (none)             │
│ 🖥️ System: app           │ ⏱️ Constraint: (none)            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 🔑 KEYWORDS ANALYSIS                                         │
│                                                              │
│ Requirement Keywords:    │ Quality Keywords:                │
│ `need` `track` `app`     │ `secure` `user-friendly`         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 🎫 GENERATED BUSINESS REQUIREMENT TICKET                     │
│                                                              │
│ {                                                            │
│   "ticket_id": "REQ-ABC12345",                               │
│   "title": "TRACK - fitness",                                │
│   "is_requirement": true,                                    │
│   "requirement_confidence": 0.92,                            │
│   "stakeholder": "user",                                     │
│   "action": "track",                                         │
│   "object": "fitness",                                       │
│   ...more fields...                                          │
│ }                                                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────┬──────────────────┬──────────────────┐
│ 📥 JSON Download │ 📋 CSV Download  │ 📊 Full Analysis │
└──────────────────┴──────────────────┴──────────────────┘
```

## Installation & Setup Flow

```
START
  ↓
┌────────────────────────────────┐
│ CHOOSE YOUR PLATFORM           │
├────────────────┬───────────────┤
│ Windows        │ Mac / Linux   │
└────────────────┴───────────────┘
  ↓              ↓
 OPTION A       OPTION B
┌──────────────┐ ┌──────────────┐
│ quickstart   │ │ bash         │
│ .bat         │ │ quickstart   │
│ (automatic)  │ │ .sh          │
└──────────────┘ │ (automatic)  │
  ↓              │ ┌──────────────┘
  │              │
  └──────────────┼─→ OR MANUAL SETUP
				 │
		┌────────┴────────┐
		↓                 ↓
   python -m venv venv
   source venv/bin/activate
   pip install dependencies
   python -m spacy download en_core_web_sm
		↓
   ┌──────────────────────────────┐
   │ streamlit run                │
   │ requirement_ticket.py        │
   └──────────────────────────────┘
		↓
   ✅ App running at:
	  http://localhost:8501
		↓
   🎉 READY TO USE
```

---

**Note**: These diagrams provide a visual understanding of the application architecture and data flow. For detailed information, refer to the documentation files.
