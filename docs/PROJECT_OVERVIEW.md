# Project Overview

io-career is a daily crawler pipeline for internship and early-career openings in international organizations.

Flow:
1. Load source registry from YAML.
2. Fetch and parse HTML/API/RSS sources.
3. Normalize and deduplicate records.
4. Detect daily new positions.
5. Export datasets, archive snapshot, and website JSON.
