type StructuredSurface =
  | "north_star"
  | "active_projects"
  | "decisions"
  | "brags"
  | "thinking"
  | "session_events";

type ToolName =
  | "start_session"
  | "standup"
  | "capture"
  | "capture_decision"
  | "capture_brag"
  | "wrap_up"
  | "get_briefing"
  | "session_start"
  | "prompt_submit"
  | "post_tool_use"
  | "session_end";

type ToolRequest = {
  tool: ToolName;
  user_id: string;
  session_id?: string;
  fork_id?: string;
  channel?: string;
  text?: string;
  title?: string;
  surface_hint?: string;
  metadata?: Record<string, unknown>;
  payload?: Record<string, unknown>;
  compact?: boolean;
  include_session_events?: boolean;
};

const STRUCTURED_SURFACES: StructuredSurface[] = [
  "north_star",
  "active_projects",
  "decisions",
  "brags",
  "thinking",
  "session_events",
];

const SURFACE_ALIASES: Record<string, StructuredSurface> = {
  governed_state: "decisions",
  prepared_context: "thinking",
  evidence: "thinking",
  goal: "north_star",
  goals: "north_star",
  "north star": "north_star",
  north_star: "north_star",
  objective: "north_star",
  objectives: "north_star",
  project: "active_projects",
  projects: "active_projects",
  initiative: "active_projects",
  initiatives: "active_projects",
  decision: "decisions",
  decisions: "decisions",
  brag: "brags",
  brags: "brags",
  thinking: "thinking",
  thought: "thinking",
  notes: "thinking",
  note: "thinking",
};

const SURFACE_LEGACY: Record<StructuredSurface, "evidence" | "prepared_context" | "governed_state"> = {
  north_star: "governed_state",
  active_projects: "governed_state",
  decisions: "governed_state",
  brags: "prepared_context",
  thinking: "prepared_context",
  session_events: "evidence",
};

const SURFACE_KEYWORDS: Record<Exclude<StructuredSurface, "session_events">, string[]> = {
  north_star: ["north star", "goal", "goals", "objective", "objectives", "mission", "vision", "priority"],
  active_projects: ["project", "projects", "initiative", "initiatives", "roadmap", "blocker", "working on"],
  decisions: ["decision", "decided", "chose", "tradeoff", "resolved", "we will", "we'll"],
  brags: ["brag", "success", "successful", "shipped", "delivered", "accomplished", "win", "wins"],
  thinking: ["thinking", "thought", "note", "idea", "maybe", "consider", "reflection"],
};

const TABLE_BY_SURFACE: Record<StructuredSurface, string> = {
  north_star: "agent_memory_north_star",
  active_projects: "agent_memory_active_projects",
  decisions: "agent_memory_decisions",
  brags: "agent_memory_brags",
  thinking: "agent_memory_thinking",
  session_events: "agent_memory_session_events",
};

const TITLE_BY_SURFACE: Record<StructuredSurface, string> = {
  north_star: "North Star",
  active_projects: "Active Projects",
  decisions: "Decisions",
  brags: "Brags",
  thinking: "Thinking",
  session_events: "Session Events",
};

const EVENT_TYPES = new Set<ToolName>([
  "start_session",
  "session_start",
  "prompt_submit",
  "post_tool_use",
  "wrap_up",
  "session_end",
]);

function getSupabaseConfig(): { url: string; key: string } {
  const url = Deno.env.get("SUPABASE_URL") ?? "";
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY") ?? "";
  return { url, key };
}

function normalizeSurfaceHint(value?: string | null): StructuredSurface | null {
  if (!value) return null;
  const token = value.trim().toLowerCase().replace(/-/g, "_");
  return SURFACE_ALIASES[token] ?? (STRUCTURED_SURFACES.includes(token as StructuredSurface) ? (token as StructuredSurface) : null);
}

function legacySurfaceFor(surface: StructuredSurface): "evidence" | "prepared_context" | "governed_state" {
  return SURFACE_LEGACY[surface];
}

function routeSurface(text: string, surfaceHint?: string | null): { surfaceKey: StructuredSurface; legacySurfaceKey: "evidence" | "prepared_context" | "governed_state"; reason: string } {
  const explicit = normalizeSurfaceHint(surfaceHint);
  if (explicit) {
    return { surfaceKey: explicit, legacySurfaceKey: legacySurfaceFor(explicit), reason: "explicit surface hint" };
  }
  const lowered = text.toLowerCase();
  let winner: StructuredSurface = "thinking";
  let score = 0;
  for (const surface of STRUCTURED_SURFACES) {
    if (surface === "session_events") continue;
    const hits = SURFACE_KEYWORDS[surface].reduce((count, keyword) => count + (lowered.includes(keyword) ? 1 : 0), 0);
    if (hits > score) {
      score = hits;
      winner = surface;
    }
  }
  if (score > 0) {
    return { surfaceKey: winner, legacySurfaceKey: legacySurfaceFor(winner), reason: `heuristic keyword match (${score})` };
  }
  return { surfaceKey: "thinking", legacySurfaceKey: legacySurfaceFor("thinking"), reason: "default fallback to thinking" };
}

function suggestTitle(text: string, fallback = "Untitled entry"): string {
  const clean = text.replace(/\s+/g, " ").trim();
  if (!clean) return fallback;
  const separators = [". ", " — ", " - ", ": "];
  for (const separator of separators) {
    if (clean.includes(separator)) {
      const candidate = clean.split(separator, 1)[0].trim();
      if (candidate) return candidate.slice(0, 90);
    }
  }
  return clean.slice(0, 90);
}

async function supabaseRequest(path: string, init: RequestInit, config = getSupabaseConfig()): Promise<Response> {
  if (!config.url || !config.key) {
    throw new Error("Supabase is not configured: set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY");
  }
  const headers = new Headers(init.headers);
  headers.set("apikey", config.key);
  headers.set("Authorization", `Bearer ${config.key}`);
  headers.set("Content-Type", "application/json");
  return fetch(`${config.url}${path}`, { ...init, headers });
}

async function insertJson(table: string, row: Record<string, unknown>): Promise<Record<string, unknown>> {
  const response = await supabaseRequest(`/rest/v1/${table}`, {
    method: "POST",
    headers: { Prefer: "return=representation" },
    body: JSON.stringify(row),
  });
  if (!response.ok) {
    throw new Error(`insert into ${table} failed: ${response.status} ${await response.text()}`);
  }
  const data = await response.json();
  return Array.isArray(data) ? (data[0] ?? {}) : data;
}

async function selectJson(table: string, params: string): Promise<Record<string, unknown>[]> {
  const response = await supabaseRequest(`/rest/v1/${table}?${params}`, { method: "GET" });
  if (!response.ok) {
    throw new Error(`select from ${table} failed: ${response.status} ${await response.text()}`);
  }
  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

function buildCoreRow(request: ToolRequest, surfaceKey: StructuredSurface, body: string, title?: string) {
  return {
    user_id: request.user_id,
    session_id: request.session_id ?? "",
    surface_key: surfaceKey,
    compatibility_surface_key: legacySurfaceFor(surfaceKey),
    title: (title ?? "").trim() || suggestTitle(body),
    body,
    metadata: request.metadata ?? {},
    source_tool: request.tool,
    source_event: request.tool,
  };
}

function buildSessionEventRow(request: ToolRequest, eventType: string, body: string) {
  const legacySurfaceKey = eventType === "prompt_submit" || eventType === "post_tool_use" ? "prepared_context" : "evidence";
  return {
    user_id: request.user_id,
    session_id: request.session_id ?? "",
    event_type: eventType,
    surface_key: "session_events",
    compatibility_surface_key: legacySurfaceKey,
    body,
    payload: request.payload ?? {},
    source_tool: request.tool,
  };
}

async function writeStructuredEntry(request: ToolRequest, surfaceKey: StructuredSurface, body: string, title?: string) {
  const core = await insertJson("agent_memory_structured_core", buildCoreRow(request, surfaceKey, body, title));
  const coreId = core.id as string;
  const shared = {
    core_id: coreId,
    user_id: request.user_id,
    session_id: request.session_id ?? "",
  };
  let surfaceRow: Record<string, unknown> = {};
  switch (surfaceKey) {
    case "north_star":
      surfaceRow = { ...shared, goal_status: "active", priority: 0, horizon: "long" };
      break;
    case "active_projects":
      surfaceRow = { ...shared, project_status: "active", owner: "", next_step: "" };
      break;
    case "decisions":
      surfaceRow = { ...shared, decision_status: "recorded", decision_reason: "", decision_owner: "" };
      break;
    case "brags":
      surfaceRow = { ...shared, impact_scope: "", wins_score: 0 };
      break;
    case "thinking":
      surfaceRow = { ...shared, thinking_mode: "note", open_question: "" };
      break;
    case "session_events":
      throw new Error("use writeSessionEvent for session_events");
  }
  const surface = await insertJson(TABLE_BY_SURFACE[surfaceKey], surfaceRow);
  return { core, surface, surface_key: surfaceKey, legacy_surface_key: legacySurfaceFor(surfaceKey) };
}

async function writeSessionEvent(request: ToolRequest, eventType: string, body: string) {
  const row = buildSessionEventRow(request, eventType, body);
  const core = await insertJson("agent_memory_structured_core", {
    user_id: request.user_id,
    session_id: request.session_id ?? "",
    surface_key: "session_events",
    compatibility_surface_key: row.compatibility_surface_key,
    title: eventType.replace(/_/g, " "),
    body,
    metadata: request.payload ?? {},
    source_tool: request.tool,
    source_event: eventType,
  });
  const event = await insertJson(TABLE_BY_SURFACE.session_events, {
    user_id: request.user_id,
    session_id: request.session_id ?? "",
    event_type: eventType,
    surface_key: "session_events",
    compatibility_surface_key: row.compatibility_surface_key,
    body,
    payload: request.payload ?? {},
    source_tool: request.tool,
  });
  return { core, event, surface_key: "session_events", legacy_surface_key: row.compatibility_surface_key };
}

function formatBullets(items: Record<string, unknown>[]): string[] {
  const bullets: string[] = [];
  for (const item of items) {
    const title = String(item.title ?? "").trim();
    const body = String(item.body ?? "").trim();
    if (title && body && title.toLowerCase() !== body.toLowerCase()) {
      bullets.push(`- ${title} — ${body}`);
    } else if (body || title) {
      bullets.push(`- ${body || title}`);
    }
  }
  return bullets;
}

function buildBriefingMarkdown(rows: Record<string, unknown>[], request: ToolRequest, title: string): string {
  const bySurface = new Map<string, Record<string, unknown>[]>();
  for (const row of rows) {
    const surface = String(row.surface_key ?? "thinking");
    const list = bySurface.get(surface) ?? [];
    list.push(row);
    bySurface.set(surface, list);
  }

  const lines: string[] = [`# ${title}`, ""];
  if (request.session_id) {
    lines.push("## Session");
    lines.push(`- session_id: ${request.session_id}`);
    if (request.fork_id) lines.push(`- fork_id: ${request.fork_id}`);
    if (request.channel) lines.push(`- channel: ${request.channel}`);
    lines.push("");
  }

  for (const surface of STRUCTURED_SURFACES) {
    const items = bySurface.get(surface) ?? [];
    if (!items.length) continue;
    lines.push(`## ${TITLE_BY_SURFACE[surface]}`);
    lines.push(...formatBullets(items));
    lines.push("");
  }

  lines.push("## Compatibility Map");
  lines.push("- north_star / active_projects / decisions -> governed_state");
  lines.push("- brags / thinking -> prepared_context");
  lines.push("- session_events -> evidence");
  lines.push("");
  lines.push("## Next Step");
  lines.push("- Use this as the live briefing surface for the next session.");
  lines.push("");
  return lines.join("\n");
}

async function buildBriefing(request: ToolRequest, title: string) {
  const rows = await selectJson(
    "agent_memory_structured_feed",
    [
      `user_id=eq.${encodeURIComponent(request.user_id)}`,
      request.session_id ? `session_id=eq.${encodeURIComponent(request.session_id)}` : "",
      "order=created_at.desc",
      "limit=100",
    ]
      .filter(Boolean)
      .join("&"),
  );
  return { markdown: buildBriefingMarkdown(rows, request, title), rows };
}

function sessionIdOrDefault(request: ToolRequest): string {
  return request.session_id ?? `SES-${new Date().toISOString().replace(/[-:TZ.]/g, "").slice(0, 14)}`;
}

async function handleCapture(request: ToolRequest) {
  const body = (request.text ?? "").trim();
  const route = routeSurface(body, request.surface_hint);
  const result = await writeStructuredEntry(
    { ...request, session_id: sessionIdOrDefault(request) },
    route.surfaceKey,
    body,
    request.title,
  );
  return { ...result, route };
}

async function handleDecision(request: ToolRequest) {
  const body = (request.text ?? "").trim();
  return writeStructuredEntry({ ...request, session_id: sessionIdOrDefault(request) }, "decisions", body, request.title);
}

async function handleBrag(request: ToolRequest) {
  const body = (request.text ?? "").trim();
  return writeStructuredEntry({ ...request, session_id: sessionIdOrDefault(request) }, "brags", body, request.title);
}

async function handleSessionStart(request: ToolRequest) {
  const event = await writeSessionEvent(
    { ...request, session_id: sessionIdOrDefault(request), tool: "session_start" },
    "session_start",
    request.text?.trim() || "Session started",
  );
  return event;
}

async function handlePromptSubmit(request: ToolRequest) {
  return writeSessionEvent(
    { ...request, session_id: sessionIdOrDefault(request), tool: "prompt_submit" },
    "prompt_submit",
    request.text?.trim() || "Prompt submitted",
  );
}

async function handlePostToolUse(request: ToolRequest) {
  return writeSessionEvent(
    { ...request, session_id: sessionIdOrDefault(request), tool: "post_tool_use" },
    "post_tool_use",
    request.text?.trim() || "Tool used",
  );
}

async function handleWrapUp(request: ToolRequest) {
  return writeSessionEvent(
    { ...request, session_id: sessionIdOrDefault(request), tool: "wrap_up" },
    "wrap_up",
    request.text?.trim() || "Session wrapped up",
  );
}

async function handleGetBriefing(request: ToolRequest) {
  return buildBriefing(request, request.compact ? "Standup" : "Briefing");
}

async function handleRequest(request: ToolRequest) {
  switch (request.tool) {
    case "capture":
      return handleCapture(request);
    case "capture_decision":
      return handleDecision(request);
    case "capture_brag":
      return handleBrag(request);
    case "start_session":
    case "session_start":
      return handleSessionStart(request);
    case "prompt_submit":
      return handlePromptSubmit(request);
    case "post_tool_use":
      return handlePostToolUse(request);
    case "wrap_up":
    case "session_end":
      return handleWrapUp(request);
    case "standup":
      return handleGetBriefing({ ...request, compact: true });
    case "get_briefing":
      return handleGetBriefing(request);
    default:
      throw new Error(`unsupported tool: ${request.tool}`);
  }
}

Deno.serve(async (req) => {
  try {
    if (req.method !== "POST") {
      return Response.json({ ok: false, error: "POST only" }, { status: 405 });
    }
    const request = (await req.json()) as ToolRequest;
    if (!request || !request.tool || !request.user_id) {
      return Response.json({ ok: false, error: "missing tool or user_id" }, { status: 400 });
    }
    const result = await handleRequest(request);
    return Response.json({ ok: true, tool: request.tool, result });
  } catch (error) {
    return Response.json(
      {
        ok: false,
        error: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
});
