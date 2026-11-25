# Reason Network Sidecar Fix

## Root cause

Reason Network delivery was reaching the stable Antigravity session as `queued`, but the App-managed sidecar was `Error`. Running the sidecar directly exposed the cause:

`Error: Antigravity must launch this sidecar with agentapi on PATH`

Antigravity shipped `agentapi.bat`, but the sidecar launcher requires a real executable named `agentapi` on Windows.

## Fix

- Added `C:\Users\PC\.gemini\antigravity\bin` to the user PATH.
- Added `C:\Users\PC\.local\bin\agentapi.exe`, a small shim that delegates to Antigravity's native `language_server.exe agentapi`.
- Restarted Antigravity so the sidecar inherited the corrected PATH.
- Kept scheduled Deltrol automations paused to prevent idle conversation spam.

## Verification

- Antigravity Automations shows `Reason Network Always on — Up`.
- Stable-session smoke messages changed from `queued` to `handed_to_agent`.
- `TASK-014-STABLE-LOOP-SMOKE` completed with `PASS` without creating a new conversation or modifying source.
