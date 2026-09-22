# 16 — RAG (Will, ~50 min, the most technical class)

LLM + retrieval system. Not a niche trick: it is the default way a model gets
anything it was not trained on. Fine-tuning teaches style, not facts that change
hourly. RAG is for private and changing data.

Terminology:
- Token: what the model reads, ~3/4 of an English word. All limits and bills.
- Context window: one shared budget for input + output. ~1M tokens on 2026 big
  models. Five articles (~72k tokens) fit easily: for five documents, do NOT
  build RAG, just send them. 250B tokens (a mid-size company's docs) is 250k
  windows: not a gap bigger models close, and still paid per request.

## The two pipelines

```
INGESTION (once, before any question)
  documents -> chunking (fixed size, respects nothing) -> embedding model -> vectors
                                                                              |
                                                                              v
                                                                      vector database
                                                                   (vector + original text
                                                                    + metadata, per chunk)

RETRIEVAL (every question)
  question -> SAME embedding model -> vector -> nearest vectors -> top chunks
           -> chunks + question into the prompt -> LLM answers
```

Chunk = unit of retrieval. Embedding model != LLM: no generation, tiny, cheap,
text in -> fixed-length number list out. Similar meaning -> similar numbers.
Retriever ranks by distance, has no idea what "correct" means. Ask for 5, get 5.

Honest details from the talk: ~8k token embed ceiling with silent truncation,
and real models put dog closer to cat than kitten because cat and dog co-occur
constantly. Diagrams lie, statistics do not.

## The silent failure, reproduced

Ingestion with `gemini-embedding-001`, query with `gemini-embedding-2`. Both
3072 dimensions, so no size check can catch it.

- Healthy: top chunk = SpaceX, score 0.6842, next 0.5511.
- Mismatched: top score 0.0293, and the three chunks were pharmacy storage,
  payment failures, vacation policy. Same call path, same result count, no
  exception, no warning, no log line.
- LLM handed the wrong chunks: "the retrieved documents do not contain
  information about what SpaceX launched." Best case. Retrieval still broken,
  nothing in the stack knows.

Scores collapsed ~20x. The score was the only signal.

## Monitoring answer (community task)

If retrieval silently returned wrong documents tomorrow, how would you notice?

1. Golden set: 10-20 question -> expected-chunk pairs, run on schedule against
   production. Alert when top-1 changes. Only direct check of the vector space.
2. Score drift: watch top similarity distribution per day, not result counts
   (counts always return k). 0.68 -> 0.03 is the alert.
3. Groundedness sampling: check answers' claims against retrieved chunks.
   Answer citing what its chunks never said = failure in a suit.

Prevention, cheap: store the embedding model id in vector metadata. Both models
were 3072 wide; the name was the only truth.

## Sizing rule for our projects

Tender RAG: hundreds of docs per client -> RAG. Five documents -> prompt.
Knowing when not to reach for it is half the skill.

Code: `rag_pipeline.py` (needs GOOGLE_API_KEY + DEEPSEEK_API_KEY).
