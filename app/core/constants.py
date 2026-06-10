from enum import Enum


# User roles in the L&D Platform (RBAC)
class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    DESIGNER = "DESIGNER"
    LEARNER = "LEARNER"

# Create User API roles
class CreateUserRole(str, Enum):
    LEARNER = "LEARNER"
    DESIGNER = "DESIGNER"
    DEVELOPER = "DEVELOPER"


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
