# lean/ — trusted statement + certificate harness

Three layers, all kernel-checked end to end (no `sorry` anywhere in this tree):

| file | what it is | status |
|---|---|---|
| `Statement.lean` | the board's problem, transcribed (`DefinesZ`, `ZDiophantineInQWithin`) — explicit binders, `autoImplicit false`, OMR house pattern (`darkhipo/omr-statement`, #145) | compiles clean. Provenance note: the file's header still carries the *transcription window's* "not compiled here" marking from when it was written; as shipped it compiled clean in the campaign gate (2026-11-06) alongside the Dzq build below — the header note is historical, not a claim about the shipped tree. |
| `Dzq/Scaff.lean` | the mechanical half: `SosCert` (residuals, weights, term list), the SoS collapse (`sum_sq_eq_zero_iff`), `EasyDirection`, `DefinesZ.of_sos`, negative-control lemmas (`toy_not_definesZ`, `not_definesZ_of_noninteger_witness`) | kernel-green |
| `Dzq/EasyDirection.lean` | witness-family bridge (`easyDirection_of_witnessFamily`, `easyDirection_of_P_witness`) | kernel-green |
| `Dzq/Conditional.lean` | the conditional frame mirroring the incumbents' dependency graph: `RC_stmt` (their `hyp:RC`), `H_is_height_constant` (their `hyp:o8-height`), `PC_derivation` (RC ⇒ PC, derived never primitive), `QuarticCertificate`, `v4_collapse` at their exact 4,552-residual shape | kernel-green |
| `AxCheck.lean` | axioms used: `[propext, Classical.choice, Quot.sound]` only | kernel-checked |

21 kernel-checked theorems across the three modules (the collapse chain, the witness-family bridges, the conditional frame, and the negative-control instances); the SoS collapse Φ = Σ Rᵢ² is proved as a lemma, not assumed. Every arithmetic claim of the incumbents that this tree does *not* carry is an `opaque` declaration named exactly as they name it (`RC_stmt`, `H_is_height_constant`, `PC_derivation`) — same hypotheses, same names, none hidden.

## Build

- toolchain: **Lean v4.34.1** (`lean-toolchain`), Mathlib at revision **d13f23b7**, 1387 jobs green.
- `lakefile.toml` carries the Mathlib dependency as a **path-dep** to the local staircase-port checkout (how this harness was actually run; keeps the build at zero Mathlib recompilation). To build here without that checkout, replace the `[[require]]` block with:

  ```toml
  [[require]]
  name = "mathlib"
  git = "https://github.com/leanprover-community/mathlib4"
  rev = "d13f23b7"
  ```

- `lake build Dzq` then `lean AxCheck.lean`.

`CERTIFIABILITY.md` ranks the remaining formalization leaves; `GAP_LIST.md` lists what is not in Mathlib (Selmer groups, L-functions, canonical heights).
