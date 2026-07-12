// Generated from schemas; do not edit manually.
export const AgentProposalType = [
  "TASK_CLASSIFICATION",
  "TASK_ASSIGNMENT",
  "PROJECT_STATUS",
  "RESTOCK",
  "EXECUTION_ACTION",
  "RISK_ASSESSMENT",
  "OTHER",
] as const;
export type AgentProposalType = typeof AgentProposalType[number];

export const ApprovalType = [
  "CONTROLLED_TASK",
  "CHANGE_DUE_AT",
  "PROJECT_COMPLETE",
  "PROJECT_CANCEL",
  "INVENTORY_ADJUSTMENT",
  "EXECUTION_SIDE_EFFECT",
  "OTHER",
] as const;
export type ApprovalType = typeof ApprovalType[number];

export const ApprovalStatus = [
  "PENDING",
  "APPROVED",
  "REJECTED",
  "CANCELLED",
  "EXPIRED",
] as const;
export type ApprovalStatus = typeof ApprovalStatus[number];

export const AuditResult = [
  "SUCCEEDED",
  "DENIED",
  "FAILED",
  "NO_OP",
] as const;
export type AuditResult = typeof AuditResult[number];

export const ProjectStatus = [
  "PROPOSED",
  "PLANNING",
  "ACTIVE",
  "PAUSED",
  "COMPLETED",
  "CANCELLED",
] as const;
export type ProjectStatus = typeof ProjectStatus[number];

export const ProjectPriority = [
  "LOW",
  "NORMAL",
  "HIGH",
  "URGENT",
] as const;
export type ProjectPriority = typeof ProjectPriority[number];

export const ActorType = [
  "HUMAN",
  "AGENT",
  "SERVICE",
] as const;
export type ActorType = typeof ActorType[number];

export const SourceType = [
  "CHAT_MESSAGE",
  "EXTERNAL_PLATFORM",
  "LOCAL_API",
  "SCHEDULE",
  "APPROVED_EXECUTOR",
  "MANUAL",
  "IMPORT",
] as const;
export type SourceType = typeof SourceType[number];

export const RiskLevel = [
  "LOW",
  "MEDIUM",
  "HIGH",
  "CRITICAL",
] as const;
export type RiskLevel = typeof RiskLevel[number];

export const EvidenceType = [
  "PHOTO",
  "VIDEO",
  "TEXT",
  "FILE",
  "MEASUREMENT",
  "MANAGER_CONFIRMATION",
] as const;
export type EvidenceType = typeof EvidenceType[number];

export const CommonMediaType = [
  "PHOTO",
  "VIDEO",
  "FILE",
  "AUDIO",
] as const;
export type CommonMediaType = typeof CommonMediaType[number];

export const EmployeeRole = [
  "OWNER",
  "MANAGER",
  "TEAM_LEADER",
  "WORKER",
  "OBSERVER",
] as const;
export type EmployeeRole = typeof EmployeeRole[number];

export const InventoryTransactionType = [
  "PURCHASE_IN",
  "RETURN_IN",
  "USE_OUT",
  "ADJUST_IN",
  "ADJUST_OUT",
  "TRANSFER",
  "DAMAGE_OUT",
  "EXPIRED_OUT",
  "RESERVE",
  "RELEASE",
] as const;
export type InventoryTransactionType = typeof InventoryTransactionType[number];

export const ProjectUpdateType = [
  "PROGRESS",
  "RISK",
  "BLOCKER",
  "NEXT_ACTION",
  "STATUS_SUGGESTION",
  "COMMENT",
  "CORRECTION",
] as const;
export type ProjectUpdateType = typeof ProjectUpdateType[number];

export const SyncDirection = [
  "CLOUD_TO_LOCAL",
  "LOCAL_TO_CLOUD",
] as const;
export type SyncDirection = typeof SyncDirection[number];

export const SyncEntityType = [
  "EMPLOYEE",
  "TASK",
  "ASSIGNMENT",
  "TASK_UPDATE",
  "PROJECT",
  "PROJECT_UPDATE",
  "ITEM",
  "LOT",
  "INVENTORY_TRANSACTION",
  "AGENT_PROPOSAL",
  "APPROVAL",
] as const;
export type SyncEntityType = typeof SyncEntityType[number];

export const SyncOperation = [
  "CREATE",
  "UPDATE",
  "APPEND",
  "SOFT_DELETE",
  "RECONCILE",
] as const;
export type SyncOperation = typeof SyncOperation[number];

export const SyncStatus = [
  "PENDING",
  "PROCESSING",
  "SUCCEEDED",
  "FAILED_RETRYABLE",
  "FAILED_PERMANENT",
  "CONFLICT",
] as const;
export type SyncStatus = typeof SyncStatus[number];

export const AssignmentStatus = [
  "PENDING",
  "ACCEPTED",
  "REJECTED",
  "CANCELLED",
  "COMPLETED",
] as const;
export type AssignmentStatus = typeof AssignmentStatus[number];

export const AssignmentMethod = [
  "MANUAL",
  "AGENT_SUGGESTED",
  "AGENT_AUTO",
  "REASSIGNED",
] as const;
export type AssignmentMethod = typeof AssignmentMethod[number];

export const TaskMode = [
  "SIMPLE",
  "COMPLEX",
  "CONTROLLED",
] as const;
export type TaskMode = typeof TaskMode[number];

export const TaskStatus = [
  "DRAFT",
  "PENDING_APPROVAL",
  "READY",
  "ASSIGNED",
  "ACCEPTED",
  "IN_PROGRESS",
  "BLOCKED",
  "SUBMITTED",
  "NEEDS_REVIEW",
  "COMPLETED",
  "CANCELLED",
] as const;
export type TaskStatus = typeof TaskStatus[number];

export const TaskCommandType = [
  "CREATE_TASK",
  "ASSIGN_TASK",
  "ACCEPT_TASK",
  "REJECT_TASK",
  "START_TASK",
  "REPORT_PROGRESS",
  "REPORT_BLOCKER",
  "UNBLOCK_TASK",
  "SUBMIT_TASK",
  "REVIEW_TASK",
  "CHANGE_DUE_AT",
  "CANCEL_TASK",
] as const;
export type TaskCommandType = typeof TaskCommandType[number];

export const TaskUpdateType = [
  "ACCEPTED",
  "REJECTED",
  "STARTED",
  "PROGRESS",
  "BLOCKED",
  "UNBLOCKED",
  "SUBMITTED",
  "COMPLETED",
  "COMMENT",
  "CORRECTION",
  "EVIDENCE_ADDED",
] as const;
export type TaskUpdateType = typeof TaskUpdateType[number];
