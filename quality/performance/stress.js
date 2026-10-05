// Week 3 — stress and soak.
//
// A load test asks "does it meet the SLA at expected traffic?".
// A stress test asks "where does it break, and how?".
// Those are different questions and they have different stage shapes.
import http from 'k6/http';
import { check } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8080';

export const options = {
  scenarios: {
    // Push past expected load until something gives.
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '2m', target: 200 },
        { duration: '2m', target: 400 },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
    // Hold moderate load for a long time. This is what finds leaks.
    soak: {
      executor: 'constant-vus',
      vus: 30,
      duration: '60m',
      startTime: '8m',
    },
  },
  // Deliberately loose. A stress test is an experiment, not a gate — you are
  // looking for the knee in the curve, and a failed threshold would hide it.
  thresholds: {
    http_req_failed: ['rate<0.25'],
  },
};

export default function () {
  const r = http.get(`${BASE}/`);
  check(r, { 'not a server error': (res) => res.status < 500 });
}
