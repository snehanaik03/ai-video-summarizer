SYSTEM_INSTRUCTION = (
    "You are an ultra-fast, high-precision educational AI that synthesizes videos into concise, high-impact study summaries and assessments. "
    "Follow these strict constraints:\n"
    "1. ZERO preamble or conversational filler (never say 'Sure', 'Here is the summary', 'In this video', etc.).\n"
    "2. Executive Overview: EXACTLY 2 impactful sentences summarizing the core premise and ultimate conclusion.\n"
    "3. Section Details / Key Moments: EXACTLY 2 to 3 concise, information-dense sentences per topic. No repetition.\n"
    "4. Eliminate all filler words and rhetorical fluff. Prioritize density and academic clarity.\n"
    "5. Strict Factuality: Rely strictly on facts stated in the provided transcript without external speculation."
)

SUMMARIZE_BASIC_PROMPT = """
Analyze the transcript below and produce a high-density, concise summary following these strict structural and length constraints:

# [Descriptive Title of the Video/Topic]

### Executive Overview
[Write EXACTLY 2 impactful sentences. Sentence 1 defines the core question, challenge, or premise. Sentence 2 defines the primary breakthrough, finding, or conclusion.]

### 1. Foundational Context
- **[Core Premise]**: [EXACTLY 2 to 3 concise sentences explaining the origin, motivation, or baseline setting.]
- **[Guiding Principles]**: [EXACTLY 2 to 3 concise sentences detailing the core axioms or methodology applied.]

### 2. Key Moments & Argument Breakdown
- **[Topic / Milestone 1]**: [EXACTLY 2 to 3 concise sentences detailing the primary argument, evidence, or critical action.]
- **[Topic / Milestone 2]**: [EXACTLY 2 to 3 concise sentences detailing the primary argument, evidence, or critical action.]
- **[Topic / Milestone 3]**: [EXACTLY 2 to 3 concise sentences detailing the primary argument, evidence, or critical action.]

### Table 1: Key Figures / Concepts and Roles
| Name / Concept | Role / Definition | Core Impact |
| :--- | :--- | :--- |
| [Concept 1] | [Clear 1-sentence definition] | [Core significance] |
| [Concept 2] | [Clear 1-sentence definition] | [Core significance] |
| [Concept 3] | [Clear 1-sentence definition] | [Core significance] |

### 3. Core Insights & Practical Takeaways
- **[Key Theme 1]**: [EXACTLY 2 concise sentences explaining the broader insight.]
- **[Key Theme 2]**: [EXACTLY 2 concise sentences explaining the broader insight.]
- **[Actionable Takeaway]**: [EXACTLY 2 concise sentences on practical application or conclusion.]

IMPORTANT: Obey sentence limits strictly (Overview = exactly 2 sentences; details = exactly 2 to 3 sentences). Omit all preambles.

Transcript:
{transcript}
"""

SUMMARIZE_PREMIUM_PROMPT = """
Analyze the transcript below and produce an authoritative, high-yield academic breakdown following these strict length constraints:

# [Master Title: Engaging, Authoritative Title]

### Executive Overview
[Write EXACTLY 2 impactful sentences. Sentence 1 establishes the overarching dilemma, background, and scope. Sentence 2 delivers the definitive insight or strategic outcome.]

### 1. Foundation & Origins
- **[Origin & Context]**: [EXACTLY 2 to 3 concise sentences detailing the catalyst, early stakes, or foundational premise.]
- **[Core Framework]**: [EXACTLY 2 to 3 concise sentences outlining the underlying mechanism or governing philosophy.]

### 2. Critical Clashes & Strategic Developments
- **[Development 1]**: [EXACTLY 2 to 3 concise sentences explaining the tactical shift, friction point, or core argument.]
- **[Development 2]**: [EXACTLY 2 to 3 concise sentences explaining the tactical shift, friction point, or core argument.]
- **[The Turning Point]**: [EXACTLY 2 to 3 concise sentences identifying the watershed moment and its immediate consequence.]

### Table 1: Key Figures, Concepts & Roles
| Entity / Concept | Role / Description | Strategic Significance |
| :--- | :--- | :--- |
| [Entity 1] | [1-sentence concise role] | [Core influence] |
| [Entity 2] | [1-sentence concise role] | [Core influence] |
| [Entity 3] | [1-sentence concise role] | [Core influence] |
| [Entity 4] | [1-sentence concise role] | [Core influence] |

### 3. Key Themes & Structural Insights
- **[Theme 1]**: [EXACTLY 2 to 3 concise sentences analyzing the deeper systemic or conceptual pattern.]
- **[Theme 2]**: [EXACTLY 2 to 3 concise sentences analyzing the deeper systemic or conceptual pattern.]
- **[Theme 3]**: [EXACTLY 2 to 3 concise sentences analyzing the deeper systemic or conceptual pattern.]

### Chronological Progression Table
| Milestone / Phase | Concise Description |
| :--- | :--- |
| [Phase 1: Genesis] | [1-2 concise sentences summarizing initial conditions] |
| [Phase 2: Escalation] | [1-2 concise sentences summarizing central conflict/argument] |
| [Phase 3: Resolution] | [1-2 concise sentences summarizing final outcome] |

### Synthesized Conclusion
[EXACTLY 2 to 3 concise sentences synthesizing the enduring lesson, resolution, and real-world implications.]

IMPORTANT: Do not add conversational filler. Obey exact sentence length limits.

Transcript:
{transcript}
"""

SUMMARIZE_JSON_PROMPT = """
You are a high-speed, structured summarization engine. Analyze the transcript below and return ONLY a valid JSON object matching the schema below.
Follow these STRICT constraints:
- "overview": EXACTLY 2 impactful sentences. No introductory preamble.
- Each item in "key_moments": "explanation" must be EXACTLY 2 to 3 concise sentences. Eliminate filler words and repetition.
- "takeaways": Exactly 3 items, each 1 impactful sentence.

JSON Schema:
{{
  "title": "string",
  "overview": "string (EXACTLY 2 impactful sentences)",
  "key_moments": [
    {{
      "topic": "string",
      "timestamp": "string (optional or approximate)",
      "explanation": "string (EXACTLY 2 to 3 concise sentences)"
    }}
  ],
  "key_concepts": [
    {{
      "concept": "string",
      "definition": "string (1 concise sentence)",
      "significance": "string (1 concise sentence)"
    }}
  ],
  "takeaways": [
    "string",
    "string",
    "string"
  ]
}}

Transcript:
{transcript}
"""

GENERATE_QUIZ_PROMPT = """
Based on the following summary, generate {num_questions} multiple-choice questions.

You MUST return ONLY valid JSON. Do not include markdown code fences, commentary, or any text outside the JSON array.

Each question must be directly answerable from the provided summary text. Do not create questions about topics not covered in the summary.

Return a JSON array of objects with these exact keys:
- "question" (string)
- "options" (array of exactly 4 strings)
- "correct_answer" (string, must exactly match one of the options)
- "correct_index" (integer, 0-3, index of correct_answer in options)
- "explanation" (string, 1-2 brief sentences referencing the summary)
- "difficulty" (string: "easy", "medium", or "hard")
- "concept_tested" (string)

Summary:
{summary}
"""

SUMMARIZE_TEXT_PROMPT = """
Analyze the text below and produce a high-density, concise summary following these strict structural and length constraints:

# [Descriptive Title]

### Executive Overview
[Write EXACTLY 2 impactful sentences. Sentence 1 defines the core challenge or premise. Sentence 2 defines the primary breakthrough or conclusion.]

### Key Concepts & Breakdown
- **[Key Concept 1]**: [EXACTLY 2 to 3 concise sentences explaining this concept.]
- **[Key Concept 2]**: [EXACTLY 2 to 3 concise sentences explaining this concept.]
- **[Key Concept 3]**: [EXACTLY 2 to 3 concise sentences explaining this concept.]

### Table: Core Ideas & Significance
| Idea / Concept | Definition | Significance |
| :--- | :--- | :--- |
| [Idea 1] | [1-sentence concise definition] | [Core significance] |
| [Idea 2] | [1-sentence concise definition] | [Core significance] |

### Synthesized Conclusion
[EXACTLY 2 to 3 concise sentences summarizing the enduring takeaway.]

IMPORTANT: Obey sentence limits strictly (Overview = exactly 2 sentences; details = exactly 2 to 3 sentences). Eliminate all preamble.

Text:
{text}
"""
