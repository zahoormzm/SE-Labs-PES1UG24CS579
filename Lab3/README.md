# Lab 3 — Component Modelling and Architectural Pattern Selection

**Mohammed Zahoor Mashahir | PES1UG24CS579 | Section J**

**Project:** Airport Lost Luggage Claim & Tracking Portal (Problem Statement 30)

## Scenario and requirements

The portal supports claim submission, luggage matching across airports,
chronological tracking, agent recovery, and approved compensation. Its design
addresses inconsistent or delayed scan feeds, duplicate payouts, and access
restricted to passengers and assigned agents.

The [Lab 1 requirements](../Lab1/Lab1_Requirements_Table.docx) define the
functional scope. Performance and availability targets are a timeline response
of at most 200 ms at p95 under 500 concurrent users, 99.9% monthly availability,
a recovery time of at most 15 minutes, and a recovery point of at most five
minutes. These are design targets, not measured results.

## Architecture selection

| Style | Benefits | Limitations |
| --- | --- | --- |
| Layered | Separates presentation, business rules, and data access; supports consistent transactions and short internal calls. | Modules share a deployment and cannot scale independently. |
| Microservices | Allows independent scaling, deployment, and fault isolation. | Adds distributed consistency, network latency, and operational complexity. |
| Client-server | Centralizes access control and storage for browser clients. | Does not define the internal separation of business responsibilities. |

The selected architecture is a layered modular monolith. It separates claim,
tracking, and compensation logic while retaining shared transactions. The
browser uses a client-server connection to the application.

## Component model

The UML diagram contains eight internal and two external components, with
11 provided/required interface pairs and component ports.

| Component | Responsibility |
| --- | --- |
| Passenger and Agent Portal | Claim forms, timelines, and agent work queue |
| Claim Workflow API | Authentication, authorization, validation, and request routing |
| Baggage Tracking | Scan ingestion, luggage matching, and chronological timelines |
| Recovery and Compensation | Recovery updates, eligibility, approval, and payout coordination |
| Claim and Scan Repository | Queries, transactions, audit records, and payout outbox |
| Baggage Feed Adapter | Scan normalization, deduplication, and retries |
| Payment Adapter | Provider requests, idempotency keys, and payout status |
| Portal Database | Persistent claims, scan history, and settlement records |
| Airport Scan Systems (external) | Airport scan logs |
| Compensation Provider (external) | Approved payouts and transaction status |

## Interfaces

Sockets indicate consumers, balls indicate providers, and solid assembly
connectors join matching interfaces. Requests follow the directions below;
responses return along the same connections.

| Interface | Consumer → provider | Protocol |
| --- | --- | --- |
| IClaimPortal | Portal → Claim Workflow API | HTTPS/JSON |
| ITracking | Claim Workflow API → Baggage Tracking | In-process API |
| IRecovery | Claim Workflow API → Recovery and Compensation | In-process API |
| IClaimStore | Claim Workflow API → Repository | Repository API |
| IScanStore | Baggage Tracking → Repository | Repository API |
| ISettlementStore | Recovery and Compensation → Repository | Repository API |
| IBaggageFeed | Baggage Tracking → Baggage Feed Adapter | In-process API |
| IPayment | Recovery and Compensation → Payment Adapter | In-process API |
| IAirportScanAPI | Baggage Feed Adapter → Airport Scan Systems | HTTPS/JSON |
| ISQL | Repository → Portal Database | SQL over TLS |
| ICompensationAPI | Payment Adapter → Compensation Provider | HTTPS/JSON |

External API contracts are proposed because the assignment does not specify
providers. Claims are validated and stored before matching. Background scan
ingestion maintains local history for timeline reads. Recovery changes require
agent authorization; payouts require approval and use an outbox with stable
idempotency keys. Uncertain payment outcomes require status reconciliation.

## Security and performance

The server checks passenger ownership and agent assignment. Validated inputs,
parameterized queries, HTTPS, and database TLS protect records and requests.
Background ingestion and indexed scan reads keep external calls off the normal
timeline path. Replicas, backups, and failover support the availability and
recovery targets; achieving these targets requires testing.

## Submission files

| File | Purpose |
| --- | --- |
| [Lab3_UML_Component_Diagram.pdf](Lab3_UML_Component_Diagram.pdf) | UML component diagram, A3 landscape |
| [Lab3_UML_Component_Diagram.png](Lab3_UML_Component_Diagram.png) | Diagram image |
| [Lab3_Architecture_Justification.docx](Lab3_Architecture_Justification.docx) | One-page architecture justification |
| [Lab3_Architecture_Justification.pdf](Lab3_Architecture_Justification.pdf) | Justification PDF |
| [Lab3_UML_Component_Diagram.drawio](Lab3_UML_Component_Diagram.drawio) | Editable diagrams.net source |
| [Lab3_UML_Component_Diagram.svg](Lab3_UML_Component_Diagram.svg) | Vector diagram |

Open the `.drawio` file in diagrams.net using **File → Open From → Device**.
