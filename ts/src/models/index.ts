// Mirrors python/nexus_core/models. Kept string-literal-typed to avoid
// a runtime code generator; contract tests verify parity.

export type PersonaKind =
  | "personal" | "family" | "company" | "community" | "client" | "custom";

export interface PersonaConfig {
  display_name: string;
  kind: PersonaKind;
  description: string;
  default_locale: string;
}

export type Modality = "local" | "fly" | "k8s" | "onprem" | "saas";

export interface DeploymentConfig {
  modality: Modality;
  domain: string | null;
  region: string | null;
  tls: boolean;
  autoscale: boolean;
}

export type LlmProvider =
  | "anthropic" | "openai" | "openrouter" | "perplexity"
  | "groq" | "together" | "mistral" | "ollama";

export interface LlmRoleAssignment {
  planner: string;
  coordinator: string;
  worker: string;
  embeddings: string;
}

export interface LlmConfig {
  enabled_providers: LlmProvider[];
  roles: LlmRoleAssignment;
  allow_fallback: boolean;
  monthly_budget_usd: number;
}

export type MemoryDriver = "sqlite" | "postgres" | "postgres_pgvector";
export type GraphDriver = "none" | "neo4j" | "postgres_graph";

export interface MemoryConfig {
  driver: MemoryDriver;
  graph: GraphDriver;
  retention_days: number;
  encryption_at_rest: boolean;
}

export type AreaTier = "core" | "vertical";

export interface Area {
  slug: string;
  label: string;
  tier: AreaTier;
  default: boolean;
}

export const AVAILABLE_AREAS: Area[] = [
  { slug: "personal_organization", label: "Personal organization", tier: "core", default: true },
  { slug: "meetings", label: "Meetings & action items", tier: "core", default: true },
  { slug: "finance_personal", label: "Personal finance", tier: "core", default: true },
  { slug: "comms", label: "Communications", tier: "core", default: true },
  { slug: "brand", label: "Brand & marketing", tier: "vertical", default: false },
  { slug: "sales", label: "Sales & pipeline", tier: "vertical", default: false },
  { slug: "product", label: "Product & roadmap", tier: "vertical", default: false },
  { slug: "dev", label: "Dev (agent factory local)", tier: "vertical", default: false },
  { slug: "legal", label: "Legal & compliance", tier: "vertical", default: false },
  { slug: "operations", label: "Operations", tier: "vertical", default: false },
];

export interface AreasConfig {
  enabled: string[];
}

export type AutonomyLevel =
  | "read_only" | "propose" | "act_with_approval" | "act_autonomously";

export interface GovernanceConfig {
  default_autonomy: AutonomyLevel;
  kill_switch_enabled: boolean;
  audit_retention_days: number;
  monthly_budget_alert_pct: number;
  require_2fa_for_superadmin: boolean;
}

export type InstanceStatus =
  | "bootstrap-pending" | "bootstrapping" | "running"
  | "degraded" | "paused" | "error";

export interface InstanceManifest {
  apiVersion: "nexus.v0.6";
  kind: "Instance";
  name: string;
  persona: PersonaConfig;
  deployment: DeploymentConfig;
  llms: LlmConfig;
  memory: MemoryConfig;
  areas: AreasConfig;
  governance: GovernanceConfig;
}

export type SpaceKind =
  | "internal" | "company" | "client" | "community" | "group" | "family" | "ad_hoc";

export interface SpaceRef {
  space_id: string;
  instance_id: string;
  name: string;
  kind: SpaceKind;
}
