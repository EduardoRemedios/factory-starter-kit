# Factory Site Design QA

## Comparison target

- Source visual truth:
  - `artifacts/design-qa/source-desktop.png`
  - `artifacts/design-qa/source-mobile.png`
- Browser-rendered implementation:
  - `artifacts/design-qa/implementation-desktop.png`
  - `artifacts/design-qa/implementation-mobile.png`
- Social and favicon assets:
  - `public/og.png`
  - `public/favicon.png`
- Combined comparison evidence:
  - `artifacts/design-qa/desktop-comparison.png`
  - `artifacts/design-qa/mobile-comparison.png`
- Route and state: `/`, English, default hero state.

## Viewports and normalization

### Desktop

- Source pixels: `1503 x 1046`.
- Browser CSS viewport: `1515 x 1025`.
- Browser capture pixels: `1502 x 1015`.
- Browser device pixel ratio: `1.1`.
- Comparison normalization: both images were scaled to `750 x 523` and placed side by side. The comparison is for hierarchy, proportions, typography, spacing, palette and content; the small source/capture height difference was normalized before judgment.

### Mobile

- Source pixels: `853 x 1844`, representing the selected `390 x 844` mobile direction.
- Browser CSS viewport: `399 x 845`.
- Browser capture pixels: `385 x 816`.
- Browser device pixel ratio: `1.1`.
- Comparison normalization: both images were scaled to `390 x 844` and placed side by side.

## Required fidelity surfaces

- Fonts and typography: Inter-first sans-serif stack, regular display weight, restrained uppercase labels and compact UI weights match the selected direction. Desktop headline line count and hierarchy now align. Mobile retains the requested readable `42–48px` display range rather than compressing all delivery steps into the first viewport.
- Spacing and layout rhythm: desktop keeps the asymmetric copy/ledger split, large negative space, fine rules and calm section rhythm. Mobile intentionally stacks explanation, primary action and ledger.
- Colors and visual tokens: the implementation uses the supplied Symphony neutral scale and `#940020` burgundy accent. The former blue/orange system is absent.
- Image quality and asset fidelity: the selected direction contains no photographic or illustrative assets. The Factory wordmark remains crisp, and the social card and favicon now use the same burgundy visual system. No placeholder imagery was introduced.
- Copy and content: the opening message, human-control boundary, single primary action and five-step ledger match the selected direction. The detailed AI-principal explanation remains in the model and authority sections below the fold.

## Comparison history

### Iteration 1

- Earlier finding — P2: the first mobile implementation carried too much explanatory copy, pushed the ledger too far down and felt denser than the source.
- Earlier finding — P2: headline weights and desktop scale created stronger contrast and an extra line compared with the source.
- Fixes:
  - Shortened the opening human-control statement while preserving the detailed role explanation below the fold.
  - Equalized headline weights.
  - Reduced the desktop display maximum to `64px`, restoring the intended two-line desktop statement.
- Post-fix evidence:
  - `artifacts/design-qa/desktop-comparison.png`
  - `artifacts/design-qa/mobile-comparison.png`

## Findings

No actionable P0, P1 or P2 mismatches remain.

- P3: the real mobile implementation shows the first ledger steps and continues naturally below the fold, while the generated mobile source visually compresses the complete ledger into one frame. This is an intentional accessibility and readability trade-off, consistent with the supplied mobile typography guidance.

## Interaction and browser checks

- English and Spanish switching updates visible copy, document language and the shareable `lang` query parameter.
- No public GitHub links appear in either language.
- Codex and Claude installation tabs switch the command content correctly.
- FAQ expansion works, including the regression-testing answer.
- Primary actions resolve to the on-page installation section.
- Open Graph and favicon assets use the selected visual direction and have verified dimensions.
- No browser console errors were recorded.
- No horizontal content overflow was observed at the tested desktop or mobile widths.

## Focused-region comparison

No separate crop was required. The selected source visuals are hero-only designs, and their typography, controls, ledger rows and labels remain readable in the original full-view captures and the normalized side-by-side comparisons.

## Verification

- Static content and privacy guard: passed.
- Lint: passed.
- Production build: passed.
- Server-rendered English and Spanish tests: passed.

final result: passed
