// Week 4 — smoke.
//
// Under two minutes. Two or three checks. If it takes longer than that it is
// not a smoke test, it is a slow gate that people will learn to skip.
//
// Pick the checks that would tell you the deploy is fundamentally broken —
// not the ones that would tell you a feature has a bug.
import http from 'k6/http';
import { check } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8080';

export const options = {
  vus: 1,
  iterations: 1,
  thresholds: {
    checks: ['rate==1.0'],          // every check must pass
    http_req_duration: ['p(95)<2000'],
  },
};

export default function () {
  const health = http.get(`${BASE}/health`);
  check(health, {
    'health endpoint responds': (r) => r.status === 200,
  });

  const home = http.get(`${BASE}/`);
  check(home, {
    'application serves its entry point': (r) => r.status === 200,
    'entry point is not an error page': (r) => !r.body.includes('Internal Server Error'),
  });

  const api = http.get(`${BASE}/api/items`);
  check(api, {
    'critical API path is alive': (r) => r.status === 200,
  });
}
