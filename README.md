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
npx skills@latest add rodrigopsasaki/skills/evolution-loop
```

This uses [skills.sh](https://skills.sh). Prefer to do it by hand? Each skill
is a self-contained directory under [`skills/`](./skills) — copy the one you
want into `~/.claude/skills/` (global) or `.claude/skills/` (per-project).

## The skills

| Skill | What it does |
| --- | --- |
| [`evolution-loop`](./skills/engineering/evolution-loop/SKILL.md) | Grow one capability toward a judgment-scored fitness over a bounded run of rounds — each round the best change you can currently justify, exposed to real feedback, the next round *discovered* from the last rather than planned. The disciplined alternative to "just iterate on it." |
| [`find-shape`](./skills/engineering/find-shape/SKILL.md) | Converge on the shape of a load-bearing design decision — competing proposals from assigned angles, an adversary panel that exists to break them, one synthesis into a design authority the implementation is then held to. The disciplined alternative to "go with the first thing that works." |

The two are complements, not variants: `find-shape` settles a decision in one
adversarial pass; `evolution-loop` matures a capability across many rounds
against real material. Reach for the first when you don't yet know the shape,
the second when you know it and it isn't good enough yet.

## Why these exist

A skill is a way to hand a model — or a teammate — a practice you've already
paid for in mistakes. Not a prompt trick; a discipline, written down once, so
it survives the next context window. These are the ones I've found worth
keeping.

## License

[MIT](./LICENSE) © Rodrigo Sasaki
