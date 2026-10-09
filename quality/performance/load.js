// Week 3: load test, written for TalkDesk.
//
// What this simulates: visitors to TalkDesk's API. Each visit starts by
// listing all talks (every visitor sees the list first), then sometimes
// opens one talk, searches, or submits a new talk.
//
// What changed from the starter: ONLY the addresses. The starter called
// /api/items, which TalkDesk does not have (evidence:
// docs/evidence/week3/load-starter-before.txt). The traffic shape (users,
// ramp, steady, think time) is the starter's, unchanged, so this commit
// changes one thing. Whether that shape is right is reader §2.13, next.
//
// Known limits of this workload (for docs/NFT-Strategy.md):
//   - The list returns at most 100 talks (ORDER BY id LIMIT 100), and the
//     database holds about 50,000. Visitors only open talks they saw in the
//     list, so only those 100 are ever read: a warm-cache workload.
//   - Each list request makes 101 database round trips (the planted N+1).
//
// Every number comes from the environment, which the pipeline fills from
// quality/thresholds.yml. The fallbacks below only exist so a local run works.
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Counter } from 'k6/metrics';

const BASE     = __ENV.BASE_URL || 'http://localhost:8080';
const P95      = Number(__ENV.P95_MS     || 500);
const ERR_RATE = Number(__ENV.ERROR_RATE || 0.01);
const VUS      = Number(__ENV.VUS        || 50);
const RAMP     = __ENV.RAMP_UP   || '1m';
const STEADY   = __ENV.STEADY    || '3m';
const RAMPDOWN = __ENV.RAMP_DOWN || '1m';

// The traffic mix: how often a visit does each extra step after the list.
// A starting estimate, not a measurement of real users; say so in
// docs/NFT-Strategy.md.
const DETAIL_SHARE = 0.4;   // 40% of visits open one talk
const SEARCH_SHARE = 0.2;   // 20% search
const WRITE_SHARE  = 0.1;   // 10% submit a new talk
const SEARCH_WORDS = ['test', 'pipeline', 'design', 'scaling', 'delivery'];
const TRACKS       = ['testing', 'architecture', 'delivery', 'culture'];

// Counts the talks this run actually created (each 201 reply adds 1).
// Why a counter: the list API returns at most 100 talks, so counting the list
// before and after can never change. It always reads 100. Found 2026-10-09.
const talksCreated = new Counter('talks_created');

export const options = {
  stages: [
    { duration: RAMP,     target: VUS },  // ramp up
    { duration: STEADY,   target: VUS },  // steady: this is where you read p95
    { duration: RAMPDOWN, target: 0   },  // ramp down
  ],
  thresholds: {
    http_req_duration: [`p(95)<${P95}`],
    http_req_failed:   [`rate<${ERR_RATE}`],
    checks:            ['rate>0.99'],
  },
  // Show p99 in the summary too: reported for the dashboard, not gated.
  summaryTrendStats: ['avg', 'min', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

// Pick one random item from a list.
function pick(list) {
  return list[Math.floor(Math.random() * list.length)];
}

// Runs ONCE before the test: stop early, with a clear message, if TalkDesk
// is not reachable, instead of recording thousands of failed requests.
export function setup() {
  const r = http.get(`${BASE}/health`, { tags: { name: 'setup' } });
  if (r.status !== 200) {
    throw new Error(`TalkDesk is not answering at ${BASE} (status ${r.status}). Is docker compose up?`);
  }
  console.log(`setup: TalkDesk is up at ${BASE}`);
}

// One visit by one simulated user. k6 repeats this for every virtual user.
export default function () {
  let talks = [];

  // Step 1: every visit lists the talks.
  // The `name` tag groups the results by address in the report.
  group('browse: list talks', () => {
    const r = http.get(`${BASE}/api/talks`, { tags: { name: 'GET /api/talks' } });
    if (check(r, { 'list 200': (res) => res.status === 200 })) {
      talks = r.json();
    }
  });

  // Step 2 (40%): open one talk the visitor actually saw in the list.
  if (talks.length > 0 && Math.random() < DETAIL_SHARE) {
    const talk = pick(talks);
    group('detail: open one talk', () => {
      const r = http.get(`${BASE}/api/talks/${talk.id}`, { tags: { name: 'GET /api/talks/{id}' } });
      check(r, { 'detail 200': (res) => res.status === 200 });
    });
  }

  // Step 3 (20%): search the titles. Search checks every title in the
  // database, so unlike the list it gets slower as the database grows.
  if (Math.random() < SEARCH_SHARE) {
    group('search: find talks', () => {
      const q = encodeURIComponent(pick(SEARCH_WORDS));
      const r = http.get(`${BASE}/api/talks/search?q=${q}`, { tags: { name: 'GET /api/talks/search' } });
      check(r, { 'search 200': (res) => res.status === 200 });
    });
  }

  // Step 4 (10%): submit a new talk for a speaker who already exists.
  if (talks.length > 0 && Math.random() < WRITE_SHARE) {
    group('write: submit a talk', () => {
      const body = JSON.stringify({
        speaker_id: pick(talks).speaker.id,
        title: `load-test talk ${__VU}-${__ITER}`,
        abstract: 'Submitted by the k6 load test.',
        track: pick(TRACKS),
      });
      const r = http.post(`${BASE}/api/talks`, body, {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'POST /api/talks' },
      });
      if (check(r, { 'write 201': (res) => res.status === 201 })) {
        talksCreated.add(1);
      }
    });
  }

  // Think time: a pause of 1 to 3 seconds between visits (the starter's).
  sleep(Math.random() * 2 + 1);
}