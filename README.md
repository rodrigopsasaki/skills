# skills

Agent skills I actually use, straight from my `.claude` directory. Each one
encodes a practice I'd otherwise have to explain from scratch every time.

Portable across agents that read the [Agent Skills](https://code.claude.com/docs/en/skills)
format (Claude Code, and anything else that loads `SKILL.md`).

## Install

Install everything (globally, into your agent):

```bash
npx skills@latest add rodrigopsasaki/skills
```

Or pick a single skill:

```bash
npx skills@latest add rodrigopsasaki/skills/find-shape
```

This uses [skills.sh](https://skills.sh). Prefer to do it by hand? Each skill
is a self-contained directory under [`skills/`](./skills) — copy the one you
want into `~/.claude/skills/` (global) or `.claude/skills/` (per-project).

## The skills

| Skill | What it does |
| --- | --- |
| [`find-shape`](./skills/engineering/find-shape/SKILL.md) | Find the shape of one capability by growing it toward a judgment-scored fitness over a bounded run of rounds — each round the best change you can currently justify, exposed to real feedback, the next round *discovered* from the last rather than planned. The disciplined alternative to "just iterate on it." |
| [`improve-linkedin`](./skills/career/improve-linkedin/SKILL.md) | Review and improve a LinkedIn presence for any career, country and language. One model in place of the usual checklist: a profile answers one specific reader, who has to find you, recognise you, believe you and know what to do next, in that order. Ranks the few changes that matter, writes the replacement text from your own facts, says so when LinkedIn is not where your decision gets made, and grades every claim it makes (documented, measured, vendor, practice, folklore). |

## Why these exist

A skill is a way to hand a model — or a teammate — a practice you've already
paid for in mistakes. Not a prompt trick; a discipline, written down once, so
it survives the next context window. These are the ones I've found worth
keeping.

## License

[MIT](./LICENSE) © Rodrigo Sasaki
