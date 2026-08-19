# Runtime readback — v1.28 successor

Executed against the final local canonical source at 390×844 and 430×932.

Observed facts:
- no recorded JS/page errors in tested sequences;
- document width equals viewport width at both targets;
- minimum visible button target = 44px;
- keyboard route pan changes the ROUTE viewport;
- Digital OFF from R06/R13 returns to ROUTE and closes contextual optional reading;
- CLOSED returns to SERVICE with Return behavior;
- Reduced Motion tested with 0 running animations;
- UNKNOWN remains fail-closed.

Pixel evidence exists locally as 13 states × two viewports plus contact sheets. Binary screenshots are not falsely claimed persisted in GitHub in this commit.

This is runtime/implementation evidence only. `Runtime PASS != Design PASS`.
