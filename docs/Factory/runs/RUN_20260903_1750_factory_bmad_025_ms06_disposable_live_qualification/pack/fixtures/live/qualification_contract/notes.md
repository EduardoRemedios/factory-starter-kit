# Live Qualification Contract Fixture

`input.json` freezes the live boundary contract for MS-06: the three allowed BMAD 6.10.0 authoring workflows, the four denial families, the two live hook paths, the pinned driver commands, the promotion rules, and the teardown/residue inventory. `expected.json` freezes the outcomes every live proof must produce. VM-001 revalidates this contract against activation pins; the drivers consume the same boundaries at execution time. Changing either file after I2 invalidates the pack.
