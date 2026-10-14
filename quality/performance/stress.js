// Week 3 — stress and soak.
//
// A load test asks "does it meet the SLA at expected traffic?".
// A stress test asks "where does it break, and how?".
// Those are different questions and they have different stage shapes.
import http from 'k6/http';
import { check } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8080';
// Minutes per stress step. The default (2) is the starter's 8-minute shape.
const STEP_MIN = Number(__ENV.STEP_MIN || 2);
// Soak length. SOAK=0 skips it (60 minutes is too long for a laptop run).
const SOAK = __ENV.SOAK || '60m';

const scenarios = {
  // Push past expected load until something gives.
  stress: {
    executor: 'ramping-vus',
    startVUs: 0,
    stages: [
      { duration: `${STEP_MIN}m`, target: 100 },
      { duration: `${STEP_MIN}m`, target: 200 },
      { duration: `${STEP_MIN}m`, target: 400 },
      { duration: `${STEP_MIN}m`, target: 0 },
    ],
    gracefulRampDown: '30s',
  },
};

// Hold moderate load for a long time. This is what finds leaks.
if (SOAK !== '0') {
  scenarios.soak = {
    executor: 'constant-vus',
    vus: 30,
    duration: SOAK,
    startTime: `${4 * STEP_MIN}m`, // starts when the stress part ends
  };
}

export const options = {
  scenarios,
  summaryTrendStats: ['avg', 'min', 'med', 'p(95)', 'p(99)', 'max'],
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