# R05 Coupling Logic

## Why R05 exists
R04 checks rules one by one. R05 proves that local legality does not guarantee global feasibility.

## Hard coupled equation
`required_span = 2e + nw + (n-1)g`

Where:
- e = edge ligament
- n = opening count
- w = opening width
- g = opening gap

The host is 6000 mm wide in this training model.

## Decision
- If every single R04 rule passes and `required_span <= host_length`, generation may continue.
- If every single R04 rule passes but `required_span > host_length`, classify as `SINGLE_PASS_PACKING_FAIL` and refuse generation.
- This is not a warning. The requested geometry cannot be packed into the host without changing at least one parameter.

## Additional coupling found
Thickness changes three other rules at once:
- edge requirement through `0.50 × thickness`;
- gap requirement through `0.75 × thickness`;
- corner-radius pass requirement through `radius / thickness >= 0.10`.

Therefore changing only wall thickness can invalidate a previously passing edge, gap or radius without changing those absolute dimensions.

## Executed result
Emergent conflicts: 7898 of 30704 single-rule-pass combinations (25.72%).
