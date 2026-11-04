import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 20 }, // Rampa de subida para 20 VUs
    { duration: '20s', target: 50 }, // Estresse em 50 VUs simultâneos
    { duration: '10s', target: 0 },  // Rampa de descida
  ],
  thresholds: {
    http_req_duration: ['p(95)<20'], // Latência p95 deve ficar abaixo de 20ms (busca em memória)
    http_req_failed: ['rate<0.01'],   // Taxa de falha menor que 1%
  },
};

export default function () {
  const BASE_URL = 'http://127.0.0.1:8001/api/v1/buscar';

  // 1. Busca por termo específico
  const resTermo = http.get(`${BASE_URL}?q=dipirona`);
  check(resTermo, {
    'Status é 200 (busca termo)': (r) => r.status === 200,
    'Retornou ao menos 1 resultado': (r) => r.json().total_encontrados > 0,
  });

  // 2. Filtro por forma farmacêutica
  const resForma = http.get(`${BASE_URL}?forma=xarope`);
  check(resForma, {
    'Status é 200 (filtro forma)': (r) => r.status === 200,
    'Retornou medicamentos em xarope': (r) => r.json().total_encontrados > 0,
  });

  sleep(0.2);
}