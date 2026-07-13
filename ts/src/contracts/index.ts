import type { InstanceManifest } from "../models/index.js";

// Console → Platform commands

export const CommandKind = {
  SetLlmProvider: "set_llm_provider",
  RotateSecret: "rotate_secret",
  InstallArea: "install_area",
  UninstallArea: "uninstall_area",
  DeployAgent: "deploy_agent",
  UpdateCeiling: "update_ceiling",
  KillSwitchAgent: "kill_switch_agent",
  CreateSpace: "create_space",
  DeleteSpace: "delete_space",
  GrantCrossInstanceAccess: "grant_cross_instance_access",
  UpgradePlatform: "upgrade_platform",
  Pause: "pause",
  Resume: "resume",
} as const;
export type CommandKind = (typeof CommandKind)[keyof typeof CommandKind];

export interface Command {
  kind: CommandKind;
  payload: Record<string, unknown>;
}

export interface CommandEnvelope {
  cmd_id: string;
  instance_id: string;
  issued_at: number;
  expires_at: number;
  command: Command;
}

export type CommandStatus =
  | "queued" | "in_progress" | "applied" | "failed" | "rejected";

export interface CommandResult {
  cmd_id: string;
  status: CommandStatus;
  detail: string | null;
  applied_at: number | null;
  error_code: string | null;
}

// Platform → Console notifications

export const NotificationKind = {
  HealthHeartbeat: "health_heartbeat",
  StatusChanged: "status_changed",
  AgentTriggeredKillSwitch: "agent_triggered_kill_switch",
  BudgetAlert: "budget_alert",
  AuditEvent: "audit_event",
  Error: "error",
} as const;
export type NotificationKind = (typeof NotificationKind)[keyof typeof NotificationKind];

export interface Notification {
  kind: NotificationKind;
  payload: Record<string, unknown>;
}

export interface NotificationEnvelope {
  notif_id: string;
  instance_id: string;
  emitted_at: number;
  notification: Notification;
}

// Bootstrap

export type BootstrapStatus =
  | "ok" | "already_bootstrapped" | "invalid_token" | "apply_failed";

export interface BootstrapRequest {
  instance_id: string;
  console_public_key_pem: string;
  console_webhook_url: string;
  manifest: InstanceManifest;
}

export interface BootstrapResponse {
  status: BootstrapStatus;
  platform_public_key_pem: string | null;
  platform_version: string | null;
  applied_areas: string[];
  error_detail: string | null;
}
