export const TaskMode = ["SIMPLE", "COMPLEX", "CONTROLLED"] as const;
export type TaskMode = typeof TaskMode[number];

export const TaskStatus = [
  "DRAFT", "PENDING_APPROVAL", "READY", "ASSIGNED", "ACCEPTED",
  "IN_PROGRESS", "BLOCKED", "SUBMITTED", "NEEDS_REVIEW", "COMPLETED", "CANCELLED"
] as const;
export type TaskStatus = typeof TaskStatus[number];

export const EmployeeRole = ["OWNER", "MANAGER", "TEAM_LEADER", "WORKER", "OBSERVER"] as const;
export type EmployeeRole = typeof EmployeeRole[number];

export const RiskLevel = ["LOW", "MEDIUM", "HIGH", "CRITICAL"] as const;
export type RiskLevel = typeof RiskLevel[number];

export const ApprovalStatus = ["PENDING", "APPROVED", "REJECTED", "CANCELLED", "EXPIRED"] as const;
export type ApprovalStatus = typeof ApprovalStatus[number];
