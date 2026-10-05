// Week 3 — load test.
//
// The workload model is the skill, not the tool. Everything here is a
// modelling decision you should be able to defend:
//   - the stage shape (ramp, steady, ramp-down) reflects how traffic arrives
//   - the scenario mix reflects what users actually do, not what is easy to script
//   - the thresholds come from quality/thresholds.yml, not from taste
import http from 'k6/http';
import { check, group, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8080';

// Every number below is read from the environment, which the workflow fills
// from quality/thresholds.yml. The fallbacks exist so a local run works; they
// are not a second copy of the gate, and if you find yourself editing them
// instead of the yaml, the yaml has stopped being the single source it claims
// to be — which is rule 1 of that file.
const P95      = Number(__ENV.P95_MS      || 500);
const ERR_RATE = Number(__ENV.ERROR_RATE  || 0.01);
const VUS      = Number(__ENV.VUS         || 50);
const RAMP     = __ENV.RAMP_UP   || '1m';
const STEADY   = __ENV.STEADY    || '3m';
const RAMPDOWN = __ENV.RAMP_DOWN || '1m';

export const options = {
  stages: [
    { duration: RAMP,     target: VUS },  // ramp
    { duration: STEADY,   target: VUS },  // steady — this is where you read p95
    { duration: RAMPDOWN, target: 0   },  // ramp down
  ],
  thresholds: {
    http_req_duration: [`p(95)<${P95}`],
    http_req_failed: [`rate<${ERR_RATE}`],
    checks: ['rate>0.99'],
  },
};

// Mix model — adjust the weights to match your own system's traffic.
// Browse 60% / detail 30% / write 10% is a starting point, not a truth.
export default function () {
  group('browse', () => {
    const r = http.get(`${BASE}/`);
    check(r, { 'browse 200': (res) => res.status === 200 });
  });

  if (Math.random() < 0.4) {
    group('detail', () => {
      const r = http.get(`${BASE}/api/items/1`);
      check(r, { 'detail 200': (res) => res.status === 200 });
    });
  }

  if (Math.random() < 0.1) {
    group('write', () => {
      const r = http.post(`${BASE}/api/items`, JSON.stringify({ name: 'load-test' }), {
        headers: { 'Content-Type': 'application/json' },
      });
      check(r, { 'write accepted': (res) => res.status === 200 || res.status === 201 });
    });
  }

  sleep(Math.random() * 2 + 1);   // think time — users do not hammer
}
