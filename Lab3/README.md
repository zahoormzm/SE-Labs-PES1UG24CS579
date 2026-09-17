# Lab 3 Component Modelling and Architectural Pattern Selection

**Mohammed Zahoor Mashahir · PES1UG24CS579 · Section J**  
Problem statement 30: Airport Lost Luggage Claim & Tracking Portal  
Domain: Smart Cities, Transport & Logistics  
Actors: Passenger and Baggage Service Agent

## Submission files

| File | Purpose |
| --- | --- |
| [Lab3_UML_Component_Diagram.pdf](Lab3_UML_Component_Diagram.pdf) | One-page vector UML component diagram, A3 landscape |
| [Lab3_UML_Component_Diagram.png](Lab3_UML_Component_Diagram.png) | High-resolution diagram image |
| [Lab3_Architecture_Justification.docx](Lab3_Architecture_Justification.docx) | Required one-page Word justification |
| [Lab3_Architecture_Justification.pdf](Lab3_Architecture_Justification.pdf) | PDF version of the same justification |
| [Lab3_UML_Component_Diagram.drawio](Lab3_UML_Component_Diagram.drawio) | Editable diagrams.net source |
| [Lab3_UML_Component_Diagram.svg](Lab3_UML_Component_Diagram.svg) | Scalable diagram source |

The `.drawio` source uses editable rectangles, text, ports and connector paths. Open it using **File → Open From → Device** in [diagrams.net](https://app.diagrams.net/). The PNG and PDF are ready for assessment. Print the diagram on A3 landscape for its intended label size.

Validation: the editable source was successfully imported and visually checked in diagrams.net. Both PDFs were rendered and reviewed; the justification is exactly one page. Structural checks confirm 10 components, 11 interface pairs and 22 component ports. The Word accessibility audit reported no findings.

## 1 Scenario review

The portal records lost-luggage claims, matches reports to scan logs from connected airports, displays a multi-leg timeline and supports agent recovery and compensation. Airport scan formats may differ, feeds may be delayed, and payout retries must not create duplicate payments. Passengers need a simple claim form and a clear chronological status view. Access to claim details must be restricted by ownership and agent assignment.

Requirements are carried forward from Lab 1; performance and availability figures below are **design and acceptance targets, not measured results**.

| Requirement | Design responsibility | Acceptance target or constraint |
| --- | --- | --- |
| FR-001 Luggage matching | Baggage Tracking, Baggage Feed Adapter, Repository | Match bag tag and itinerary to unrouted logs across all connected terminals; link a valid seeded match and expose a recovery alert within 5 s; reject invalid or incorrect matches. |
| FR-002 Claim submission | Portal, Claim Workflow API, Repository | Validate booking, bag tag, itinerary, contact, description and delivery address; accept optional images; return a unique claim ID within 3 s; prevent duplicate active claims for the same passenger and bag. |
| FR-003 Claim tracking | Workflow authorization, Baggage Tracking, Repository | Return the passenger's own status and complete chronological multi-leg scan history with airport, event and time. |
| FR-004 Agent recovery | Workflow authorization, Recovery and Compensation, Repository | Assigned agents search claims, add notes, update recovery/delivery and link recovered bags; audit agent and time; expose updates to the passenger within 5 s. |
| FR-005 Compensation | Recovery and Compensation, Payment Adapter, Repository | Apply configured delay/loss rules, calculate eligibility and amount, require agent approval, submit one logical payout and retain its transaction reference. |
| NFR-001 Timeline latency and access control | In-process tracking calls, indexed local scan reads, API access checks | p95 at most 200 ms across 10,000 authorized requests at 500 concurrent virtual users; unauthorized requests return 401/403 without claim data. |
| NFR-002 Availability and recovery | Proposed stateless application replicas, database failover, monitored backups | At least 99.9% monthly availability excluding scheduled maintenance; RTO at most 15 min; RPO at most 5 min. Verify through monitoring and restore/failover tests. |

## 2 Architectural style analysis

| Style | Scenario-specific benefits | Scenario-specific limitations | Decision |
| --- | --- | --- | --- |
| Layered | Keeps passenger screens separate from matching, compensation rules and data access. A shared relational store supports consistent claim, approval and audit updates. In-process calls keep the timeline path short. | Internal modules share a deployment and fault boundary; they cannot scale independently. Careless layer coupling makes changes harder, and extra indirection adds overhead. | Selected as a modular monolith with explicit interface contracts. |
| Microservices | Tracking could scale separately from compensation. Separate deployments could isolate feed-adapter faults and allow independent releases. | Claim and payout state would cross service boundaries; retries and consistency need more coordination. Network calls complicate the 200 ms timeline target and increase operational work. | Not selected for the current lab scope; reconsider if deployment autonomy or measured load demands it. |
| Client-server | Centralizes passenger and agent access, policy enforcement and data storage. Browser clients need no local claim database. | Describes the deployment interaction but does not sufficiently separate matching, recovery and integration logic. A single server would be a bottleneck and failure point. | Used as the browser-to-server deployment relationship, not the primary internal architecture. |

## 3 Component model

The diagram contains **8 internal components and 2 external components**, grouped by responsibility. The presentation layer accesses the business layer; business modules use repository or integration interfaces. Only the repository accesses the database. Adapters call external systems. The model does not depict ten independently deployed microservices.

| Component | Responsibility |
| --- | --- |
| Passenger and Agent Portal | Claim forms, optional-image input, passenger timeline, agent work queue and recovery-alert display. |
| Claim Workflow API | Authenticate sessions, authorize ownership/assignment, validate input, create claims and route tracking or recovery requests. |
| Baggage Tracking | Ingest normalized scans in the background, match tags and itineraries, persist matches/alerts and construct chronological timelines. |
| Recovery and Compensation | Maintain recovery and delivery state, apply configured compensation rules, validate approval and orchestrate payout dispatch/reconciliation. |
| Claim and Scan Repository | Encapsulate transactions and queries for claims, scan events, notes, approvals, audit entries and a durable payout outbox. |
| Baggage Feed Adapter | Fetch scans from connected airports, normalize data, reject malformed events, deduplicate and retry transient failures. |
| Payment Adapter | Translate approved payment commands to the provider API, preserve idempotency keys, and return payout status and references. |
| Portal Database | Persist relational records, attachment metadata/content where used, indexed scan history, unique constraints, audit entries and payout state. |
| Airport Scan Systems — external | Provide scan logs, including unrouted bags, from connected airports. |
| Compensation Provider — external | Execute approved payouts and expose transaction status. |

## 4 Interface contracts and directions

Each solid connection is a UML assembly connector. The **socket belongs to the consumer** and the **ball belongs to the provider**. Requests travel from consumer to provider; responses travel back. Squares show ports. These connections express usage dependencies without adding redundant dashed `<<use>>` arrows. The diagram has **11 named provided/required interface pairs**.

| Interface | Required by | Provided by | Protocol and exchanged data |
| --- | --- | --- | --- |
| IClaimPortal | Portal | Claim Workflow API | HTTPS/JSON with authenticated session; claim input, timeline queries and agent commands; returns claim ID, status/timeline, work queue or validation errors. Optional images use a validated upload operation. |
| ITracking | Claim Workflow API | Baggage Tracking | In-process API; authorized claim context, tag and itinerary; returns match result, recovery alert and ordered scan events. |
| IRecovery | Claim Workflow API | Recovery and Compensation | In-process API; authorized agent context, claim, recovery/delivery change or approval; returns updated state and payout result. |
| IClaimStore | Claim Workflow API | Repository | Repository API; create/read claims, ownership/assignment checks, filtered searches and duplicate checks; returns persisted records. |
| IScanStore | Baggage Tracking | Repository | Repository API; upsert deduplicated events, read tag/itinerary history, persist matched bag and recovery alert. |
| ISettlementStore | Recovery and Compensation | Repository | Repository API; atomically store local recovery/approval/audit changes, create/read payout outbox records, and save provider results. |
| IBaggageFeed | Baggage Tracking | Baggage Feed Adapter | In-process API; airport scope and ingestion cursor; returns normalized scan batches and source freshness/error status. |
| IPayment | Recovery and Compensation | Payment Adapter | In-process API; approved payout, amount and stable idempotency key; returns transaction reference or retry/reconciliation status. |
| IAirportScanAPI | Baggage Feed Adapter | Airport Scan Systems | Authenticated HTTPS/JSON; cursor-based scan queries across connected airports; returns raw scan logs and continuation cursor. |
| ISQL | Repository | Portal Database | Parameterized SQL over TLS; transactional writes, constraints and indexed queries. |
| ICompensationAPI | Payment Adapter | Compensation Provider | Authenticated HTTPS/JSON; payout submission and status query; returns provider transaction reference and outcome. |

External API shapes are proposed contracts: the problem statement does not specify vendors, schemas or provider guarantees. If a provider lacks idempotent submission or a reliable status query, automatic retries of an uncertain payout must stop for reconciliation.

## 5 Main interaction flows

1. **Submit and match:** Portal → IClaimPortal → Workflow. The API validates the session and mandatory data, then writes the claim through IClaimStore with a uniqueness constraint. It calls ITracking to match tag and itinerary against stored scan events. Tracking stores a valid match and recovery alert through IScanStore. The portal returns the claim ID and displays the resulting state.
2. **Ingest airport scans:** A background job within Baggage Tracking invokes IBaggageFeed. The adapter queries IAirportScanAPI for every configured airport, normalizes/deduplicates events and returns them. Tracking persists events through IScanStore and reevaluates relevant open claims. Persisted cursors, bounded retries and source-freshness indicators make interruptions visible. No external airport call is required for a normal timeline read.
3. **View timeline:** Portal → IClaimPortal → Workflow ownership check via IClaimStore → ITracking → IScanStore → ISQL. Tracking assembles the complete ordered timeline, which returns along the same path. Unauthorized requests stop before any claim data is returned.
4. **Update recovery:** An assigned agent submits a change through IClaimPortal. Workflow checks role and assignment, then calls IRecovery. Recovery stores the change and its audit entry in one local transaction through ISettlementStore. The passenger view refreshes through IClaimPortal; polling at a proposed interval of at most 2 s leaves processing time within the 5 s visibility target, subject to testing.
5. **Pay compensation:** Recovery evaluates configured eligibility and amount, then requires agent approval. It transactionally records approval, audit and one payout outbox entry through ISettlementStore. Its background dispatcher reads pending entries and calls IPayment with a stable idempotency key. The adapter invokes ICompensationAPI. Recovery saves the reference/result through ISettlementStore. Timeouts trigger a status query or a safe retry, never a new logical payout. The external payment is not part of the local database transaction.

## 6 Security and performance decisions

Authentication and authorization run at the server boundary, not merely in browser controls. Every passenger request checks claim ownership; every agent mutation checks role and assignment. Internal business functions receive the authorized context and validate valid state transitions and approval prerequisites. Inputs and attachments require validation; secrets remain on the server; external API calls use HTTPS and database traffic uses TLS. Repository queries are parameterized, and logs must not expose contact details or credentials.

The timeline read model uses an index on bag tag and event time with itinerary filtering and stable event ordering. Background ingestion maintains this local history. Reads must expose stale-source information rather than imply that an unavailable airport feed is current. The 5 s seeded matching target is tested with available scan data; real feed propagation requires an airport integration agreement. The 200 ms p95 target must be load-tested end to end. Proposed replicas, health checks, replicated storage and tested backups address availability; deployment topology is outside this logical component diagram.

## 7 Handout checklist

- [x] Review the assigned airport scenario, functional/non-functional requirements and challenges.
- [x] Compare Layered, Microservices and Client-Server styles.
- [x] Select and justify the architecture using scenario-specific reasoning.
- [x] Show at least 5 components: 8 internal plus 2 external.
- [x] Show at least 4 interfaces: 11 provided/required pairs.
- [x] Use component stereotypes, ball/socket notation, ports and solid assembly connectors.
- [x] Label protocols and explain request/response direction and data interactions.
- [x] Provide PNG and PDF diagram exports and an editable source.
- [x] Provide a one-page Word justification with the choice, two reasons, security advantage and performance benefit.
- [x] Include the same justification as PDF.
- [x] Place the submission in `Lab3` under `SE-Labs-PES1UG24CS579`.

The coffee-kiosk, Order Manager and payment example in the handout illustrates notation; this submission models the assigned airport portal.

## Sources

- `Lab_3_Architecture_Student_handout.pdf`: required deliverables, UML notation and architectural styles.
- `30_SE_Lab1_SE_Problem_Statements.pdf`: assigned project scope, actors, cross-airport matching and timeline latency.
- [Lab 1 requirements table](../Lab1/Lab1_Requirements_Table.docx): requirement identifiers and acceptance targets carried forward.
