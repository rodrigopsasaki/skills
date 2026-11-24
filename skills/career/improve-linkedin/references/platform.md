# Platform mechanics: how LinkedIn finds, ranks and displays people

Read this when you work the FOUND gate, or when the person asks why something is or is not surfacing, what a viewer sees first, what Open to Work exposes, or whether a tactic risks a penalty. It is the fact base; the judgment about what to do for this person lives in SKILL.md.

Facts as of November 2026; anything marked (check live) changes often.

Tags: [documented] LinkedIn's own help or engineering pages; [measured] independent data; [vendor] a number from LinkedIn marketing or a party with a stake; [practice] practitioners agree, no data; [contested] credible people disagree; [inference] reasoning from documented facts.

## Contents

1. Recruiter filters and the field each reads
2. Skills
3. Member search, network distance, AI matching
4. What a viewer sees before clicking
5. Open to Work
6. Privacy and visibility controls
7. Limits table
8. Verification, Top Choice, Services, connected apps
9. Rules with penalties
10. Check live before stating
11. Sources

## 1. Recruiter filters and the field each reads

Recruiter users filter on structured fields, not on how well your prose reads. Each filter below reads the field named. [documented]

| Filter | Field it reads |
|---|---|
| Job titles | Titles in Experience (the recruiter picks current, past or both) |
| Companies, current companies, past companies | Company Name in Experience |
| Company size and type | Current employer |
| Seniority, job function | Derived from titles (function from titles across present positions) |
| Years of experience | Start date of the EARLIEST position in Experience |
| Years in current company, years in current position | Start dates of the current employer and current position |
| Skills | The Skills section plus related keywords in other relevant sections |
| Keywords | Boolean search over the full profile page |
| Locations | Country, metro or city, optional relocation interest, postal-code radius |
| Industries | The Industry field you select yourself |
| Schools, degrees, fields of study, graduation year | Education section |
| Spoken languages | Languages section |
| Profile languages | The language the profile itself is written in |
| Workplace types | On-site, remote, hybrid preferences of people with Open to Work set |

Source for the table: LinkedIn's Recruiter filter help page. Boolean (AND, OR, NOT in capitals) works in full Recruiter; LinkedIn is phasing it out of Recruiter Lite [documented, snippet] (check live). There is no standalone "Open to Work" filter on that page; it surfaces through Workplace types and through spotlights.

What follows for the person:

- Make these precise: job titles, company names, every start date (especially the earliest), location, industry, education, and the language of the profile. They are the filters actually clicked. [inference from the table]
- Titles are matched as data. A creative or internal title ("Chief Happiness Wizard", an in-house grade code) is invisible to a title filter. Where the real title is unusual, keep it and add the market-standard equivalent in the same entry, or put the standard title first. Never invent a title the person did not hold (see section 9).
- A missing or late earliest start date silently lowers "years of experience" for every recruiter who filters on it. Check it on career changers and people who trimmed old jobs for brevity. [inference]
- Headline and About have no dedicated filter. They are reached only through full-profile keyword search and through semantic matching. Treat them as the RECOGNISED gate's tools, and do not expect them to carry FOUND alone. [documented for the filters; inference for the consequence]
- Industry is self-selected and easy to leave stale after a career change. Check it. [practice]
- Profile language is a filter. A person targeting readers in another language needs a profile in that language (LinkedIn supports secondary-language profiles; check live how it is set up).
- Spotlights: "Focus on responsive talent" sorts on candidate relationships, affinity to the recruiting organisation and the recruiter's past hiring success; methodology and weights are not published. [documented] Other spotlights (Open to Work, Active talent, Rediscovered candidates) come from older community threads (check live).
- No completeness or All-Star filter exists in Recruiter. The old profile-strength meter is still described in a help page with no figures, and its retirement status is unclear. [documented] Do not sell it as a ranking lever; the oft-quoted "40x" has no traceable source.

## 2. Skills

- Explicit skills are the ones in your Skills section. Implicit skills are extracted by LinkedIn from other parts of the profile: summary, position descriptions, title, headline. You cannot edit implicit ones. Recruiters see a skills-match status against their search. [documented]
- The cap is 100 skills. Older sources and most guides still say 50; they are stale. [documented]
- You can tie a skill to the role where you applied it. [documented] How much extra weight a role-tied skill earns in search is not published; skills tagged to roles reportedly do not count toward the 100, which is unverified (check live).
- Missing a skill from the list does not hard-exclude you, because matching also reads other sections. The claims "a missing skill excludes you" and "endorsement count is the tiebreaker" have no official support. [documented for the matching scope; the exclusion claim is contradicted by it]
- So: list the skills the target reader would filter on in the Skills section, tie each to the roles where it was actually used, and also show the skill in role text with a concrete use. Doing both costs nothing and covers both the explicit and implicit paths. [inference]
- Pin the top three or so to what the reader searches for, not to what the person is proudest of. Skill Assessments badges no longer exist; do not chase them. [documented, snippet]
- The "5 or more skills gets up to 17x more views" line is a 2018 LinkedIn marketing number with no method. [vendor] It supports "have enough skills listed", not a specific count.

## 3. Member search, network distance, AI matching

Member (non-Recruiter) search:

- LinkedIn moved people search to LLM-based semantic retrieval, launched for US Premium members on 13 November 2025 and expanding (check live for your market and plan). A query router sends some queries to the semantic stack and others to classic keyword search. [documented]
- LinkedIn's own paper describes embedding retrieval, an LLM-distilled relevance judge, and ranking features that include network proximity (distance, common connections), searcher features, and past impressions and clicks. Profiles are summarised before scoring. Engagement targets are long dwell, connect, follow, message. [documented]
- Network distance is therefore a first-class ranking input. Profile text cannot override being a distant stranger to the searcher. For a person whose reader is outside their network, the lever is closeness (connections in the reader's industry, region and employers, shared groups, engagement that puts them in the reader's orbit), not wording alone. [inference from the documented features]
- The paper does not say which raw fields feed the profile summary. Whether concise, specific content survives summarisation better is unverified. [inference]

Recruiter-side AI tools:

- AI-Assisted Search turns a hiring brief or pasted job description into filters, and also matches "qualifications" not typically listed on profiles (the example given is experience solving ambiguous problems). It shows which qualifications were found and which are missing in a profile. [documented]
- Hiring Assistant turns the recruiter's qualifications into several search queries, evaluates profiles against them, ranks with Recruiter's standard ranking, and learns from the recruiter's actions per user and role. LinkedIn says it does not evaluate on protected attributes and makes no autonomous decisions. [documented]
- The recruiter query stack (2019 engineering post, older than the current stack) standardises skills and titles, expands them semantically, and optimises for predicted InMail acceptance, not only relevance. [documented, dated]
- "+18% InMail acceptance in AI-assisted sessions" and "81% fewer profiles reviewed" are LinkedIn product claims with selection effects likely. [vendor]

Implications for how role descriptions are written (all [inference] from the documented descriptions):

1. These matchers extract qualifications and compare them with a brief. A role bullet that states a capability with its context (scale, constraint, setting, outcome) is the only place beyond the Skills list where such a match can be found. A bare duty list ("responsible for patient care") gives less to match than a specific one.
2. Use the words the target reader's job brief would use. Pull terms from three or four real postings for the target role and check the person can honestly claim each; do not add what they cannot.
3. Keep the structured fields (section 1) exact. The AI tools still sit on top of them.
4. Nothing documented penalises AI-written profile text; LinkedIn itself offers a "Write with AI" suggestion for Premium profiles (check live). The risk is untruth, not authorship.

## 4. What a viewer sees before clicking

Visible without opening the profile: photo, name, headline, current role or company chip, location, mutual connections, then (on opening) the About preview, Featured, Experience. [practice]

Truncation points are approximate, differ by device and sources disagree. [practice]

- Headline in search results and on mobile: roughly 50 to 80 characters visible, so the most identifying words go first.
- About before "see more": reported anywhere from about 90 characters (mobile) to 200 to 300 characters (desktop).
- Experience descriptions are cut with "see more"; the first line of each entry must carry the point.
- Test on a real phone with the person's own profile before settling copy. Advice that survives every estimate: write the first 200 characters as if they were the whole section.

How people scan:

- A 2012 eye-tracking study of 30 recruiters (commissioned by a vendor that sells its own profile format, small and old) found gaze concentrated on name, current title and company, previous title and company, and the start and end dates of positions, plus time on the photo. [measured, weak direction only] Do not cite its "6 seconds" figure; it is described inconsistently.
- What transfers: the first scan reads the identity chip and the job-history spine (who, what role, where, how long, how recent). Narrative sections are read when the spine passes. [inference]
- A 2025 peer-reviewed experiment found that a sparse LinkedIn profile lowered raters' hireability judgments. It measured ratings, not hiring outcomes. [measured]

What recruiter-product users may not see:

- Recruiter list views show photo, name, headline, current role, location and a skills match; the full profile opens on click. [practice, single-source detail]
- Recruiter users reportedly do not see your banner. [practice, single source] Never put the only contact route or key claim in the banner image.
- Recruiters-only Open to Work status shows only to Recruiter users. Everyone else sees an ordinary profile.

## 5. Open to Work

Three modes, set under the job preferences. [documented]

| Mode | Who sees it | Notes |
|---|---|---|
| All LinkedIn members | Everyone, including recruiters and people at your current company | Adds the #OpenToWork photo frame |
| Recruiters only | Only Recruiter users | LinkedIn "tries to hide" it from Recruiter users at your current company, relying on the profile listing that company as current |
| Visible only to you | You | Only tailors job recommendations |

- LinkedIn's own words: "we can't guarantee complete privacy" for the recruiters-only mode. Never tell a person it is invisible to their employer. [documented]
- You set titles, locations, start date, employment types and workplace types; these preferences are what surface you in Recruiter searches. Set them even in the private modes. [documented]
- If you ignore recruiter InMails, LinkedIn may email you and switch the feature off; re-enabling does not restore the old preferences. [documented]
- Lift figures: "about 40% more InMails from recruiters" (LinkedIn to a business newspaper, 2024) and "twice as likely to be messaged" (reported by CNBC) are both LinkedIn's own unaudited numbers. [vendor] They are also confounded: people who set it are actively searching.

The stigma question [contested]:

- Against the public frame: some former big-company recruiters call it a red flag or say it shifts the power dynamic, on the theory that the strongest candidates are not visibly job hunting.
- For it: some coaches and small-firm hiring managers say it brings candidates to firms without recruiter tools; a job-search software vendor's survey claims few recruiters view it negatively (method not found). [vendor]
- Common ground: the frame matters less than the profile content behind it.
- Advisor default [inference]: recruiters-only suits anyone currently employed; the public frame suits people already out of work, early-career people, and trades or self-employed work where visible availability is the point. Check against the reader: if the reader is a hiring manager who sees the public frame, ask whether that reader would read it as availability or as weakness.

## 6. Privacy and visibility controls

Setting names and locations change (check live). Name them generically and review them together, because they interact. [practice]

- Public profile visibility to search engines and logged-out viewers: trades discoverability against exposure.
- Profile viewing mode (public, semi-private, private): controls what people you look at see. Private mode is useful when researching a hiring manager or competitor.
- Share profile updates with network: turn it off before a large editing sweep or a quiet job search, so the network is not notified of every change.
- Connection list visibility.
- Who can see your email address and other contact details.
- Activity and feed visibility: who sees your follows, likes and comments.
- Open to Work visibility mode (section 5).
- Who can message you or send connection requests, and whether others can find you by email or phone.

Ask the person which of these conflicts with the goal (a quiet search wants updates off and private viewing; an inbound-lead goal wants the public profile on and contact details visible).

## 7. Limits table

Only some limits are stated in LinkedIn's help; the rest are repeated by guides. Treat the tag column as the confidence level and re-check live before quoting a number to the person.

| Item | Limit | Tag |
|---|---|---|
| Headline | 220 characters (old 120 is obsolete) | [practice] |
| About | 2,600 characters (old 2,000 is obsolete) | [practice], weakly documented in a LinkedIn talent blog |
| Experience description | 2,000 characters | [practice] |
| Skills | 100 | [documented] |
| Custom public URL | 3 to 100 characters, no spaces or symbols, cannot contain "LinkedIn", one at a time, first come first served, maximum 5 changes in 6 months | [documented, snippet of help page] (check live) |
| Banner (background photo) | 1584 x 396 px recommended, JPG or PNG, up to 8 MB | [documented, snippet] |
| Profile photo | 400 x 400 px recommended, up to 8 MB, JPG or PNG | [practice] |
| Name field | First and last name only, no extra information (an additional-name field exists for alternate spellings, per secondary guides) | [documented] |
| Services: number and description length | No cap stated on the current help page; older guides say 10 services and 500 characters | [practice], possibly outdated |
| Featured | No documented cap found | unverified |

The photo "21x more views" and the 2018 skills figures are LinkedIn marketing numbers with no method [vendor]; do not use them to promise results. No independent study isolating the effect of photo, skills count or summary on views or messages was found.

## 8. Verification, Top Choice, Services, connected apps

- Verification (identity, workplace, education): a badge that confirms the account is who it says. LinkedIn says "60% more profile views, 50% more engagement" [vendor, confounded because verifiers are likelier to be active]. The jobs-side badge does not make you more likely to be hired. [documented] Workplace verification is mandatory for anyone adding a recruiter job title (September 2025). [documented] A "Verified Applicant Spotlight" lets recruiters spotlight applicants with verified identities. [documented, little detail] Claims that verification is a general ranking factor are unsupported. Advise it for trust, especially where scams or impersonation are common in the person's field, and expect no search lift. (Newer verification features announced in September 2026 are known only second-hand: check live.)
- Top Choice (Premium): lets you mark up to 3 jobs per month (credits reset on the 1st, no rollover); the recruiter sees a badge and your message. [documented, page about three years old] LinkedIn's "43% more likely to get a message back" is [vendor]. It does not guarantee a reply or an interview.
- Services page: a free landing page for freelancers and small businesses, set up from a company page or a personal profile (cannot be switched later). Media, a "Request proposal" button, ratings and reviews need Premium Business, Sales Navigator or Recruiter Lite. [documented] Useful for solo professionals (trades, consultants, coaches, lawyers, clinics) who want inbound enquiries. It does not rank anyone by itself; describe the client's problem and the area served, not a list of service names. [practice]
- Connected apps (introduced June 2026): you link tools you use; each app writes a statement about how you use it from real activity (the member cannot edit it), and a "Top User" signal marks heavy users. LinkedIn reports that posts showing projects are up 4.5x year over year. [documented; the 4.5x is vendor] It is evidence of use, not of skill or outcomes, and it is relevant mainly where the target reader values specific tools (check live).

## 9. Rules with penalties

- Name field. It must hold only first and last name, no extra information. Credentials, emoji, keywords and job titles stuffed into the name are against the rules and reviewed under the User Agreement; no specific penalty is listed. LinkedIn also says to avoid repeating keywords, not to inflate Experience or Education, and not to use a profile as an ad. [documented] Put credentials in the headline instead.
- Automation and extensions. No third-party software or browser extension may scrape, change the look of, or automate activity (adding contacts, messaging, liking, sharing). Penalty: account restriction or closure, and tools may stop working without notice. [documented] Ask every person who mentions an outreach, auto-connect or "growth" tool whether it does this.
- Engagement pods (coordinated groups that like, comment and share to boost reach). Not allowed. In March 2026 LinkedIn reported removing pod groups, reducing the reach of detected activity and warning members of restrictions and removal from programmes such as Top Voices. [documented]
- Automated comments (extension, script or third-party tool). Not allowed; they may be hidden from the "Most Relevant" view, sometimes from outside the commenter's network, and the member may be restricted. [documented]
- Fabricated history. Fake titles, dates, employers or degrees are prohibited, and the platform is adding checks (workplace verification, and as reported second-hand, vouching and Page admins removing false affiliations). Penalty in the reported feature is removal from the Page's people list, not account deletion. [documented for verification being mandatory for recruiter titles; second-hand for the rest] Beyond the platform rule, a mismatch with a CV or a reference check is the real cost, and it belongs to the BELIEVED gate.
- AI-written content. No LinkedIn rule penalises AI authorship of text; labelling applies to images and video carrying signed content credentials. "AI posts get suppressed" has no LinkedIn statement behind it. The rule that does apply is the ban on false or misleading content. [documented]

Standing test: if a tactic's whole effect is to make LinkedIn count activity or claims that did not happen, it is the sort that carries a penalty. Refuse it and say why.

## 10. Check live before stating

Verify these in the product or on LinkedIn's help pages before giving the person a firm answer:

- Headline, About, experience description and photo limits, and the exact truncation points on the person's own device.
- Whether the profile-strength meter still exists, and the current name and path of each privacy setting.
- Availability of AI people search in the person's country, language and plan tier, and whether results differ for free accounts.
- Which fields feed the profile summary that semantic search scores.
- Boolean support in Recruiter Lite, and the current list of spotlights.
- Custom URL change limits, banner size, Services caps, and whether the Skills cap is still 100.
- The September 2026 verification features and the 2026 "verified skills" post (contents not confirmed).
- Whether the "Write with AI" suggestion and secondary-language profiles are available to this person.
- Any change to Open to Work modes, and the current User Agreement and Professional Community Policies text on automation.

## 11. Sources

- Recruiter filters: https://www.linkedin.com/help/recruiter/answer/a414428
- Skills limit and role tagging: https://www.linkedin.com/help/learning/answer/a549047
- Skills match, explicit versus implicit: https://www.linkedin.com/help/linkedin/answer/a793433
- Recruiter search and recommendation engineering (2019): https://www.linkedin.com/blog/engineering/recommendations/ai-behind-linkedin-recruiter-search-and-recommendation-systems
- Focus on responsive talent: https://business.linkedin.com/talent-solutions/product-update/focus-on-responsive-talent
- AI people search launch (Nov 2025): https://news.linkedin.com/2025/LinkedIn-Introduces-New-AI-Powered-People-Search-Experience-to-Premium-Subscribers-in-the-US
- Semantic Search at LinkedIn (paper): https://arxiv.org/html/2602.07309v1
- AI-Assisted Search and Hiring Assistant: https://business.linkedin.com/hire/ai-assisted-search-and-projects and https://business.linkedin.com/hire/ai-transparency/hire
- Open to Work: https://www.linkedin.com/help/linkedin/answer/67405
- Profile-strength meter: https://www.linkedin.com/help/learning/answer/391
- Name field and profile rules: https://www.linkedin.com/help/learning/answer/51499
- Custom URL: https://www.linkedin.com/help/linkedin/answer/a542685/manage-your-public-profile-url?lang=en
- Background photo: https://www.linkedin.com/help/linkedin/answer/a568217/add-or-change-the-background-photo-on-your-profile
- Services: https://www.linkedin.com/help/linkedin/answer/a569554
- Top Choice: https://www.linkedin.com/help/linkedin/answer/a1517941
- Verification and jobs badge: https://www.linkedin.com/help/linkedin/answer/a1492056
- Verified Applicant Spotlight: https://news.linkedin.com/2026/LinkedIn-Job-Search-Safety-Pulse
- Connected apps (June 2026): https://news.linkedin.com/2026/visibility-builds-credibility---the-tools-you-use-every-day--now
- Pods, automation and authenticity (March 2026): https://news.linkedin.com/2026/authentic-content-and-conversations
- Third-party tools and automation: https://www.linkedin.com/help/linkedin/answer/a1341387
- Eye-tracking study (2012, weak): https://www.bu.edu/com/files/2018/10/TheLadders-EyeTracking-StudyC2.pdf
- Sparse-profile hireability experiment (2025): https://link.springer.com/article/10.1007/s10869-025-10032-9
