# Gold Weekly — Fixed Report Specification

Version: 1.0

This file is the normative content standard for every weekly issue. The scheduled task may collect and summarize information, but it must not redefine the report structure or editorial rules. Changes to this specification should be deliberate repository changes.

## 1. Purpose

Gold Weekly is a source-first Chinese-language international information digest for readers who may not read English. Its primary job is to collect, preserve, translate/summarize, classify, and link to reliable original sources relevant to gold markets.

The report is **not** primarily a trading note, price forecast, or macro strategy report.

## 2. Editorial priorities

Priority order:

1. Coverage of important international information.
2. Traceability to an original or high-trust source.
3. Accurate Chinese summary for non-English readers.
4. Clear distinction between fact, official statement, media reporting, institutional view, and analysis.
5. Limited contextual explanation.
6. Limited market analysis.

Analysis should normally occupy no more than roughly 10–15% of the report.

## 3. Source hierarchy

### Tier A — Primary

Prefer whenever available:

- central banks;
- finance ministries / treasuries;
- national statistical agencies;
- government gazettes and official statements;
- regulators and exchanges;
- IMF, World Bank, BIS, UN and related international organisations;
- World Gold Council and other direct industry datasets;
- official company disclosures for mining/supply events.

### Tier B — High-trust media

Use for reporting, cross-checking, investigations and market context:

- Reuters;
- Bloomberg;
- AP;
- Financial Times;
- Wall Street Journal;
- BBC;
- other comparably reliable outlets when needed.

### Tier C — Institutional research

Large banks, rating agencies, research institutes and industry bodies may be used for views and analysis. Their forecasts must be labelled as views, not facts.

Low-trust aggregators, anonymous social-media claims and copied articles must never be the sole basis for a key fact.

## 4. Required source-card fields

Every important item must contain:

- source level;
- source name;
- publication date;
- original-language title;
- Chinese summary;
- information type;
- clickable original URL.

Optional but recommended when useful:

- why it matters;
- verification caveat / conflicting account;
- related primary-source URL.

Do not provide a source name without an original-page entry whenever an original page can be preserved.

## 5. Freshness rule

The observation window is the previous weekly period stated in the issue metadata.

If an older document is needed to explain the current policy state, mark it explicitly as **政策基线 / 背景资料**. Never present an older policy decision as if it were newly announced during the observation window.

## 6. Conflict rule

For wars, sanctions, diplomatic disputes and contested claims:

- separate confirmed observations from party statements;
- identify whose claim is being reported;
- preserve materially different accounts side by side;
- do not silently resolve conflicting claims into a single definitive narrative;
- use observable data (shipping, official statistics, satellite/market data when reliable) to cross-check where possible.

## 7. Required report structure

Every issue must render in this order:

1. **本周信息速览** — 5–10 short factual bullets.
2. **国际宏观与政策** — grouped by country/region; source cards.
3. **黄金市场、资金流与供需** — source cards.
4. **地缘政治与战争** — source cards with conflict labelling.
5. **能源与大宗商品** — only materially relevant items.
6. **本周重要原始资料索引** — preserved official / primary links.
7. **下周信息日历** — known scheduled events only; no prediction.
8. **简短参考分析** — 3–5 points maximum; clearly labelled as analysis.
9. **给非专业中文读者的简明摘要** — plain Chinese, understanding-focused, not trading guidance.

## 8. Writing standard

Chinese summaries should:

- summarize the substantive information, not merely translate the headline;
- explain important numbers and policy changes in ordinary Chinese;
- avoid sensational language;
- preserve uncertainty and attribution;
- avoid unexplained finance jargon where possible;
- avoid deterministic “利多/利空” labels as the main organising device.

## 9. Analysis standard

Analysis is explicitly secondary.

Allowed:

- explain possible channels connecting a fact to gold, rates, USD, inflation or safe-haven demand;
- identify variables worth tracking;
- present competing interpretations.

Not allowed:

- guaranteed direction forecasts;
- deterministic buy/sell recommendations;
- presenting analyst forecasts as established outcomes.

Every analysis section must state that it is reference analysis and not investment advice.

## 10. Data and rendering model

`data/issues/YYYY-MM-DD.json` is the **single source of truth** for an issue.

`reports/YYYY-MM-DD.html` is a generated artifact and should normally not be edited directly.

Manual corrections should be made in the JSON issue file, then rebuilt with:

```bash
python scripts/build_site.py
```

The build script validates required sections and fields before rendering. GitHub Actions also runs the build before Pages deployment.

## 11. Manual editing policy

Manual editorial changes are expected and supported.

Safe workflow:

1. Edit the structured issue JSON.
2. Commit the change.
3. GitHub Actions rebuilds the HTML and index automatically.

This preserves human edits across future deployments and keeps data/history reviewable in Git.
