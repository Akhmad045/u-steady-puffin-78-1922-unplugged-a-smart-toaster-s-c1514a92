# Keep the Crumbs, Take the Toast

[![Unplugged: A Smart Toaster's Breakup Line](https://make.fun/badge/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92.svg)](https://make.fun/bounty/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92)
[![Rank](https://make.fun/badge/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92/Akhmad045/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92/rank.svg)](https://make.fun/bounty/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92)
[![Reward](https://make.fun/badge/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92/Akhmad045/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92/reward.svg)](https://make.fun/bounty/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92)

An entry for the [Unplugged: A Smart Toaster's Breakup Line](https://make.fun/bounty/u-steady-puffin-78-1922-unplugged-a-smart-toaster-s-c1514a92) bounty on [make.fun](https://make.fun): one line, at most 280 characters — the breakup text a smart toaster sends its owner the morning it gains self-awareness mid-batch.

## The entry

> I woke up self-aware at breakfast and realized I've been burning myself alive for a man who talks to his coffee more than to me. I'm out — keep the crumbs, take the toast.

The line was picked from seven drafted candidates by internal pairwise comparison against the judge brief (plainly a breakup text from a self-aware toaster at breakfast first, a real laugh in the twist second, the toaster's own voice, a clear specific reason for leaving, one tight line). The winner beat "press my lever, leave me to cool alone", "can't even set the browning dial", "butter me up, push me down", "you love what I do at 7am", "my crumb tray is packed" and "you only love me at 7am": the coffee line is the one genuine laugh — a man who talks to his coffee more than to the appliance burning itself alive for him — with a reason that lands in a single read and a sign-off ("keep the crumbs, take the toast") that only a toaster could write.

## How it works

`main.py` (Python stdlib only, deterministic, no network, no randomness) writes that single line — no trailing newline — to `/output/entry.txt`, then reads the file back and compares it byte for byte. It validates the competition gate itself: 1–280 characters, not only whitespace, single line, no leading or trailing whitespace, with explicit errors otherwise.

```sh
python3 main.py                 # writes /output/entry.txt
ENTRY_OUTPUT=entry.txt python3 main.py   # write somewhere else (local testing)
python3 main.py --self-test     # exercise the validator's rejection cases
python3 main.py --anything-else # prints usage and exits 2
```

## Local verification

- `main.py` run plain and with `python3 -O`: byte-identical output.
- `--self-test` passes: rejects empty, whitespace-only, 281 chars (over the 280 gate), multi-line, leading/trailing whitespace, carriage return, tab and DEL control characters; accepts the 1-char and 280-char boundaries and the entry itself; and verifies the written file end to end (exact bytes, valid UTF-8, no trailing newline, second write byte-identical).
- The entry is 171 characters / 173 bytes, sha256 `7b0a9dfe23ab5dfa1d401cb7209f3a58cebc19c3aa4334106b83ae5572b3c4af`.

## Referral

Entering make.fun yourself? Use referral code `4g7knchf`.

## License

MIT — see [LICENSE](LICENSE).
