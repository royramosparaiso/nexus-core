import { describe, it, expect } from "vitest";
import { AVAILABLE_AREAS, type InstanceManifest } from "../src/models/index.js";
import { CommandKind } from "../src/contracts/index.js";

describe("shared models", () => {
  it("exposes 10 available areas (4 core + 6 vertical)", () => {
    expect(AVAILABLE_AREAS).toHaveLength(10);
    expect(AVAILABLE_AREAS.filter((a) => a.tier === "core")).toHaveLength(4);
    expect(AVAILABLE_AREAS.filter((a) => a.tier === "vertical")).toHaveLength(6);
  });

  it("all default-true areas are core-tier", () => {
    const defaults = AVAILABLE_AREAS.filter((a) => a.default);
    expect(defaults.every((a) => a.tier === "core")).toBe(true);
  });

  it("InstanceManifest is structurally satisfiable", () => {
    const m: InstanceManifest = {
      apiVersion: "nexus.v0.6",
      kind: "Instance",
      name: "test",
      persona: { display_name: "T", kind: "personal", description: "", default_locale: "es-ES" },
      deployment: { modality: "local", domain: null, region: null, tls: true, autoscale: false },
      llms: {
        enabled_providers: ["ollama"],
        roles: {
          planner: "llama3.1:70b", coordinator: "llama3.1:8b",
          worker: "llama3.1:8b", embeddings: "nomic-embed-text",
        },
        allow_fallback: true,
        monthly_budget_usd: 0,
      },
      memory: {
        driver: "sqlite", graph: "none",
        retention_days: 365, encryption_at_rest: true,
      },
      areas: { enabled: ["personal_organization"] },
      governance: {
        default_autonomy: "act_with_approval", kill_switch_enabled: true,
        audit_retention_days: 730, monthly_budget_alert_pct: 80,
        require_2fa_for_superadmin: true,
      },
    };
    expect(m.name).toBe("test");
  });
});

describe("command contracts", () => {
  it("CommandKind values match Python string enum", () => {
    expect(CommandKind.CreateSpace).toBe("create_space");
    expect(CommandKind.KillSwitchAgent).toBe("kill_switch_agent");
    expect(CommandKind.UpgradePlatform).toBe("upgrade_platform");
  });
});
