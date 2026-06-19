-- Structured memory v2 reference schema for the OB1 bridge.
--
-- This file is a live Supabase-oriented scaffold. It keeps the new structured
-- surfaces first-class while preserving backward compatibility with the older
-- evidence / prepared_context / governed_state path through compatibility views.

create extension if not exists pgcrypto;

create table if not exists agent_memory_structured_core (
    id uuid primary key default gen_random_uuid(),
    user_id text not null,
    session_id text not null default '',
    surface_key text not null,
    compatibility_surface_key text not null,
    title text not null default '',
    body text not null default '',
    metadata jsonb not null default '{}'::jsonb,
    source_tool text not null default '',
    source_event text not null default '',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    embedding vector(1536)
);

create table if not exists agent_memory_north_star (
    core_id uuid primary key references agent_memory_structured_core(id) on delete cascade,
    user_id text not null,
    session_id text not null default '',
    goal_status text not null default 'active',
    priority integer not null default 0,
    horizon text not null default 'long'
);

create table if not exists agent_memory_active_projects (
    core_id uuid primary key references agent_memory_structured_core(id) on delete cascade,
    user_id text not null,
    session_id text not null default '',
    project_status text not null default 'active',
    owner text not null default '',
    next_step text not null default ''
);

create table if not exists agent_memory_decisions (
    core_id uuid primary key references agent_memory_structured_core(id) on delete cascade,
    user_id text not null,
    session_id text not null default '',
    decision_status text not null default 'recorded',
    decision_reason text not null default '',
    decision_owner text not null default ''
);

create table if not exists agent_memory_brags (
    core_id uuid primary key references agent_memory_structured_core(id) on delete cascade,
    user_id text not null,
    session_id text not null default '',
    impact_scope text not null default '',
    wins_score numeric not null default 0
);

create table if not exists agent_memory_thinking (
    core_id uuid primary key references agent_memory_structured_core(id) on delete cascade,
    user_id text not null,
    session_id text not null default '',
    thinking_mode text not null default 'note',
    open_question text not null default ''
);

create table if not exists agent_memory_session_events (
    id uuid primary key default gen_random_uuid(),
    user_id text not null,
    session_id text not null,
    event_type text not null,
    surface_key text not null default 'session_events',
    compatibility_surface_key text not null default 'evidence',
    body text not null default '',
    payload jsonb not null default '{}'::jsonb,
    source_tool text not null default '',
    created_at timestamptz not null default now()
);

create index if not exists agent_memory_structured_core_user_created_idx
    on agent_memory_structured_core (user_id, created_at desc);

create index if not exists agent_memory_structured_core_session_created_idx
    on agent_memory_structured_core (session_id, created_at desc);

create index if not exists agent_memory_structured_core_surface_created_idx
    on agent_memory_structured_core (surface_key, created_at desc);

create index if not exists agent_memory_session_events_user_created_idx
    on agent_memory_session_events (user_id, created_at desc);

create index if not exists agent_memory_session_events_session_created_idx
    on agent_memory_session_events (session_id, created_at desc);

alter table agent_memory_structured_core enable row level security;
alter table agent_memory_north_star enable row level security;
alter table agent_memory_active_projects enable row level security;
alter table agent_memory_decisions enable row level security;
alter table agent_memory_brags enable row level security;
alter table agent_memory_thinking enable row level security;
alter table agent_memory_session_events enable row level security;

drop policy if exists structured_core_isolation on agent_memory_structured_core;
create policy structured_core_isolation
    on agent_memory_structured_core
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

drop policy if exists north_star_isolation on agent_memory_north_star;
create policy north_star_isolation
    on agent_memory_north_star
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

drop policy if exists active_projects_isolation on agent_memory_active_projects;
create policy active_projects_isolation
    on agent_memory_active_projects
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

drop policy if exists decisions_isolation on agent_memory_decisions;
create policy decisions_isolation
    on agent_memory_decisions
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

drop policy if exists brags_isolation on agent_memory_brags;
create policy brags_isolation
    on agent_memory_brags
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

drop policy if exists thinking_isolation on agent_memory_thinking;
create policy thinking_isolation
    on agent_memory_thinking
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

drop policy if exists session_events_isolation on agent_memory_session_events;
create policy session_events_isolation
    on agent_memory_session_events
    for all
    using (user_id = current_setting('app.tenant_id', true))
    with check (user_id = current_setting('app.tenant_id', true));

create or replace view agent_memory_structured_feed as
    select
        c.id as core_id,
        c.user_id,
        c.session_id,
        c.surface_key,
        c.compatibility_surface_key,
        c.title,
        c.body,
        c.metadata,
        c.source_tool,
        c.source_event,
        c.created_at,
        c.updated_at,
        n.goal_status,
        n.priority,
        n.horizon,
        null::text as project_status,
        null::text as owner,
        null::text as next_step,
        null::text as decision_status,
        null::text as decision_reason,
        null::text as decision_owner,
        null::text as impact_scope,
        null::numeric as wins_score,
        null::text as thinking_mode,
        null::text as open_question,
        null::text as event_type,
        null::jsonb as payload
    from agent_memory_structured_core c
    join agent_memory_north_star n on n.core_id = c.id
    union all
    select
        c.id as core_id,
        c.user_id,
        c.session_id,
        c.surface_key,
        c.compatibility_surface_key,
        c.title,
        c.body,
        c.metadata,
        c.source_tool,
        c.source_event,
        c.created_at,
        c.updated_at,
        null::text as goal_status,
        null::integer as priority,
        null::text as horizon,
        p.project_status,
        p.owner,
        p.next_step,
        null::text as decision_status,
        null::text as decision_reason,
        null::text as decision_owner,
        null::text as impact_scope,
        null::numeric as wins_score,
        null::text as thinking_mode,
        null::text as open_question,
        null::text as event_type,
        null::jsonb as payload
    from agent_memory_structured_core c
    join agent_memory_active_projects p on p.core_id = c.id
    union all
    select
        c.id as core_id,
        c.user_id,
        c.session_id,
        c.surface_key,
        c.compatibility_surface_key,
        c.title,
        c.body,
        c.metadata,
        c.source_tool,
        c.source_event,
        c.created_at,
        c.updated_at,
        null::text as goal_status,
        null::integer as priority,
        null::text as horizon,
        null::text as project_status,
        null::text as owner,
        null::text as next_step,
        d.decision_status,
        d.decision_reason,
        d.decision_owner,
        null::text as impact_scope,
        null::numeric as wins_score,
        null::text as thinking_mode,
        null::text as open_question,
        null::text as event_type,
        null::jsonb as payload
    from agent_memory_structured_core c
    join agent_memory_decisions d on d.core_id = c.id
    union all
    select
        c.id as core_id,
        c.user_id,
        c.session_id,
        c.surface_key,
        c.compatibility_surface_key,
        c.title,
        c.body,
        c.metadata,
        c.source_tool,
        c.source_event,
        c.created_at,
        c.updated_at,
        null::text as goal_status,
        null::integer as priority,
        null::text as horizon,
        null::text as project_status,
        null::text as owner,
        null::text as next_step,
        null::text as decision_status,
        null::text as decision_reason,
        null::text as decision_owner,
        b.impact_scope,
        b.wins_score,
        null::text as thinking_mode,
        null::text as open_question,
        null::text as event_type,
        null::jsonb as payload
    from agent_memory_structured_core c
    join agent_memory_brags b on b.core_id = c.id
    union all
    select
        c.id as core_id,
        c.user_id,
        c.session_id,
        c.surface_key,
        c.compatibility_surface_key,
        c.title,
        c.body,
        c.metadata,
        c.source_tool,
        c.source_event,
        c.created_at,
        c.updated_at,
        null::text as goal_status,
        null::integer as priority,
        null::text as horizon,
        null::text as project_status,
        null::text as owner,
        null::text as next_step,
        null::text as decision_status,
        null::text as decision_reason,
        null::text as decision_owner,
        null::text as impact_scope,
        null::numeric as wins_score,
        t.thinking_mode,
        t.open_question,
        null::text as event_type,
        null::jsonb as payload
    from agent_memory_structured_core c
    join agent_memory_thinking t on t.core_id = c.id
    union all
    select
        null::uuid as core_id,
        e.user_id,
        e.session_id,
        e.surface_key,
        e.compatibility_surface_key,
        e.event_type as title,
        e.body,
        e.payload as metadata,
        e.source_tool,
        e.event_type as source_event,
        e.created_at,
        e.created_at as updated_at,
        null::text as goal_status,
        null::integer as priority,
        null::text as horizon,
        null::text as project_status,
        null::text as owner,
        null::text as next_step,
        null::text as decision_status,
        null::text as decision_reason,
        null::text as decision_owner,
        null::text as impact_scope,
        null::numeric as wins_score,
        null::text as thinking_mode,
        null::text as open_question,
        e.event_type,
        e.payload
    from agent_memory_session_events e;

create or replace view agent_memory_evidence_compat as
    select * from agent_memory_structured_feed where compatibility_surface_key = 'evidence';

create or replace view agent_memory_prepared_context_compat as
    select * from agent_memory_structured_feed where compatibility_surface_key = 'prepared_context';

create or replace view agent_memory_governed_state_compat as
    select * from agent_memory_structured_feed where compatibility_surface_key = 'governed_state';
