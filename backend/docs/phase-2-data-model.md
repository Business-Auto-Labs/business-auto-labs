# Phase 2"éÝyø§yÔ database and core models

These focused Mermaid ER diagrams cover the Phase 2 relational model. The palette follows the Business Automation Labs website: warm ivory paper, forest green table headers, restrained gold relationship lines, and the existing system sans-serif stack.

## 1. Organization, access, niches, and geography

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#f6f4ed","primaryColor":"#fffefa","primaryTextColor":"#1d2521","primaryBorderColor":"#214e3e","lineColor":"#796239","secondaryColor":"#ece9df","tertiaryColor":"#f6f4ed","fontFamily":"Aptos, Segoe UI, Arial, sans-serif"}}}%%
erDiagram
    ORGANIZATION ||--o{ USER : members
    ORGANIZATION ||--o{ TEAM : owns
    TEAM ||--o{ TEAM_MEMBER : includes
    USER ||--o{ TEAM_MEMBER : joins
    ORGANIZATION ||--o{ ORGANIZATION_NICHE : enables
    NICHE ||--o{ ORGANIZATION_NICHE : available_to
    COUNTRY ||--o{ REGION : contains
    REGION ||--o{ CITY : contains

    ORGANIZATION {
        int id PK
        string name
        string slug UK
        string timezone
        datetime created_at
        datetime updated_at
    }
    USER {
        int id PK
        int organization_id FK
        string email UK
        string role
    }
    TEAM {
        int id PK
        int organization_id FK
        string name
    }
    TEAM_MEMBER {
        int id PK
        int team_id FK
        int user_id FK
        string role
        boolean is_active
    }
    NICHE {
        int id PK
        string name UK
        string slug UK
    }
    ORGANIZATION_NICHE {
        int id PK
        int organization_id FK
        int niche_id FK
        boolean is_active
    }
    COUNTRY {
        int id PK
        string name UK
        string code UK
    }
    REGION {
        int id PK
        int country_id FK
        string name
        string region_type
    }
    CITY {
        int id PK
        int region_id FK
        string name
    }
```

## 2. Leads, multiple niches, contacts, and retained sources

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#f6f4ed","primaryColor":"#fffefa","primaryTextColor":"#1d2521","primaryBorderColor":"#214e3e","lineColor":"#796239","secondaryColor":"#ece9df","tertiaryColor":"#f6f4ed","fontFamily":"Aptos, Segoe UI, Arial, sans-serif"}}}%%
erDiagram
    ORGANIZATION ||--o{ LEAD : owns
    NICHE ||--o{ LEAD : primary_niche
    COUNTRY ||--o{ LEAD : located_in
    REGION o|--o{ LEAD : region
    CITY o|--o{ LEAD : city
    LEAD ||--o{ LEAD_NICHE : classified_as
    NICHE ||--o{ LEAD_NICHE : tags
    LEAD ||--o{ LEAD_CONTACT : has
    LEAD ||--o{ LEAD_SOURCE : discovered_through

    ORGANIZATION {
        int id PK
        string name
        string slug UK
    }
    LEAD {
        int id PK
        int organization_id FK
        string business_name
        string business_category
        int niche_id FK
        int country_id FK
        int region_id FK
        int city_id FK
        string address
        string website
        string public_phone
        string public_email
        string email_validation_status
        string original_source
        string original_source_url
        datetime discovered_at
        float qualification_score
        string crm_status
        string notes
        int assigned_to_user_id FK
        datetime created_at
        datetime updated_at
    }
    NICHE {
        int id PK
        string name UK
        string slug UK
    }
    COUNTRY {
        int id PK
        string name UK
        string code UK
    }
    REGION {
        int id PK
        int country_id FK
        string name
    }
    CITY {
        int id PK
        int region_id FK
        string name
    }
    LEAD_NICHE {
        int id PK
        int lead_id FK
        int niche_id FK
        boolean is_primary
        datetime added_at
    }
    LEAD_CONTACT {
        int id PK
        int lead_id FK
        string contact_type
        string value
        string normalized_value
        boolean is_primary
        boolean is_public
    }
    LEAD_SOURCE {
        int id PK
        int lead_id FK
        int data_source_id FK
        string source_url
        string normalized_url
        boolean is_original
        datetime discovered_at
    }
```

The original source URL stays on the lead and in source history. Additional niche selections add links; changing a selected niche is a filter operation and does not delete a lead.

## 3. Search configuration, discovery records, validation, and scores

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#f6f4ed","primaryColor":"#fffefa","primaryTextColor":"#1d2521","primaryBorderColor":"#214e3e","lineColor":"#796239","secondaryColor":"#ece9df","tertiaryColor":"#f6f4ed","fontFamily":"Aptos, Segoe UI, Arial, sans-serif"}}}%%
erDiagram
    ORGANIZATION ||--o{ SEARCH_CONFIGURATION : configures
    ORGANIZATION ||--o{ SCRAPING_JOB : scopes
    SEARCH_CONFIGURATION o|--o{ SCRAPING_JOB : records
    DATA_SOURCE ||--o{ SCRAPING_JOB : records
    DATA_SOURCE o|--o{ LEAD_SOURCE : catalogs
    LEAD ||--o{ LEAD_SOURCE : found_at
    LEAD ||--o{ LEAD_SCORE : scored
    LEAD ||--o{ LEAD_CONTACT : has
    LEAD_CONTACT ||--o{ EMAIL_VERIFICATION : validation_history

    ORGANIZATION {
        int id PK
        string name
    }
    SEARCH_CONFIGURATION {
        int id PK
        int organization_id FK
        int niche_id FK
        int country_id FK
        int region_id FK
        int city_id FK
        string query_text
        json options
        boolean is_active
    }
    SCRAPING_JOB {
        int id PK
        int organization_id FK
        int search_configuration_id FK
        int data_source_id FK
        string status
        datetime created_at
        datetime started_at
        datetime finished_at
    }
    DATA_SOURCE {
        int id PK
        string name UK
        string base_url
        string source_kind
    }
    LEAD {
        int id PK
        int organization_id FK
        string business_name
        string original_source_url
    }
    LEAD_SOURCE {
        int id PK
        int lead_id FK
        int data_source_id FK
        string source_url
        string normalized_url
        boolean is_original
    }
    LEAD_CONTACT {
        int id PK
        int lead_id FK
        string contact_type
        string normalized_value
        boolean is_public
    }
    EMAIL_VERIFICATION {
        int id PK
        int lead_contact_id FK
        string status
        string validation_method
        string result_details
        datetime verified_at
    }
    LEAD_SCORE {
        int id PK
        int lead_id FK
        float score
        string score_type
        json factors
        datetime created_at
    }
```

Search configurations and scraping jobs are metadata only in this phase. They do not invoke a scraper, external data provider, or paid API. Email validation rows record manual, syntax-only, or imported outcomes; no verification service is configured.

## 4. Assignments, team history, activity, status changes, and reminders

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#f6f4ed","primaryColor":"#fffefa","primaryTextColor":"#1d2521","primaryBorderColor":"#214e3e","lineColor":"#796239","secondaryColor":"#ece9df","tertiaryColor":"#f6f4ed","fontFamily":"Aptos, Segoe UI, Arial, sans-serif"}}}%%
erDiagram
    ORGANIZATION ||--o{ USER : members
    ORGANIZATION ||--o{ TEAM : owns
    TEAM ||--o{ TEAM_MEMBER : includes
    USER ||--o{ TEAM_MEMBER : joins
    LEAD ||--o{ LEAD_ASSIGNMENT : assignment_history
    USER ||--o{ LEAD_ASSIGNMENT : assigned_to
    TEAM o|--o{ LEAD_ASSIGNMENT : assigned_with
    LEAD ||--o{ CRM_ACTIVITY : activity_history
    USER ||--o{ CRM_ACTIVITY : performs
    LEAD ||--o{ LEAD_STATUS_HISTORY : status_history
    USER o|--o{ LEAD_STATUS_HISTORY : changes
    LEAD ||--o{ FOLLOW_UP_REMINDER : reminders
    USER ||--o{ FOLLOW_UP_REMINDER : owns

    ORGANIZATION {
        int id PK
        string name
        string slug UK
    }
    USER {
        int id PK
        int organization_id FK
        string email UK
        string role
    }
    TEAM {
        int id PK
        int organization_id FK
        string name
    }
    TEAM_MEMBER {
        int id PK
        int team_id FK
        int user_id FK
        string role
    }
    LEAD {
        int id PK
        int organization_id FK
        string business_name
        string crm_status
        int assigned_to_user_id FK
    }
    LEAD_ASSIGNMENT {
        int id PK
        int lead_id FK
        int user_id FK
        int team_id FK
        int assigned_by_user_id FK
        datetime assigned_at
        datetime ended_at
        boolean is_current
    }
    CRM_ACTIVITY {
        int id PK
        int lead_id FK
        int user_id FK
        string activity_type
        string details
        datetime timestamp
    }
    LEAD_STATUS_HISTORY {
        int id PK
        int lead_id FK
        int actor_user_id FK
        string from_status
        string to_status
        datetime changed_at
    }
    FOLLOW_UP_REMINDER {
        int id PK
        int lead_id FK
        int user_id FK
        datetime due_date
        boolean is_completed
        datetime completed_at
    }
```

The status helper writes the status and its history/activity record together in the caller's transaction. Assignments retain previous owners and mark one current assignment.

## 5. Campaign lists, drafts, suppression, and do-not-contact

```mermaid
%%{init: {"theme":"base","themeVariables":{"background":"#f6f4ed","primaryColor":"#fffefa","primaryTextColor":"#1d2521","primaryBorderColor":"#214e3e","lineColor":"#796239","secondaryColor":"#ece9df","tertiaryColor":"#f6f4ed","fontFamily":"Aptos, Segoe UI, Arial, sans-serif"}}}%%
erDiagram
    ORGANIZATION ||--o{ CAMPAIGN : owns
    CAMPAIGN ||--o{ CAMPAIGN_CONTACT : includes
    LEAD ||--o{ CAMPAIGN_CONTACT : listed_in
    CAMPAIGN ||--o{ CAMPAIGN_NICHE : targets
    NICHE ||--o{ CAMPAIGN_NICHE : selected
    CAMPAIGN o|--o{ EMAIL_DRAFT : stores
    LEAD o|--o{ EMAIL_DRAFT : contextualizes
    ORGANIZATION o|--o{ SUPPRESSION_RECORD : scopes
    ORGANIZATION o|--o{ DO_NOT_CONTACT : scopes
    LEAD o|--o{ DO_NOT_CONTACT : blocks

    ORGANIZATION {
        int id PK
        string name
        string slug UK
    }
    CAMPAIGN {
        int id PK
        int organization_id FK
        string name UK
        string status
        string niche_filter
    }
    CAMPAIGN_CONTACT {
        int id PK
        int campaign_id FK
        int lead_id FK
        string status
    }
    CAMPAIGN_NICHE {
        int id PK
        int campaign_id FK
        int niche_id FK
    }
    NICHE {
        int id PK
        string name UK
        string slug UK
    }
    LEAD {
        int id PK
        int organization_id FK
        string business_name
        string public_email
    }
    EMAIL_DRAFT {
        int id PK
        int campaign_id FK
        int lead_id FK
        int created_by_user_id FK
        string subject
        string body
        string status
    }
    SUPPRESSION_RECORD {
        int id PK
        int organization_id FK
        string value UK
        string normalized_value UK
        string suppression_type
        string reason
    }
    DO_NOT_CONTACT {
        int id PK
        int organization_id FK
        int lead_id FK
        int lead_contact_id FK
        string normalized_value
        string reason
        datetime created_at
    }
```

Email drafts are stored with status `draft`; there is no sender or send job in this phase. Suppression and do-not-contact records are data controls and do not connect to a mailing service.

## Data integrity notes

- New lead writes use an organization ID. Existing Phase 1 rows retain a nullable organization link until assigned to a real organization; migration does not invent one.
- A lead keeps a primary niche for compatibility and may link to multiple niches through `lead_niches`. Filtering does not delete or retag historical leads.
- The source URL on the lead preserves the first recorded source. `lead_sources` stores additional discovery URLs, normalized for duplicate detection.
- Duplicate matching is organization-scoped. It uses normalized business names, public contact values, website host, and geographic IDs; a partial unique index prevents duplicate fingerprints where organization mapping is known.
- Country, region, and city IDs have foreign keys. The write service checks that a region belongs to its country and a city belongs to its region.
- Timestamp defaults are UTC. Existing legacy timestamps are interpreted as UTC; ORM values round-trip as timezone-aware UTC.
- SQLite foreign keys are enabled for application connections. PostgreSQL is supported when a local server and its optional open-source driver are installed.
- There is no production seed data. The test suite creates clearly marked `.test` records only in temporary SQLite files.
