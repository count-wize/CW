#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                          ║
║   AI WORKFLOW ORCHESTRATOR v4.1 - "Swiss Watch" Edition                                  ║
║   ══════════════════════════════════════════════════════════════════════════════════════ ║
║                                                                                          ║
║   A comprehensive, production-grade AI workflow orchestration system that coordinates    ║
║   multiple AI agents for automated development tasks.                                    ║
║                                                                                          ║
║   FEATURES:                                                                              ║
║   ─────────────────────────────────────────────────────────────────────────────────────  ║
║   • FIXED: Proper task parsing (only ### Task headers, NOT "Step X:" lines)             ║
║   • FIXED: HTTP polling for reliable dashboard updates (no WebSocket dependency)         ║
║   • Status file protocol for Claude Code completion detection                            ║
║   • Comprehensive state machine with all transitions                                     ║
║   • Error recovery with configurable retries                                             ║
║   • Git integration with auto-commit/push                                                ║
║   • Session persistence and resume capability                                            ║
║   • Built-in testing framework                                                           ║
║   • Sound notifications (macOS)                                                          ║
║   • Auto-cascade between phases                                                          ║
║   • Real-time logging with history                                                       ║
║                                                                                          ║
║   USAGE:                                                                                 ║
║   ─────────────────────────────────────────────────────────────────────────────────────  ║
║   python3 orchestrator.py /path/to/project                                               ║
║   python3 orchestrator.py .                                                              ║
║                                                                                          ║
║   VERSION: 4.1.0                                                                         ║
║   CODENAME: Swiss Watch                                                                  ║
║                                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import re
import signal
import hashlib
import subprocess
import threading
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import deque
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socket

# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ CONSTANTS & CONFIGURATION                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

VERSION = "4.1.0"
CODENAME = "Swiss Watch"

# Server ports
DEFAULT_DASHBOARD_PORT = 3000
DEFAULT_PREVIEW_PORT = 8000

# Phase splitting parameters
MAX_TASKS_PER_PHASE = 6
TARGET_TOKENS_PER_PHASE = 90000
CHARS_PER_TOKEN = 4

# Timing parameters
STATUS_CHECK_INTERVAL = 2  # seconds - how often to check status.json
AUTO_CASCADE_DELAY = 5     # seconds - delay before starting next phase
MAX_RETRIES = 3            # maximum retry attempts per phase
RETRY_DELAY = 10           # seconds - delay before retrying

# File names (relative to .ai-workflow directory)
CONFIG_FILE = "config.json"
STATE_FILE = "state.json"
SESSION_FILE = "session.json"
STATUS_FILE = "status.json"
CURRENT_COMMAND_FILE = "current-command.md"
PLANNING_FILE = "planning.md"
LOG_FILE = "orchestrator.log"


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ ENUMS - State Definitions                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class WorkflowState(Enum):
    """
    Main workflow states.
    
    State Machine Diagram:
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │   IDLE ──► ANALYZING ──► READY ──► RUNNING ──► WAITING_FOR_CLAUDE          │
    │                            │          │              │                      │
    │                            ▼          ▼              ▼                      │
    │                         PAUSED     ERROR ◄────── TESTING                    │
    │                            │          │              │                      │
    │                            └──────────┴──────────────┴──► COMPLETED         │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """
    IDLE = "idle"                              # Initial state, no plan loaded
    ANALYZING = "analyzing"                    # Parsing planning.md
    READY = "ready"                            # Plan loaded, ready to start
    RUNNING = "running"                        # Actively executing phases
    PAUSED = "paused"                          # User paused the workflow
    WAITING_FOR_CLAUDE = "waiting_for_claude"  # Waiting for Claude Code to complete
    TESTING = "testing"                        # Running tests after phase completion
    ERROR = "error"                            # An error occurred
    COMPLETED = "completed"                    # All phases finished successfully


class PhaseState(Enum):
    """
    Individual phase states.
    
    Lifecycle:
    PENDING ──► RUNNING ──► WAITING ──► TESTING ──► COMPLETED
                   │                        │
                   └────────► ERROR ◄───────┘
                   │
                   └────────► SKIPPED
    """
    PENDING = "pending"       # Not yet started
    RUNNING = "running"       # Currently executing
    WAITING = "waiting"       # Waiting for Claude Code
    TESTING = "testing"       # Running tests
    COMPLETED = "completed"   # Successfully finished
    SKIPPED = "skipped"       # User skipped this phase
    ERROR = "error"           # Phase failed


class LogLevel(Enum):
    """Log levels for the logging system."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ DATA CLASSES - Core Data Structures                                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

@dataclass
class Task:
    """
    Represents a single task parsed from planning.md.
    
    CRITICAL PARSING RULE:
    ══════════════════════
    Tasks are ONLY identified by the pattern: ### Task [Letter][Number]: Title
    
    VALID task headers:
        ### Task A1: Fix broken images
        ### Task B2: Update navigation
        ### Task C10: Refactor CSS
    
    INVALID (not counted as tasks):
        Step 1: Do something          ← This is a sub-step, NOT a task
        **Step 2:** Another step      ← This is a sub-step, NOT a task
        1. First action               ← This is a numbered list item
        ## Task A1: Wrong heading     ← Wrong heading level (## not ###)
    """
    id: str                    # Task ID (e.g., "A1", "B2", "C10")
    title: str                 # Task title from the header
    content: str               # Full task content including description
    phase: str                 # Phase letter (A, B, C, etc.)
    line_start: int            # Starting line number in planning.md
    line_end: int              # Ending line number in planning.md
    token_estimate: int = 0    # Estimated token count for this task
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class Phase:
    """
    Represents a group of tasks to be executed together.
    
    Phases are automatically created by the TaskParser by splitting tasks based on:
    - Maximum tasks per phase (default: 6)
    - Maximum tokens per phase (default: 90,000)
    
    Each phase is executed as a unit:
    1. Command file written with all phase tasks
    2. Claude Code executes all tasks
    3. Status file updated to signal completion
    4. Tests run (if enabled)
    5. Next phase begins (if auto-cascade enabled)
    """
    id: str                                          # Phase identifier (A, B, C, etc.)
    name: str                                        # Display name (e.g., "Phase A")
    tasks: List[Task] = field(default_factory=list)  # Tasks in this phase
    state: PhaseState = PhaseState.PENDING           # Current state
    started_at: Optional[str] = None                 # ISO timestamp when started
    completed_at: Optional[str] = None               # ISO timestamp when completed
    error: Optional[str] = None                      # Error message if failed
    test_results: Optional[Dict] = None              # Test results after completion
    files_modified: List[str] = field(default_factory=list)  # Files changed
    retry_count: int = 0                             # Number of retry attempts
    
    @property
    def token_estimate(self) -> int:
        """Total estimated tokens for all tasks in this phase."""
        return sum(t.token_estimate for t in self.tasks)
    
    @property
    def task_count(self) -> int:
        """Number of tasks in this phase."""
        return len(self.tasks)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "tasks": [t.to_dict() for t in self.tasks],
            "state": self.state.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "test_results": self.test_results,
            "files_modified": self.files_modified,
            "retry_count": self.retry_count,
            "token_estimate": self.token_estimate,
            "task_count": self.task_count
        }


@dataclass
class Session:
    """
    Represents a workflow session.
    
    Sessions persist across orchestrator restarts and can be resumed.
    Session data is saved to session.json after every state change.
    
    Session Lifecycle:
    1. Created when orchestrator starts (or loaded from existing file)
    2. Updated during workflow execution
    3. Archived when workflow completes or resets
    """
    id: str                                            # Unique session ID
    created_at: str                                    # ISO timestamp of creation
    project_path: str                                  # Absolute path to project root
    planning_file: str                                 # Path to planning.md
    phases: List[Phase] = field(default_factory=list)  # All phases in this session
    current_phase_index: int = 0                       # Index of current/active phase
    state: WorkflowState = WorkflowState.IDLE          # Current workflow state
    total_tasks: int = 0                               # Total number of tasks
    completed_tasks: int = 0                           # Number of completed tasks
    errors: List[Dict] = field(default_factory=list)   # Error history
    git_commits: List[str] = field(default_factory=list)  # Commit hashes created
    started_at: Optional[str] = None                   # When workflow started
    completed_at: Optional[str] = None                 # When workflow finished
    
    @property
    def current_phase(self) -> Optional[Phase]:
        """Get the current phase being executed."""
        if 0 <= self.current_phase_index < len(self.phases):
            return self.phases[self.current_phase_index]
        return None
    
    @property
    def progress_percent(self) -> float:
        """Calculate overall progress percentage."""
        if not self.phases:
            return 0.0
        completed = sum(1 for p in self.phases if p.state in [PhaseState.COMPLETED, PhaseState.SKIPPED])
        return (completed / len(self.phases)) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "project_path": self.project_path,
            "planning_file": self.planning_file,
            "phases": [p.to_dict() for p in self.phases],
            "current_phase_index": self.current_phase_index,
            "state": self.state.value,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "errors": self.errors,
            "git_commits": self.git_commits,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ LOGGER - Comprehensive Logging System                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class Logger:
    """
    Comprehensive logging system with file output and in-memory buffer.
    
    Features:
    - Logs to file and console simultaneously
    - Maintains circular buffer for recent logs (accessible via API)
    - Color-coded console output for easy reading
    - Thread-safe operations
    - Supports log listeners for real-time updates
    """
    
    # ANSI color codes for console output
    COLORS = {
        "DEBUG": "\033[94m",   # Blue
        "INFO": "\033[92m",    # Green
        "WARN": "\033[93m",    # Yellow
        "ERROR": "\033[91m",   # Red
        "RESET": "\033[0m"     # Reset
    }
    
    def __init__(self, log_dir: Path, max_buffer_size: int = 1000):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to store log files
            max_buffer_size: Maximum number of log entries to keep in memory
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = log_dir / LOG_FILE
        self.max_buffer_size = max_buffer_size
        self.buffer: deque = deque(maxlen=max_buffer_size)
        self.listeners: List[Callable] = []
        self._lock = threading.Lock()
    
    def add_listener(self, callback: Callable[[Dict], None]):
        """Add a callback to be notified of new log entries."""
        with self._lock:
            self.listeners.append(callback)
    
    def remove_listener(self, callback: Callable):
        """Remove a log listener."""
        with self._lock:
            if callback in self.listeners:
                self.listeners.remove(callback)
    
    def _format_entry(self, level: str, message: str) -> Dict:
        """Create a log entry dictionary."""
        return {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
    
    def _write(self, level: str, message: str):
        """
        Write a log entry to file, console, and buffer.
        Thread-safe implementation.
        """
        entry = self._format_entry(level, message)
        
        with self._lock:
            # Add to in-memory buffer
            self.buffer.append(entry)
            
            # Write to log file
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"[{entry['timestamp']}] [{level}] {message}\n")
            except Exception:
                pass  # Don't fail if log file write fails
            
            # Console output with colors
            color = self.COLORS.get(level, "")
            reset = self.COLORS["RESET"]
            timestamp_short = entry['timestamp'].split('T')[1].split('.')[0]
            print(f"{color}[{entry['timestamp'][:19]}] [{level}] {message}{reset}")
            
            # Notify listeners (for real-time updates)
            for listener in self.listeners:
                try:
                    listener(entry)
                except Exception:
                    pass  # Don't fail if listener fails
    
    def debug(self, message: str):
        """Log a debug message."""
        self._write("DEBUG", message)
    
    def info(self, message: str):
        """Log an info message."""
        self._write("INFO", message)
    
    def warn(self, message: str):
        """Log a warning message."""
        self._write("WARN", message)
    
    def error(self, message: str):
        """Log an error message."""
        self._write("ERROR", message)
    
    def get_recent(self, count: int = 100) -> List[Dict]:
        """Get the most recent log entries."""
        with self._lock:
            return list(self.buffer)[-count:]
    
    def clear(self):
        """Clear the log buffer (does not clear file)."""
        with self._lock:
            self.buffer.clear()


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ TASK PARSER - Planning.md Parser                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class TaskParser:
    """
    Parser for planning.md files.
    
    ╔═══════════════════════════════════════════════════════════════════════════════════════╗
    ║ CRITICAL: TASK IDENTIFICATION RULES                                                   ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║                                                                                       ║
    ║ This parser ONLY matches task headers in the EXACT format:                            ║
    ║                                                                                       ║
    ║     ### Task [Letter][Number]: Title                                                  ║
    ║                                                                                       ║
    ║ EXAMPLES OF VALID TASKS (will be parsed):                                             ║
    ║     ### Task A1: Fix broken navigation link                                           ║
    ║     ### Task B2: Update image paths                                                   ║
    ║     ### Task C10: Refactor CSS structure                                              ║
    ║                                                                                       ║
    ║ EXAMPLES OF INVALID (will NOT be parsed as tasks):                                    ║
    ║     Step 1: Do something          ← Sub-step within a task                            ║
    ║     **Step 2:** Format something  ← Formatted sub-step                                ║
    ║     1. First action item          ← Numbered list item                                ║
    ║     ## Task A1: Wrong heading     ← Wrong heading level (## not ###)                  ║
    ║     ### Fix something             ← Missing "Task X#:" prefix                         ║
    ║                                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════╝
    
    The regex pattern: ^###\s+Task\s+([A-Z])(\d+):\s*(.+)$
    - Must start with "### Task"
    - Followed by a single uppercase letter (A-Z)
    - Followed by one or more digits (1-999)
    - Followed by a colon and the task title
    """
    
    # CRITICAL: This pattern ONLY matches "### Task X#:" format
    # It explicitly does NOT match "Step X:" or numbered lists
    TASK_PATTERN = re.compile(
        r'^###\s+Task\s+([A-Z])(\d+):\s*(.+)$',
        re.MULTILINE
    )
    
    # Phase header pattern for organization (optional)
    PHASE_PATTERN = re.compile(
        r'^##\s+(?:PHASE\s+)?([A-Z])[\s:\-]+(.+)$',
        re.MULTILINE | re.IGNORECASE
    )
    
    @classmethod
    def parse(cls, content: str, logger: Logger) -> List[Task]:
        """
        Parse planning.md content and extract tasks.
        
        Args:
            content: The full text content of planning.md
            logger: Logger instance for output
            
        Returns:
            List of Task objects, ordered by appearance in file
        """
        tasks = []
        lines = content.split('\n')
        
        logger.info("Parsing planning.md...")
        logger.debug(f"File has {len(lines)} lines, {len(content):,} characters")
        
        # Find all task matches using the strict pattern
        for match in cls.TASK_PATTERN.finditer(content):
            phase_letter = match.group(1).upper()
            task_num = match.group(2)
            title = match.group(3).strip()
            task_id = f"{phase_letter}{task_num}"
            
            # Calculate line numbers
            start_pos = match.start()
            line_start = content[:start_pos].count('\n') + 1
            
            # Find the end of this task (next task header or next phase header or EOF)
            search_start = match.end()
            next_task = cls.TASK_PATTERN.search(content, search_start)
            next_phase = cls.PHASE_PATTERN.search(content, search_start)
            
            # Determine end position (whichever comes first)
            end_positions = [len(content)]  # Default to EOF
            if next_task:
                end_positions.append(next_task.start())
            if next_phase:
                end_positions.append(next_phase.start())
            end_pos = min(end_positions)
            
            # Extract task content
            task_content = content[match.start():end_pos].strip()
            line_end = line_start + task_content.count('\n')
            
            # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
            token_estimate = len(task_content) // CHARS_PER_TOKEN
            
            task = Task(
                id=task_id,
                title=title,
                content=task_content,
                phase=phase_letter,
                line_start=line_start,
                line_end=line_end,
                token_estimate=token_estimate
            )
            tasks.append(task)
            
            logger.debug(f"  Found Task {task_id}: {title[:50]}{'...' if len(title) > 50 else ''}")
        
        # Log parsing summary
        logger.info(f"Parsed {len(tasks)} tasks from planning.md")
        
        # Count tasks per original phase
        phase_counts: Dict[str, int] = {}
        for task in tasks:
            phase_counts[task.phase] = phase_counts.get(task.phase, 0) + 1
        
        for phase_letter, count in sorted(phase_counts.items()):
            logger.debug(f"  Original Phase {phase_letter}: {count} tasks")
        
        return tasks
    
    @classmethod
    def split_into_phases(
        cls,
        tasks: List[Task],
        max_tasks: int = MAX_TASKS_PER_PHASE,
        max_tokens: int = TARGET_TOKENS_PER_PHASE,
        logger: Optional[Logger] = None
    ) -> List[Phase]:
        """
        Split tasks into phases based on task count and token limits.
        
        The algorithm:
        1. Groups tasks by their original phase letter
        2. Within each group, splits based on max_tasks or max_tokens
        3. Assigns new sequential phase letters (A, B, C, ...)
        
        Args:
            tasks: List of tasks to split
            max_tasks: Maximum tasks per phase (default: 6)
            max_tokens: Maximum tokens per phase (default: 90,000)
            logger: Optional logger for output
            
        Returns:
            List of Phase objects
        """
        if not tasks:
            return []
        
        # Group tasks by their original phase letter
        phase_groups: Dict[str, List[Task]] = {}
        for task in tasks:
            if task.phase not in phase_groups:
                phase_groups[task.phase] = []
            phase_groups[task.phase].append(task)
        
        phases: List[Phase] = []
        phase_counter = 0
        
        # Process each original phase group
        for original_phase in sorted(phase_groups.keys()):
            group_tasks = phase_groups[original_phase]
            current_batch: List[Task] = []
            current_tokens = 0
            
            for task in group_tasks:
                # Check if adding this task would exceed limits
                would_exceed_tasks = len(current_batch) >= max_tasks
                would_exceed_tokens = (current_tokens + task.token_estimate) > max_tokens and current_batch
                
                if would_exceed_tasks or would_exceed_tokens:
                    # Save current batch as a new phase
                    new_phase_id = chr(ord('A') + phase_counter)
                    phases.append(Phase(
                        id=new_phase_id,
                        name=f"Phase {new_phase_id}",
                        tasks=current_batch.copy()
                    ))
                    phase_counter += 1
                    current_batch = []
                    current_tokens = 0
                
                # Add task to current batch
                current_batch.append(task)
                current_tokens += task.token_estimate
            
            # Save remaining tasks in final batch
            if current_batch:
                new_phase_id = chr(ord('A') + phase_counter)
                phases.append(Phase(
                    id=new_phase_id,
                    name=f"Phase {new_phase_id}",
                    tasks=current_batch.copy()
                ))
                phase_counter += 1
        
        # Log summary
        if logger:
            logger.info(f"Split {len(tasks)} tasks into {len(phases)} phases")
            for phase in phases:
                logger.debug(
                    f"  {phase.name}: {phase.task_count} tasks, "
                    f"~{phase.token_estimate:,} tokens"
                )
        
        return phases


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ STATUS PROTOCOL - Claude Code Communication                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class StatusProtocol:
    """
    Protocol for bidirectional communication between orchestrator and Claude Code.
    
    Communication Flow:
    ══════════════════
    
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │   ORCHESTRATOR                              CLAUDE CODE                     │
    │   ────────────                              ──────────                      │
    │        │                                         │                          │
    │        │  1. Writes current-command.md           │                          │
    │        │ ───────────────────────────────────────►│                          │
    │        │                                         │                          │
    │        │                                         │  2. Reads tasks          │
    │        │                                         │  3. Executes work        │
    │        │                                         │  4. Commits & pushes     │
    │        │                                         │                          │
    │        │         5. Updates status.json          │                          │
    │        │ ◄───────────────────────────────────────│                          │
    │        │                                         │                          │
    │        │  6. Detects change (polling)            │                          │
    │        │  7. Runs tests                          │                          │
    │        │  8. Starts next phase                   │                          │
    │        │                                         │                          │
    └─────────────────────────────────────────────────────────────────────────────┘
    
    Status File Format (status.json):
    ═════════════════════════════════
    {
        "version": "4.1.0",
        "protocol": "v1",
        "state": "idle|running|completed|error",
        "current_phase": "A",
        "phases_completed": ["A", "B"],
        "files_modified": ["file1.html", "file2.css"],
        "errors": [],
        "last_updated": "2026-01-21T12:00:00.000Z"
    }
    """
    
    @staticmethod
    def create_initial_status(workflow_dir: Path) -> Dict:
        """
        Create the initial status.json file.
        
        Args:
            workflow_dir: Path to .ai-workflow directory
            
        Returns:
            The status dictionary that was written
        """
        status = {
            "version": VERSION,
            "protocol": "v1",
            "last_updated": datetime.now().isoformat(),
            "state": "idle",
            "current_phase": None,
            "phases_completed": [],
            "files_modified": [],
            "errors": [],
            "messages": []
        }
        
        status_file = workflow_dir / STATUS_FILE
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
        
        return status
    
    @staticmethod
    def read_status(workflow_dir: Path) -> Optional[Dict]:
        """
        Read the current status.json file.
        
        Args:
            workflow_dir: Path to .ai-workflow directory
            
        Returns:
            Status dictionary or None if file doesn't exist or is invalid
        """
        status_file = workflow_dir / STATUS_FILE
        if not status_file.exists():
            return None
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    @staticmethod
    def update_status(workflow_dir: Path, updates: Dict):
        """
        Update the status.json file with new values.
        
        Args:
            workflow_dir: Path to .ai-workflow directory
            updates: Dictionary of values to update
        """
        status_file = workflow_dir / STATUS_FILE
        
        # Read current status
        status = StatusProtocol.read_status(workflow_dir) or {}
        
        # Apply updates
        status.update(updates)
        status["last_updated"] = datetime.now().isoformat()
        
        # Write back
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
    
    @staticmethod
    def get_file_hash(workflow_dir: Path) -> str:
        """
        Get MD5 hash of status.json for change detection.
        
        The orchestrator uses this to detect when Claude Code has
        updated the status file.
        
        Args:
            workflow_dir: Path to .ai-workflow directory
            
        Returns:
            MD5 hash string or empty string if file doesn't exist
        """
        status_file = workflow_dir / STATUS_FILE
        if not status_file.exists():
            return ""
        
        try:
            with open(status_file, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except IOError:
            return ""


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ GIT MANAGER - Git Integration                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class GitManager:
    """
    Git integration for automatic commits and pushes.
    
    Features:
    - Detect if project is a git repository
    - Stage all changes (git add -A)
    - Create semantic commits with phase information
    - Push to remote repository
    - Track modified files
    """
    
    def __init__(self, project_path: Path, logger: Logger):
        """
        Initialize GitManager.
        
        Args:
            project_path: Path to project root
            logger: Logger instance
        """
        self.project_path = project_path
        self.logger = logger
        self.is_git_repo = (project_path / ".git").exists()
        
        if not self.is_git_repo:
            self.logger.warn("Project is not a git repository - git features disabled")
    
    def _run_git(self, *args, timeout: int = 60) -> Tuple[bool, str]:
        """
        Run a git command.
        
        Args:
            *args: Git command arguments
            timeout: Command timeout in seconds
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout + result.stderr
            return result.returncode == 0, output.strip()
        except subprocess.TimeoutExpired:
            return False, "Git command timed out"
        except FileNotFoundError:
            return False, "Git executable not found"
        except Exception as e:
            return False, str(e)
    
    def get_modified_files(self) -> List[str]:
        """
        Get list of modified files in the working directory.
        
        Returns:
            List of modified file paths relative to project root
        """
        if not self.is_git_repo:
            return []
        
        success, output = self._run_git("status", "--porcelain")
        if not success:
            return []
        
        files = []
        for line in output.strip().split('\n'):
            if line.strip():
                # Format: "XY filename" where XY is status code
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    files.append(parts[1].strip())
        
        return files
    
    def stage_all(self) -> bool:
        """
        Stage all changes (git add -A).
        
        Returns:
            True if successful
        """
        if not self.is_git_repo:
            return False
        
        success, output = self._run_git("add", "-A")
        if success:
            self.logger.info("Staged all changes")
        else:
            self.logger.error(f"Failed to stage changes: {output}")
        
        return success
    
    def commit(self, message: str) -> Optional[str]:
        """
        Create a commit with the given message.
        
        Args:
            message: Commit message
            
        Returns:
            Commit hash if successful, None otherwise
        """
        if not self.is_git_repo:
            return None
        
        success, output = self._run_git("commit", "-m", message)
        
        if success:
            # Extract commit hash from output
            hash_match = re.search(r'\[[\w\s]+\s+([a-f0-9]+)\]', output)
            commit_hash = hash_match.group(1) if hash_match else "unknown"
            self.logger.info(f"Committed: {commit_hash[:8]} - {message[:50]}...")
            return commit_hash
        else:
            if "nothing to commit" in output:
                self.logger.info("Nothing to commit")
                return None
            self.logger.error(f"Failed to commit: {output}")
            return None
    
    def push(self) -> bool:
        """
        Push to remote repository.
        
        Returns:
            True if successful
        """
        if not self.is_git_repo:
            return False
        
        success, output = self._run_git("push", timeout=120)
        
        if success:
            self.logger.info("Pushed to remote")
        else:
            self.logger.warn(f"Failed to push: {output}")
        
        return success
    
    def commit_and_push(self, phase_id: str, description: str) -> Optional[str]:
        """
        Stage, commit, and push in one operation.
        
        Args:
            phase_id: Phase identifier for commit message
            description: Description for commit message
            
        Returns:
            Commit hash if successful, None otherwise
        """
        if not self.is_git_repo:
            return None
        
        # Check for changes
        modified = self.get_modified_files()
        if not modified:
            self.logger.info("No changes to commit")
            return None
        
        self.logger.info(f"Committing {len(modified)} modified files")
        
        # Stage all
        if not self.stage_all():
            return None
        
        # Commit with semantic message
        message = f"fix: Phase {phase_id} - {description}"
        commit_hash = self.commit(message)
        
        # Push if commit succeeded
        if commit_hash:
            self.push()
        
        return commit_hash


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ TEST RUNNER - Built-in Testing Framework                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class TestRunner:
    """
    Built-in testing framework for validating changes.
    
    Tests Performed:
    ────────────────
    1. Internal Link Validation - Check all internal hrefs point to existing files
    2. HTML Structure Validation - Check for DOCTYPE, title, charset
    3. Image Reference Check - Verify all referenced images exist
    4. CSS Validation - Basic CSS syntax validation
    
    Test results are saved to test-results/ directory and included in session data.
    """
    
    def __init__(
        self,
        project_path: Path,
        workflow_dir: Path,
        logger: Logger,
        config: Dict
    ):
        """
        Initialize TestRunner.
        
        Args:
            project_path: Path to project root
            workflow_dir: Path to .ai-workflow directory
            logger: Logger instance
            config: Configuration dictionary
        """
        self.project_path = project_path
        self.workflow_dir = workflow_dir
        self.logger = logger
        self.config = config
        self.results_dir = workflow_dir / "test-results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def run_tests(self, phase_id: str) -> Dict:
        """
        Run all tests for a phase.
        
        Args:
            phase_id: Phase identifier
            
        Returns:
            Test results dictionary with structure:
            {
                "phase": "A",
                "timestamp": "2026-01-21T12:00:00Z",
                "status": "passed|failed",
                "tests": [...],
                "summary": {"total": 4, "passed": 4, "failed": 0, "skipped": 0}
            }
        """
        self.logger.info(f"Running tests for Phase {phase_id}...")
        
        results = {
            "phase": phase_id,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }
        
        # Run individual test suites
        tests = []
        tests.append(self._test_internal_links())
        tests.append(self._test_html_structure())
        tests.append(self._test_images())
        tests.append(self._test_css_validity())
        
        results["tests"] = tests
        
        # Calculate summary
        results["summary"]["total"] = len(tests)
        results["summary"]["passed"] = sum(1 for t in tests if t["status"] == "passed")
        results["summary"]["failed"] = sum(1 for t in tests if t["status"] == "failed")
        results["summary"]["skipped"] = sum(1 for t in tests if t["status"] == "skipped")
        
        # Overall status
        results["status"] = "passed" if results["summary"]["failed"] == 0 else "failed"
        
        # Log results
        passed = results["summary"]["passed"]
        failed = results["summary"]["failed"]
        total = results["summary"]["total"]
        
        if failed == 0:
            self.logger.info(f"✅ All tests passed: {passed}/{total}")
        else:
            self.logger.warn(f"⚠️ Tests: {passed} passed, {failed} failed of {total}")
        
        # Save results to file
        timestamp = int(time.time())
        results_file = self.results_dir / f"phase-{phase_id}-{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def _test_internal_links(self) -> Dict:
        """Test that internal links point to existing files."""
        test = {
            "name": "Internal Links",
            "status": "passed",
            "message": "",
            "details": []
        }
        
        html_files = list(self.project_path.glob("**/*.html"))
        broken_links = []
        
        for html_file in html_files[:20]:  # Limit to first 20 files for speed
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                
                # Find all href attributes
                hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
                
                for href in hrefs:
                    # Skip external links, anchors, and special protocols
                    if href.startswith(('#', 'http', 'https', 'mailto:', 'tel:', 'javascript:')):
                        continue
                    
                    # Remove query strings and anchors
                    clean_href = href.split('?')[0].split('#')[0]
                    
                    # Try relative to HTML file
                    target = html_file.parent / clean_href
                    if not target.exists():
                        # Try relative to project root
                        target = self.project_path / clean_href.lstrip('/')
                        if not target.exists():
                            broken_links.append(f"{html_file.name}: {href}")
            except Exception:
                pass
        
        if broken_links:
            test["status"] = "failed"
            test["message"] = f"Found {len(broken_links)} broken internal links"
            test["details"] = broken_links[:10]  # Limit details shown
        else:
            test["message"] = "All internal links are valid"
        
        return test
    
    def _test_html_structure(self) -> Dict:
        """Test basic HTML structure requirements."""
        test = {
            "name": "HTML Structure",
            "status": "passed",
            "message": "",
            "details": []
        }
        
        issues = []
        html_files = list(self.project_path.glob("*.html"))  # Only root HTML files
        
        for html_file in html_files[:10]:
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for DOCTYPE declaration
                if '<!DOCTYPE' not in content.upper():
                    issues.append(f"{html_file.name}: Missing DOCTYPE declaration")
                
                # Check for title tag
                if '<title>' not in content.lower():
                    issues.append(f"{html_file.name}: Missing <title> tag")
                
                # Check for charset declaration
                if 'charset' not in content.lower():
                    issues.append(f"{html_file.name}: Missing charset declaration")
                
            except Exception:
                pass
        
        if issues:
            test["status"] = "failed" if len(issues) > 5 else "passed"
            test["message"] = f"Found {len(issues)} HTML structure issues"
            test["details"] = issues[:10]
        else:
            test["message"] = "HTML structure is valid"
        
        return test
    
    def _test_images(self) -> Dict:
        """Test that image references exist."""
        test = {
            "name": "Image References",
            "status": "passed",
            "message": "",
            "details": []
        }
        
        missing_images = []
        html_files = list(self.project_path.glob("*.html"))
        
        for html_file in html_files[:10]:
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                
                # Find all image sources
                srcs = re.findall(
                    r'src=["\']([^"\']+\.(png|jpg|jpeg|gif|svg|webp))["\']',
                    content,
                    re.IGNORECASE
                )
                
                for src, ext in srcs:
                    # Skip external images and data URIs
                    if src.startswith(('http://', 'https://', 'data:')):
                        continue
                    
                    # Check if image exists
                    img_path = self.project_path / src.lstrip('/')
                    if not img_path.exists():
                        # Try relative to HTML file
                        img_path = html_file.parent / src
                        if not img_path.exists():
                            missing_images.append(src)
            except Exception:
                pass
        
        # Remove duplicates
        missing_images = list(set(missing_images))
        
        if missing_images:
            test["status"] = "failed"
            test["message"] = f"Found {len(missing_images)} missing images"
            test["details"] = missing_images[:10]
        else:
            test["message"] = "All referenced images exist"
        
        return test
    
    def _test_css_validity(self) -> Dict:
        """Basic CSS validation."""
        test = {
            "name": "CSS Validation",
            "status": "passed",
            "message": "",
            "details": []
        }
        
        issues = []
        css_files = list(self.project_path.glob("**/*.css"))
        
        for css_file in css_files[:10]:
            try:
                content = css_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for unmatched braces
                open_braces = content.count('{')
                close_braces = content.count('}')
                if open_braces != close_braces:
                    issues.append(
                        f"{css_file.name}: Mismatched braces "
                        f"({open_braces} open, {close_braces} close)"
                    )
                
            except Exception:
                pass
        
        if issues:
            test["status"] = "failed"
            test["message"] = f"Found {len(issues)} CSS issues"
            test["details"] = issues[:10]
        else:
            test["message"] = "CSS files are valid"
        
        return test


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ CLAUDE CODE MANAGER - Command File Generation                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class ClaudeCodeManager:
    """
    Manages communication with Claude Code.
    
    Responsibilities:
    - Generate command files with phase tasks
    - Format tasks in a clear, executable format
    - Include completion instructions (status.json update)
    - Provide context and guidance for Claude Code
    """
    
    def __init__(self, project_path: Path, workflow_dir: Path, logger: Logger):
        """
        Initialize ClaudeCodeManager.
        
        Args:
            project_path: Path to project root
            workflow_dir: Path to .ai-workflow directory
            logger: Logger instance
        """
        self.project_path = project_path
        self.workflow_dir = workflow_dir
        self.logger = logger
    
    def write_command_file(self, phase: Phase) -> bool:
        """
        Write the command file for a phase.
        
        The command file (current-command.md) contains:
        - Phase information
        - All tasks to execute
        - Completion instructions
        - Status update template
        
        Args:
            phase: Phase to write commands for
            
        Returns:
            True if successful
        """
        try:
            content = self._build_command_content(phase)
            command_file = self.workflow_dir / CURRENT_COMMAND_FILE
            
            with open(command_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Wrote command file for Phase {phase.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write command file: {e}")
            return False
    
    def _build_command_content(self, phase: Phase) -> str:
        """
        Build the content of the command file.
        
        Args:
            phase: Phase to build content for
            
        Returns:
            Formatted markdown content
        """
        lines = [
            f"# Phase {phase.id} Implementation",
            "",
            f"**Generated:** {datetime.now().isoformat()}",
            f"**Phase:** {phase.id} ({phase.name})",
            f"**Tasks:** {phase.task_count}",
            f"**Estimated tokens:** ~{phase.token_estimate:,}",
            "",
            "---",
            "",
            "## 📋 Instructions",
            "",
            "Execute the following tasks in order. After completing ALL tasks:",
            "",
            "1. **Stage and commit changes:**",
            "   ```bash",
            f'   git add -A && git commit -m "fix: Phase {phase.id} - [brief description]"',
            "   ```",
            "",
            "2. **Push to remote:**",
            "   ```bash",
            "   git push",
            "   ```",
            "",
            "3. **🚨 CRITICAL: Update status.json to signal completion:**",
            "   ```bash",
            "   cat > .ai-workflow/status.json << 'EOF'",
            "   {",
            '     "state": "completed",',
            f'     "current_phase": "{phase.id}",',
            f'     "phases_completed": ["{phase.id}"],',
            '     "files_modified": ["list", "your", "modified", "files"],',
            '     "errors": []',
            "   }",
            "   EOF",
            "   ```",
            "",
            "---",
            "",
            "## 🎯 Tasks",
            ""
        ]
        
        # Add each task
        for i, task in enumerate(phase.tasks, 1):
            lines.append(f"### {i}. Task {task.id}: {task.title}")
            lines.append("")
            
            # Add task content (skip the header line from the original content)
            content_lines = task.content.split('\n')
            for line in content_lines:
                if not line.strip().startswith('### Task'):
                    lines.append(line)
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Completion section
        lines.extend([
            "## ✅ Completion Checklist",
            "",
            "Before marking this phase complete, verify:",
            "",
            "- [ ] All tasks have been completed",
            "- [ ] Changes have been tested locally",
            "- [ ] Git commit has been created",
            "- [ ] Git push has been completed",
            "- [ ] **status.json has been updated** ← MOST IMPORTANT!",
            "",
            "---",
            "",
            "## 🚨 IMPORTANT - Status Update Required",
            "",
            "The orchestrator monitors `.ai-workflow/status.json` for changes.",
            "You **MUST** update this file when done, or the workflow will not continue!",
            "",
            "```json",
            "{",
            '  "state": "completed",',
            f'  "current_phase": "{phase.id}",',
            f'  "phases_completed": ["{phase.id}"],',
            '  "files_modified": ["file1.html", "file2.css"],',
            '  "errors": []',
            "}",
            "```"
        ])
        
        return '\n'.join(lines)


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ SOUND MANAGER - macOS Sound Notifications                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class SoundManager:
    """
    Play system sounds for notifications (macOS only).
    
    Sound Events:
    - start: Phase started (Ping)
    - complete: Phase completed (Glass)
    - error: Error occurred (Basso)
    - warning: Warning notification (Purr)
    - success: Workflow completed (Hero)
    """
    
    # Map of event names to macOS system sounds
    SOUNDS = {
        "start": "Ping",
        "complete": "Glass",
        "error": "Basso",
        "warning": "Purr",
        "success": "Hero"
    }
    
    @classmethod
    def play(cls, sound_name: str):
        """
        Play a system sound.
        
        Args:
            sound_name: Name of the sound event (start, complete, error, etc.)
        """
        # Only works on macOS
        if sys.platform != "darwin":
            return
        
        sound = cls.SOUNDS.get(sound_name, "Ping")
        sound_path = f"/System/Library/Sounds/{sound}.aiff"
        
        try:
            subprocess.run(
                ["afplay", sound_path],
                capture_output=True,
                timeout=2
            )
        except Exception:
            pass  # Don't fail if sound doesn't play


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ HTTP SERVER - Dashboard and API                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class DashboardHandler(SimpleHTTPRequestHandler):
    """
    HTTP request handler for the dashboard and API endpoints.
    
    Dashboard: Served at root (/)
    API Endpoints:
    ──────────────
    GET  /              - Dashboard HTML page
    GET  /api/state     - Current workflow state (JSON)
    GET  /api/logs      - Recent log entries (JSON)
    GET  /api/config    - Current configuration (JSON)
    GET  /api/health    - Health check endpoint
    POST /api/analyze   - Analyze planning.md
    POST /api/start     - Start workflow
    POST /api/pause     - Pause workflow
    POST /api/resume    - Resume workflow
    POST /api/reset     - Reset workflow
    POST /api/start-phase - Start specific phase
    POST /api/skip      - Skip a phase
    POST /api/retry     - Retry a phase
    
    NOTE: This uses HTTP polling instead of WebSocket for reliability.
    The dashboard polls /api/state every 2 seconds.
    """
    
    def __init__(self, *args, orchestrator=None, **kwargs):
        self.orchestrator = orchestrator
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging to reduce noise."""
        pass
    
    def send_cors_headers(self):
        """Send CORS headers for API responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        path = urlparse(self.path).path
        
        if path == '/' or path == '/index.html':
            self._serve_dashboard()
        elif path == '/api/state':
            self._serve_json(self.orchestrator.get_state())
        elif path == '/api/logs':
            self._serve_json(self.orchestrator.get_logs())
        elif path == '/api/config':
            self._serve_json(self.orchestrator.config)
        elif path == '/api/health':
            self._serve_json({"status": "ok", "version": VERSION})
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests."""
        path = urlparse(self.path).path
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        
        # Route to appropriate handler
        if path == '/api/analyze':
            result = self.orchestrator.analyze_plan()
        elif path == '/api/start':
            result = self.orchestrator.start_workflow()
        elif path == '/api/pause':
            result = self.orchestrator.pause_workflow()
        elif path == '/api/resume':
            result = self.orchestrator.resume_workflow()
        elif path == '/api/reset':
            result = self.orchestrator.reset_workflow()
        elif path == '/api/skip':
            phase_id = data.get('phase_id')
            result = self.orchestrator.skip_phase(phase_id)
        elif path == '/api/retry':
            phase_id = data.get('phase_id')
            result = self.orchestrator.retry_phase(phase_id)
        elif path == '/api/start-phase':
            phase_id = data.get('phase_id')
            result = self.orchestrator.start_specific_phase(phase_id)
        else:
            result = {"error": "Unknown endpoint", "path": path}
        
        self._serve_json(result)
    
    def _serve_dashboard(self):
        """Serve the dashboard HTML file."""
        dashboard_path = Path(self.orchestrator.workflow_dir) / "dashboard.html"
        
        if dashboard_path.exists():
            try:
                content = dashboard_path.read_text(encoding='utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', len(content.encode('utf-8')))
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except Exception as e:
                self._serve_json({"error": f"Failed to read dashboard: {e}"}, 500)
        else:
            self._serve_json({"error": "Dashboard not found"}, 404)
    
    def _serve_json(self, data: Any, status: int = 200):
        """Serve a JSON response."""
        try:
            content = json.dumps(data, default=str, ensure_ascii=False)
            content_bytes = content.encode('utf-8')
            
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(content_bytes))
            self.send_header('Cache-Control', 'no-cache')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(content_bytes)
        except Exception as e:
            error_content = json.dumps({"error": str(e)})
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_content.encode('utf-8'))


class ThreadedHTTPServer(HTTPServer):
    """HTTP Server that passes orchestrator reference to handler."""
    
    def __init__(self, *args, orchestrator=None, **kwargs):
        self.orchestrator = orchestrator
        super().__init__(*args, **kwargs)
    
    def finish_request(self, request, client_address):
        """Create handler with orchestrator reference."""
        self.RequestHandlerClass(
            request, client_address, self,
            orchestrator=self.orchestrator
        )


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ MAIN ORCHESTRATOR - Core Engine                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

class Orchestrator:
    """
    Main orchestrator engine that coordinates the entire workflow.
    
    This is the central component that:
    ────────────────────────────────────
    1. Loads and saves configuration
    2. Manages session state (persistence, resume)
    3. Parses planning.md into phases
    4. Executes phases sequentially
    5. Monitors status.json for completion signals
    6. Runs tests after each phase
    7. Handles errors with retry logic
    8. Serves the dashboard and API
    
    Architecture:
    ─────────────
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                          ORCHESTRATOR                                       │
    │                                                                             │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
    │  │   Logger     │  │  TaskParser  │  │  GitManager  │  │  TestRunner  │    │
    │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
    │                                                                             │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
    │  │ ClaudeCode   │  │   Status     │  │    HTTP      │                       │
    │  │   Manager    │  │  Protocol    │  │   Server     │                       │
    │  └──────────────┘  └──────────────┘  └──────────────┘                       │
    │                                                                             │
    │                    ┌──────────────┐                                         │
    │                    │   Session    │                                         │
    │                    │   Manager    │                                         │
    │                    └──────────────┘                                         │
    └─────────────────────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self, project_path: str, config_overrides: Dict = None):
        """
        Initialize the orchestrator.
        
        Args:
            project_path: Path to the project directory
            config_overrides: Optional config values to override defaults
        """
        # Resolve project path to absolute
        self.project_path = Path(project_path).resolve()
        self.workflow_dir = self.project_path / ".ai-workflow"
        
        # Initialize directories
        self._init_directories()
        
        # Initialize logger first (needed by other components)
        self.logger = Logger(self.workflow_dir / "logs")
        self.logger.info(f"AI Workflow Orchestrator v{VERSION} ({CODENAME})")
        self.logger.info(f"Project: {self.project_path}")
        
        # Load configuration
        self.config = self._load_config(config_overrides)
        
        # Initialize components
        self.git = GitManager(self.project_path, self.logger)
        self.test_runner = TestRunner(
            self.project_path, self.workflow_dir, self.logger, self.config
        )
        self.claude = ClaudeCodeManager(
            self.project_path, self.workflow_dir, self.logger
        )
        
        # Load or create session
        self.session: Optional[Session] = None
        self._load_session()
        
        # Server instance
        self.http_server: Optional[ThreadedHTTPServer] = None
        
        # Monitoring state
        self.status_hash = ""
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
    
    def _init_directories(self):
        """Create necessary directories."""
        dirs = [
            self.workflow_dir,
            self.workflow_dir / "phases",
            self.workflow_dir / "logs",
            self.workflow_dir / "test-results",
            self.workflow_dir / "session-history"
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self, overrides: Dict = None) -> Dict:
        """
        Load configuration from file or create defaults.
        
        Args:
            overrides: Optional values to override defaults
            
        Returns:
            Configuration dictionary
        """
        default_config = {
            # Server ports
            "dashboard_port": DEFAULT_DASHBOARD_PORT,
            "preview_port": DEFAULT_PREVIEW_PORT,
            
            # Automation settings
            "auto_cascade": True,              # Automatically start next phase
            "auto_cascade_delay": AUTO_CASCADE_DELAY,  # Delay between phases
            "auto_trigger_claude": True,       # Auto-write command file
            "auto_commit": True,               # Auto-commit after phase
            "auto_push": True,                 # Auto-push after commit
            
            # Notifications
            "sound_notifications": True,        # Play sounds on events
            
            # Error handling
            "max_retries": MAX_RETRIES,         # Max retry attempts
            "retry_delay": RETRY_DELAY,         # Delay before retry
            
            # Testing
            "run_tests": True,                  # Run tests after phases
            
            # Phase splitting
            "max_tasks_per_phase": MAX_TASKS_PER_PHASE,
            "target_tokens_per_phase": TARGET_TOKENS_PER_PHASE,
            
            # Logging
            "log_level": "INFO",
            "max_log_entries": 1000
        }
        
        # Load from file if exists
        config_file = self.workflow_dir / CONFIG_FILE
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
            except Exception:
                pass
        
        # Apply command-line overrides
        if overrides:
            default_config.update(overrides)
        
        # Save config
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _load_session(self):
        """Load existing session or create new one."""
        session_file = self.workflow_dir / SESSION_FILE
        
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Reconstruct session from saved data
                self.session = Session(
                    id=data["id"],
                    created_at=data["created_at"],
                    project_path=data["project_path"],
                    planning_file=data.get("planning_file", ""),
                    current_phase_index=data.get("current_phase_index", 0),
                    state=WorkflowState(data.get("state", "idle")),
                    total_tasks=data.get("total_tasks", 0),
                    completed_tasks=data.get("completed_tasks", 0),
                    errors=data.get("errors", []),
                    git_commits=data.get("git_commits", []),
                    started_at=data.get("started_at"),
                    completed_at=data.get("completed_at")
                )
                
                # Reconstruct phases
                for phase_data in data.get("phases", []):
                    tasks = [Task(**t) for t in phase_data.get("tasks", [])]
                    phase = Phase(
                        id=phase_data["id"],
                        name=phase_data["name"],
                        tasks=tasks,
                        state=PhaseState(phase_data.get("state", "pending")),
                        started_at=phase_data.get("started_at"),
                        completed_at=phase_data.get("completed_at"),
                        error=phase_data.get("error"),
                        test_results=phase_data.get("test_results"),
                        files_modified=phase_data.get("files_modified", []),
                        retry_count=phase_data.get("retry_count", 0)
                    )
                    self.session.phases.append(phase)
                
                self.logger.info(f"Loaded session: {self.session.id}")
                return
                
            except Exception as e:
                self.logger.warn(f"Failed to load session: {e}")
        
        # Create new session
        self.session = Session(
            id=self._generate_session_id(),
            created_at=datetime.now().isoformat(),
            project_path=str(self.project_path),
            planning_file=""
        )
        self._save_session()
    
    def _save_session(self):
        """Save current session to file."""
        if not self.session:
            return
        
        session_file = self.workflow_dir / SESSION_FILE
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session.to_dict(), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        random_part = hashlib.md5(str(time.time()).encode()).hexdigest()[:6]
        return f"session-{timestamp}-{random_part}"
    
    # ════════════════════════════════════════════════════════════════════════════════════════
    # API Methods - Called by HTTP handlers
    # ════════════════════════════════════════════════════════════════════════════════════════
    
    def get_state(self) -> Dict:
        """
        Get current workflow state for API.
        
        Returns:
            State dictionary with session and config
        """
        if not self.session:
            return {"error": "No session"}
        
        return {
            "version": VERSION,
            "session": self.session.to_dict(),
            "config": self.config
        }
    
    def get_logs(self, count: int = 100) -> List[Dict]:
        """Get recent log entries."""
        return self.logger.get_recent(count)
    
    def analyze_plan(self) -> Dict:
        """
        Analyze planning.md and create phases.
        
        This is the first step in the workflow:
        1. Read planning.md
        2. Parse tasks using strict pattern matching
        3. Split tasks into phases
        4. Initialize status file
        
        Returns:
            Result dictionary with success status and counts
        """
        self.logger.info("Analyzing planning.md...")
        self.session.state = WorkflowState.ANALYZING
        self._save_session()
        
        planning_file = self.workflow_dir / PLANNING_FILE
        
        if not planning_file.exists():
            self.logger.error("planning.md not found in .ai-workflow directory")
            self.session.state = WorkflowState.IDLE
            self._save_session()
            return {
                "success": False,
                "error": "planning.md not found. Create .ai-workflow/planning.md with your tasks."
            }
        
        try:
            # Read planning file
            content = planning_file.read_text(encoding='utf-8')
            
            # Parse tasks using strict pattern (only ### Task X#:)
            tasks = TaskParser.parse(content, self.logger)
            
            if not tasks:
                self.logger.error("No tasks found in planning.md")
                self.session.state = WorkflowState.IDLE
                self._save_session()
                return {
                    "success": False,
                    "error": "No tasks found. Tasks must use format: ### Task A1: Title"
                }
            
            # Split into phases based on limits
            phases = TaskParser.split_into_phases(
                tasks,
                max_tasks=self.config.get("max_tasks_per_phase", MAX_TASKS_PER_PHASE),
                max_tokens=self.config.get("target_tokens_per_phase", TARGET_TOKENS_PER_PHASE),
                logger=self.logger
            )
            
            # Update session
            self.session.phases = phases
            self.session.planning_file = str(planning_file)
            self.session.total_tasks = len(tasks)
            self.session.completed_tasks = 0
            self.session.current_phase_index = 0
            self.session.state = WorkflowState.READY
            self._save_session()
            
            # Write individual phase files (for reference)
            self._write_phase_files(phases)
            
            # Initialize status file
            StatusProtocol.create_initial_status(self.workflow_dir)
            
            # Play sound notification
            if self.config.get("sound_notifications"):
                SoundManager.play("start")
            
            return {
                "success": True,
                "tasks": len(tasks),
                "phases": len(phases)
            }
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            self.logger.error(traceback.format_exc())
            self.session.state = WorkflowState.ERROR
            self._save_session()
            return {
                "success": False,
                "error": str(e)
            }
    
    def _write_phase_files(self, phases: List[Phase]):
        """Write individual phase files to phases directory."""
        phases_dir = self.workflow_dir / "phases"
        
        # Clear existing phase files
        for f in phases_dir.glob("phase-*.md"):
            f.unlink()
        
        # Write new phase files
        for phase in phases:
            phase_file = phases_dir / f"phase-{phase.id}.md"
            content = self.claude._build_command_content(phase)
            with open(phase_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def start_workflow(self) -> Dict:
        """
        Start the workflow from the beginning or continue.
        
        Returns:
            Result dictionary
        """
        if not self.session or not self.session.phases:
            return {
                "success": False,
                "error": "No phases to execute. Run analyze first."
            }
        
        self.logger.info("Starting workflow...")
        self.session.state = WorkflowState.RUNNING
        self.session.started_at = datetime.now().isoformat()
        self._save_session()
        
        # Start status monitoring thread
        self._start_monitoring()
        
        # Start first pending phase
        return self._start_next_phase()
    
    def _start_next_phase(self) -> Dict:
        """Find and start the next pending phase."""
        for i, phase in enumerate(self.session.phases):
            if phase.state == PhaseState.PENDING:
                self.session.current_phase_index = i
                return self._start_phase(phase)
        
        # All phases complete
        self.session.state = WorkflowState.COMPLETED
        self.session.completed_at = datetime.now().isoformat()
        self._save_session()
        
        self.logger.info("🎉 All phases completed successfully!")
        
        if self.config.get("sound_notifications"):
            SoundManager.play("success")
        
        return {
            "success": True,
            "message": "All phases completed"
        }
    
    def _start_phase(self, phase: Phase) -> Dict:
        """
        Start execution of a specific phase.
        
        Args:
            phase: Phase to start
            
        Returns:
            Result dictionary
        """
        self.logger.info(f"Starting Phase {phase.id}: {phase.task_count} tasks")
        
        # Update phase state
        phase.state = PhaseState.RUNNING
        phase.started_at = datetime.now().isoformat()
        
        # Update workflow state
        self.session.state = WorkflowState.WAITING_FOR_CLAUDE
        self._save_session()
        
        # Write command file for Claude Code
        if not self.claude.write_command_file(phase):
            phase.state = PhaseState.ERROR
            phase.error = "Failed to write command file"
            self._save_session()
            return {
                "success": False,
                "error": phase.error
            }
        
        # Update status file (signals to dashboard and Claude Code)
        StatusProtocol.update_status(self.workflow_dir, {
            "state": "running",
            "current_phase": phase.id,
            "files_modified": [],
            "errors": []
        })
        
        # Store current hash for change detection
        self.status_hash = StatusProtocol.get_file_hash(self.workflow_dir)
        
        # Play sound
        if self.config.get("sound_notifications"):
            SoundManager.play("start")
        
        return {
            "success": True,
            "phase": phase.id
        }
    
    def start_specific_phase(self, phase_id: str) -> Dict:
        """Start a specific phase by ID."""
        for i, phase in enumerate(self.session.phases):
            if phase.id == phase_id:
                self.session.current_phase_index = i
                self._start_monitoring()
                return self._start_phase(phase)
        
        return {
            "success": False,
            "error": f"Phase {phase_id} not found"
        }
    
    def pause_workflow(self) -> Dict:
        """Pause the workflow."""
        self.logger.info("Pausing workflow...")
        self.session.state = WorkflowState.PAUSED
        self._save_session()
        
        return {"success": True}
    
    def resume_workflow(self) -> Dict:
        """Resume a paused workflow."""
        self.logger.info("Resuming workflow...")
        self.session.state = WorkflowState.RUNNING
        self._save_session()
        
        self._start_monitoring()
        
        return self._start_next_phase()
    
    def reset_workflow(self) -> Dict:
        """Reset the workflow and archive current session."""
        self.logger.info("Resetting workflow...")
        
        # Archive current session if it has data
        if self.session and self.session.phases:
            self._archive_session()
        
        # Create new session
        self.session = Session(
            id=self._generate_session_id(),
            created_at=datetime.now().isoformat(),
            project_path=str(self.project_path),
            planning_file=""
        )
        self._save_session()
        
        # Reset status file
        StatusProtocol.create_initial_status(self.workflow_dir)
        
        # Clear phase files
        for f in (self.workflow_dir / "phases").glob("phase-*.md"):
            f.unlink()
        
        # Clear command file
        command_file = self.workflow_dir / CURRENT_COMMAND_FILE
        if command_file.exists():
            command_file.unlink()
        
        return {"success": True}
    
    def skip_phase(self, phase_id: str) -> Dict:
        """Skip a phase."""
        for phase in self.session.phases:
            if phase.id == phase_id:
                phase.state = PhaseState.SKIPPED
                self.logger.info(f"Skipped Phase {phase_id}")
                self._save_session()
                
                # Auto-cascade if enabled
                if self.config.get("auto_cascade"):
                    return self._start_next_phase()
                
                return {"success": True}
        
        return {
            "success": False,
            "error": f"Phase {phase_id} not found"
        }
    
    def retry_phase(self, phase_id: str) -> Dict:
        """Retry a failed phase."""
        for phase in self.session.phases:
            if phase.id == phase_id:
                if phase.retry_count >= self.config.get("max_retries", MAX_RETRIES):
                    return {
                        "success": False,
                        "error": f"Maximum retries ({MAX_RETRIES}) exceeded"
                    }
                
                phase.state = PhaseState.PENDING
                phase.error = None
                phase.retry_count += 1
                
                self.logger.info(f"Retrying Phase {phase_id} (attempt {phase.retry_count})")
                self._save_session()
                
                return self._start_phase(phase)
        
        return {
            "success": False,
            "error": f"Phase {phase_id} not found"
        }
    
    def _archive_session(self):
        """Archive the current session to history."""
        if not self.session:
            return
        
        history_dir = self.workflow_dir / "session-history"
        archive_file = history_dir / f"{self.session.id}.json"
        
        try:
            with open(archive_file, 'w', encoding='utf-8') as f:
                json.dump(self.session.to_dict(), f, indent=2)
            self.logger.info(f"Archived session: {self.session.id}")
        except Exception as e:
            self.logger.error(f"Failed to archive session: {e}")
    
    # ════════════════════════════════════════════════════════════════════════════════════════
    # Status Monitoring - Background thread that watches status.json
    # ════════════════════════════════════════════════════════════════════════════════════════
    
    def _start_monitoring(self):
        """Start the status monitoring thread."""
        if self.monitor_thread and self.monitor_thread.is_alive():
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.debug("Status monitoring started")
    
    def _stop_monitoring(self):
        """Stop the status monitoring thread."""
        self.running = False
    
    def _monitor_loop(self):
        """
        Background loop that monitors status.json for changes.
        
        This is how the orchestrator detects when Claude Code has
        completed a phase - by watching for changes to status.json.
        """
        while self.running:
            try:
                self._check_status()
                time.sleep(STATUS_CHECK_INTERVAL)
            except Exception as e:
                self.logger.error(f"Monitor error: {e}")
                time.sleep(5)
    
    def _check_status(self):
        """Check status.json for changes indicating completion."""
        # Only check when waiting for Claude
        if self.session.state != WorkflowState.WAITING_FOR_CLAUDE:
            return
        
        # Check if status file has changed
        current_hash = StatusProtocol.get_file_hash(self.workflow_dir)
        if current_hash == self.status_hash:
            return  # No change
        
        # Status file changed - read it
        self.status_hash = current_hash
        status = StatusProtocol.read_status(self.workflow_dir)
        
        if not status:
            return
        
        # Handle different states
        if status.get("state") == "completed":
            self._handle_phase_completion(status)
        elif status.get("state") == "error":
            self._handle_phase_error(status)
    
    def _handle_phase_completion(self, status: Dict):
        """
        Handle phase completion detected from status.json.
        
        Args:
            status: Status dictionary from status.json
        """
        current_phase = self.session.phases[self.session.current_phase_index]
        
        self.logger.info(f"✅ Phase {current_phase.id} completed!")
        
        # Update phase state
        current_phase.state = PhaseState.COMPLETED
        current_phase.completed_at = datetime.now().isoformat()
        current_phase.files_modified = status.get("files_modified", [])
        
        # Update session task count
        self.session.completed_tasks += current_phase.task_count
        
        # Git commit if auto-commit enabled
        if self.config.get("auto_commit"):
            commit_hash = self.git.commit_and_push(
                current_phase.id,
                f"Completed {current_phase.task_count} tasks"
            )
            if commit_hash:
                self.session.git_commits.append(commit_hash)
        
        # Run tests if enabled
        if self.config.get("run_tests"):
            self.session.state = WorkflowState.TESTING
            current_phase.state = PhaseState.TESTING
            self._save_session()
            
            test_results = self.test_runner.run_tests(current_phase.id)
            current_phase.test_results = test_results
            current_phase.state = PhaseState.COMPLETED
        
        self._save_session()
        
        # Play completion sound
        if self.config.get("sound_notifications"):
            SoundManager.play("complete")
        
        # Auto-cascade to next phase
        if self.config.get("auto_cascade"):
            delay = self.config.get("auto_cascade_delay", AUTO_CASCADE_DELAY)
            self.logger.info(f"Auto-cascading to next phase in {delay}s...")
            time.sleep(delay)
            
            # Reset status for next phase
            StatusProtocol.update_status(self.workflow_dir, {
                "state": "idle",
                "current_phase": None,
                "files_modified": [],
                "errors": []
            })
            
            self._start_next_phase()
    
    def _handle_phase_error(self, status: Dict):
        """
        Handle phase error detected from status.json.
        
        Args:
            status: Status dictionary from status.json
        """
        current_phase = self.session.phases[self.session.current_phase_index]
        
        errors = status.get("errors", [])
        error_msg = errors[0] if errors else "Unknown error"
        
        self.logger.error(f"❌ Phase {current_phase.id} error: {error_msg}")
        
        # Update phase state
        current_phase.state = PhaseState.ERROR
        current_phase.error = error_msg
        
        # Update session
        self.session.state = WorkflowState.ERROR
        self.session.errors.append({
            "phase": current_phase.id,
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_session()
        
        # Play error sound
        if self.config.get("sound_notifications"):
            SoundManager.play("error")
        
        # Auto-retry if within limits
        if current_phase.retry_count < self.config.get("max_retries", MAX_RETRIES):
            delay = self.config.get("retry_delay", RETRY_DELAY)
            self.logger.info(f"Auto-retrying in {delay}s...")
            time.sleep(delay)
            self.retry_phase(current_phase.id)
    
    # ════════════════════════════════════════════════════════════════════════════════════════
    # Server Management
    # ════════════════════════════════════════════════════════════════════════════════════════
    
    def start_servers(self):
        """Start the HTTP server for dashboard and API."""
        dashboard_port = self.config.get("dashboard_port", DEFAULT_DASHBOARD_PORT)
        
        # Create HTTP server
        self.http_server = ThreadedHTTPServer(
            ("0.0.0.0", dashboard_port),
            DashboardHandler,
            orchestrator=self
        )
        
        self.logger.info(f"Dashboard: http://localhost:{dashboard_port}")
        
        try:
            self.http_server.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown the orchestrator."""
        self.logger.info("Shutting down...")
        
        self.running = False
        self._save_session()
        
        if self.http_server:
            self.http_server.shutdown()
        
        self.logger.info("Goodbye!")


# ╔══════════════════════════════════════════════════════════════════════════════════════════╗
# ║ MAIN ENTRY POINT                                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════════════════╝

def main():
    """Main entry point for the orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f"AI Workflow Orchestrator v{VERSION} ({CODENAME})",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 orchestrator.py .                    # Use current directory
  python3 orchestrator.py /path/to/project     # Specify project path
  python3 orchestrator.py . --port 8080        # Custom dashboard port
  python3 orchestrator.py . --no-sound         # Disable sound notifications
  python3 orchestrator.py . --no-auto-cascade  # Disable automatic phase cascade
        """
    )
    
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project directory (default: current directory)"
    )
    
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=DEFAULT_DASHBOARD_PORT,
        help=f"Dashboard port (default: {DEFAULT_DASHBOARD_PORT})"
    )
    
    parser.add_argument(
        "--no-auto-cascade",
        action="store_true",
        help="Disable automatic cascade to next phase"
    )
    
    parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disable sound notifications"
    )
    
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="Disable automatic testing after phases"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"AI Workflow Orchestrator v{VERSION} ({CODENAME})"
    )
    
    args = parser.parse_args()
    
    # Build config overrides from arguments
    config = {
        "dashboard_port": args.port
    }
    
    if args.no_auto_cascade:
        config["auto_cascade"] = False
    
    if args.no_sound:
        config["sound_notifications"] = False
    
    if args.no_tests:
        config["run_tests"] = False
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    
    # Create orchestrator instance
    orchestrator = Orchestrator(args.project_path, config)
    
    # Print startup banner
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                          ║
║   🤖 AI WORKFLOW ORCHESTRATOR v{VERSION}                                                   ║
║   ══════════════════════════════════════════════════════════════════════════════════════ ║
║   Codename: {CODENAME}                                                                    ║
║                                                                                          ║
║   Dashboard:  http://localhost:{args.port:<5}                                                  ║
║                                                                                          ║
║   Press Ctrl+C to stop                                                                   ║
║                                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Start servers (blocking)
    orchestrator.start_servers()


if __name__ == "__main__":
    main()
