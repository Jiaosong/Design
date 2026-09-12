# Chat On Steroids Skill Router Contract v0.1

Purpose:
Connect local execution with OLEANDER reusable skills.

Execution gate:
1. Parse task.
2. Check project state.
3. Resolve applicable skill.
4. Check capability and authority.
5. Execute through adapter.
6. Validate.
7. Produce receipt.

The router does not create project authority. It only selects execution capability.
