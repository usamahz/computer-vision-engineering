# Status

Last updated 21 October 2026. Published privately, CI green.

## What shipped

- README.md: sixteen sections in dependency order, 243 core entries, a dated watchlist of
  fourteen lines each with its promotion condition, and the admission rule.
- misc/notes/: conventions, the owner, benchmark and voice briefs, sixteen section drafts with their
  Rejected, Claims, Link notes and Benchmark proposal blocks, the review records (red-team.md,
  evidence-marshal.md, link-verification.md) and the generated changelog.
- misc/scripts/: check_links.py, check_format.py and build_changelog.py, standard library only.
- misc/benchmarks/: sixteen microbenchmarks, one per section, plus the shared harness in common/,
  with results committed from the machine named in each README.
- .github/: three issue forms, a pull request template, and two workflows: quality runs the format
  check, the changelog check and every benchmark in quick mode against a ten second budget;
  links runs the link check on every push and weekly, opening an issue on a dead link.
- CONTRIBUTING.md, LICENSE (MIT).

## What was rejected

Owners rejected 123 sources at draft, each with the rule it failed. Review removed 36 drafted
entries and moved 10 to the watchlist. The red team raised 116 findings, and every one has a
written answer in misc/notes/red-team.md. The evidence marshal ruled on 171 claims, recorded in
misc/notes/evidence-marshal.md. misc/notes/changelog.md counts all of it.

## Verified

- Format checker passes on README.md, CONTRIBUTING.md and every benchmark README.
- Changelog is current.
- All sixteen benchmarks pass quick mode in under three seconds each, and full runs finish in
  under fifteen seconds. A full rerun reproduced every non-timing number bit for bit; only
  latency columns moved.
- Link identity: the first review confirmed 317 of 327 URLs. Every flagged URL was fixed or
  removed, and each of the sixteen sources added in review was confirmed before it went in.

## Not done, stated plainly

1. The live link check ran in CI on the first push and passed with no dead links and no
   mirrors. It runs again on every push and weekly.
2. The marshal's second ruling on 21 rewritten or re-admitted entries did not complete. A usage
   limit stopped it, then it was cancelled to save tokens. Those lines were rewritten to name a
   mechanism and not a measured outcome, but no independent marshal pass has confirmed that.
   They are listed in misc/notes/evidence-marshal.md under the editor's veto procedure.
3. Benchmarks ran on a shared cloud virtual machine (Intel Xeon at 2.10 GHz, four vCPU, no
   GPU), not an Apple M4 Pro. To produce M4 Pro results, run ./run.sh in each benchmark
   directory on that machine and replace each README's Environment block with the measured
   banner.
4. Open coverage gaps, with no verified source available from this container: the JPEG
   specification, rolling shutter, binary descriptors, grouped leakage, dataset withdrawals,
   operating point selection, semantic mean IoU, fine-tuning distortion, video object
   segmentation, optical flow evaluation, classical stereo, and trajectory error protocols.

## Published

Private repository: https://github.com/usamahz/computer-vision-engineering. Layout and
README skeleton aligned with usamahz/cpu-performance-engineering. The banner image slot is
empty until an image is supplied.
