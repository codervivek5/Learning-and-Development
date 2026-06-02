from enum import Enum

# Multi-tenant Header
TENANT_HEADER = "X-Organization-ID"


# User roles in the L&D Platform (RBAC)
class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    INSTRUCTIONAL_DESIGNER = "instructional_designer"
    REVIEWER = "reviewer"
    SME = "sme"  # Subject Matter Expert
    LEARNER = "learner"


# Workflow execution phases
class WorkflowPhase(str, Enum):
    ANALYSIS = "analysis"
    DESIGN = "design"
    DEVELOP = "develop"
    REVIEW = "review"


# Workflow execution status
class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_APPROVAL = "waiting_approval"
