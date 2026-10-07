-- TalkDesk seed data.
--
-- Generated in SQL rather than as thousands of INSERT statements: the file
-- stays small and readable, and it loads in a few seconds.
--
-- Size is deliberate. 500 rows would make the unindexed search (D-2) too fast
-- to measure, and a defect a learner cannot detect is not a teaching defect.
-- 200 speakers and 50 000 talks is enough for a full table scan to be an order
-- of magnitude worse than an indexed read, and still small enough to start
-- quickly and to reason about.

-- deterministic pseudo-random from an integer, so every learner gets identical data
CREATE OR REPLACE FUNCTION det(seed INT, lo INT, hi INT) RETURNS INT AS $$
  SELECT lo + (abs(hashint4(seed)) % (hi - lo + 1));
$$ LANGUAGE SQL IMMUTABLE;

INSERT INTO speakers (name, email, bio)
SELECT
  (ARRAY['Amara','Chen','Priya','Tomas','Ines','Kwame','Lena','Rafael','Yuki','Nadia',
         'Oscar','Fatima','Dmitri','Aoife','Mateo','Sanjay','Elke','Jonas','Rania','Bo'])[det(i,1,20)]
  || ' ' ||
  (ARRAY['Okafor','Whitfield','Nair','Berg','Duarte','Mensah','Kowalski','Ferreira','Tanaka','Haddad',
         'Lindqvist','Rahman','Volkov','Byrne','Castillo','Iyer','Brandt','Meyer','Aziz','Zhang'])[det(i*3,1,20)],
  'speaker' || i || '@talkdesk.test',
  'Has spoken on software quality for ' || det(i*7,2,15) || ' years.'
FROM generate_series(1, 200) AS i;

INSERT INTO talks (speaker_id, title, abstract, track, status, score, created_at)
SELECT
  det(i, 1, 200),
  (ARRAY['Testing','Automating','Refactoring','Measuring','Rethinking','Scaling','Debugging',
         'Designing','Instrumenting','Governing','Simplifying','Hardening','Observing','Owning'])[det(i*11,1,14)]
  || ' ' ||
  (ARRAY['What You Cannot See','the Unhappy Path','a Legacy Suite','Flaky Tests at Scale',
         'the Deployment Pipeline','Quality as Policy','the Feedback Loop','Contract Boundaries',
         'Accessibility from Day One','the Cost of Coverage','Load Under Pressure',
         'Security in the Build','Trust in Metrics','the Handover','Technical Debt Honestly',
         'Teams That Ship','the Long Tail of Latency','Tests Nobody Reads'])[det(i*17,1,18)]
  || ' (' || i || ')',
  'A practical session with worked examples and a takeaway checklist.',
  (ARRAY['testing','architecture','delivery','culture'])[det(i*5,1,4)],
  (ARRAY['submitted','submitted','submitted','accepted','rejected'])[det(i*13,1,5)],
  CASE WHEN det(i*13,1,5) = 1 THEN NULL ELSE det(i*19,1,10) END,
  TIMESTAMP '2026-01-01 00:00:00' + (det(i*23,0,200) || ' days')::INTERVAL
FROM generate_series(1, 50000) AS i;

DROP FUNCTION det(INT,INT,INT);

ANALYZE speakers;
ANALYZE talks;
